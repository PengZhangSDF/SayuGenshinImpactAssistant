import threading
import time
from utils.GIautogui import GIautogui as pyautogui
import pyautogui as pyautogui_real
from utils import OCR
import pydirectinput
import re
import os
import json
import config
from utils.Tools import read_config_value as rcv
import Package.log_config
import cv2
import AutoFight.AutoFight_tools
import numpy as np
path = config.get_config_directory()
os.chdir(path)  # 更改工作目录为脚本所在目录
print("AutoFightConfig.py:当前工作目录：", os.getcwd())  # 打印当前工作目录

logger = Package.log_config.logger
stop_event = threading.Event()

with open('./AutoFight/combat_avatar.json', 'r', encoding='utf-8') as file:
    character_data = json.load(file)
def is_white_region_present(x1, y1, x2, y2, saturation_threshold=0.10, brightness_threshold=0.90, area_threshold=0.7):
    """saturation_threshold：用于判断低饱和度的阈值，表示白色区域的饱和度应该低于此值。
    brightness_threshold：用于判断高亮度的阈值，表示白色区域的亮度应该高于此值。
    area_threshold：用于判断白色区域的占比，如果满足白色条件的像素比例超过此值，函数返回 True，否则返回 False。"""
    # 截取屏幕指定区域
    screenshot = pyautogui_real.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 提取S通道（饱和度）和V通道（亮度）
    saturation = hsv_image[:, :, 1]
    brightness = hsv_image[:, :, 2]

    # 计算满足条件（低饱和度和高亮度）的像素数量
    white_pixels = np.sum((saturation < (saturation_threshold * 255)) & (brightness > (brightness_threshold * 255)))

    # 计算总像素数量
    total_pixels = saturation.size

    # 计算满足条件的白色像素占总像素的比例
    white_ratio = white_pixels / total_pixels

    # 如果白色像素比例大于指定阈值，返回True，否则返回False
    try:
        return white_ratio > area_threshold
    except:
        return False

def recognition_front_character():
    list_under = []
    dead0 = is_white_region_present(1859,258,1885,280)
    dead1 = is_white_region_present(1858,354, 1885,375)
    dead2 = is_white_region_present(1858,449, 1885,470)
    dead3 = is_white_region_present(1859,546, 1884,566)
    logger.info(dead0,dead1,dead2,dead3)
    list_dead=[dead0,dead1,dead2,dead3]
    if dead0 or dead1 or dead3 or dead2:
        dead = True
        num = 0
        for i in list_dead:
            num = num + 1
            if i:
                dead_character = num
                list_under.append(num)
    list1 = [1, 2, 3, 4]
    complement = list(set(list1) - set(list_under))
    logger.info(f'当前角色：{complement}')
    return complement


def check_skill_release_success():
    """检查技能释放是否成功"""
    result = OCR.ppocr(1673, 974, 1718, 1007, model='int')
    logger.info(f"检测到的结果：{result}")

    # 判断结果列表中是否包含数字
    contains_digit = any(str(int(item)).isdigit() for item in result)

    return contains_digit


def load_character_aliases(character_data):
    alias_mapping = {}
    for character in character_data:
        for alias in character["alias"]:
            alias_mapping[alias] = character["name"]
    return alias_mapping

alias_mapping = load_character_aliases(character_data)

def parse_config(file_path):
    character_actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split()
                character = parts[0]
                actions = parts[1].split(',')
                character_actions.append((character, actions))
    logger.info("解析配置文件：%s", character_actions)
    return character_actions

def fast_mouse_circle(times):
    for _ in range(times):
        pydirectinput.moveRel(2000, 0, duration=0.1, relative=True)  # 向右移动

def clean_ocr_result(ocr_results):
    clean_results = {}
    for character, coords in ocr_results.items():
        clean_character = re.sub(r'[^\u4e00-\u9fa5]', '', character)  # 仅保留汉字字符
        if clean_character in alias_mapping:
            clean_results[alias_mapping[clean_character]] = coords
        elif clean_character:
            clean_results[clean_character] = coords
    return clean_results

def get_characters_from_screen():
    ocr_results = OCR.ppocr(1660, 235, 1764, 574, model='box and text')
    clean_results = clean_ocr_result(ocr_results)
    logger.info("OCR结果：%s", clean_results)

    character_positions = []
    for character, (x1, y1, x2, y2) in clean_results.items():
        character_positions.append((character, y1))
    character_positions.sort(key=lambda x: x[1])
    sorted_characters = [char for char, y in character_positions]
    logger.info("排序后的角色：%s", sorted_characters)
    return sorted_characters

def find_best_matching_config(current_characters):
    config_directory = './AutoFight/AutoFightconfig'
    best_match_file = None
    best_match_count = 0

    for file_name in os.listdir(config_directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(config_directory, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                config_characters = [line.split()[0] for line in file if line.strip()]
                match_count = len(set(current_characters) & set(config_characters))
                if match_count > best_match_count:
                    best_match_count = match_count
                    best_match_file = file_path

    return best_match_file

def perform_action(character, action):
    logger.info("开始执行动作：%s, %s", character, action)
    max_retries = 3  # 最多重试次数
    parts = action.split('(')
    action_name = parts[0]
    param = parts[1][:-1] if len(parts) > 1 else None
    if not stop_event.is_set():
        if action_name == 'skill' or action_name == 'e':  # E技能配置--草神专配
            for attempt in range(max_retries):
                if param == 'hold':
                    time.sleep(0.2)
                    pyautogui.keyDown('e')
                    if character == '纳西妲':
                        time.sleep(0.2)
                        fast_mouse_circle(4)
                        pyautogui.keyUp('e')
                    elif character == '枫原万叶':
                        time.sleep(1)
                        pyautogui.keyDown('e')
                        time.sleep(1.35)
                    else:
                        time.sleep(1)
                        pyautogui.keyUp('e')
                        time.sleep(1)
                else:
                    pyautogui.press('e')
                    time.sleep(0.35)

                # 检查技能释放是否成功
                if check_skill_release_success():
                    logger.info(f"{character} 的技能释放成功")
                    break
                else:
                    logger.warning(f"{character} 的技能释放失败，重试 {attempt + 1}/{max_retries} 次")
                    pyautogui.press('shift')  # 释放失败后按下shift键
                    time.sleep(0.25)
            else:
                logger.error(f"{character} 的技能释放失败超过 {max_retries} 次，视为成功")


        elif action_name == 'burst' or action_name == 'q':  # 大招配置
            time.sleep(0.2)
            result = AutoFight.AutoFight_tools.is_vibrant()
            if result:
                pyautogui.press('q')
                time.sleep(2.2)
            else:
                logger.info(f'{character} 大招未充能完毕')

        elif action_name == 'attack':  # 普攻配置
            duration = float(param) if param else 0.2
            end_time = time.time() + duration
            while time.time() < end_time:
                pyautogui.click()
                time.sleep(0.3)

        elif action_name == 'charge':  # 重击配置--那位维莱特专配
            duration = float(param) if param else 0.2
            pyautogui.mouseDown()
            if character == '那维莱特':
                fast_mouse_circle(40)
                pyautogui.mouseUp()
                time.sleep(0.5)
            else:
                time.sleep(duration)
            pyautogui.mouseUp()
            time.sleep(0.5)

        elif action_name == 'wait':  # 等待 秒
            duration = float(param) if param else 0.5
            time.sleep(duration)

        elif action_name == 'dash':  # 闪避
            duration = float(param) if param else 0.5
            pyautogui.keyDown('shift')
            time.sleep(duration)
            pyautogui.keyUp('shift')
            time.sleep(0.45)

        elif action_name == 'jump' or action_name == 'j':
            pyautogui.press('space')

        elif action_name == 'walk':
            direction = param.split(',')[0]
            duration = float(param.split(',')[1])
            pyautogui.keyDown(direction)
            time.sleep(duration)
            pyautogui.keyUp(direction)

        elif action_name in ['w', 'a', 's', 'd']:
            duration = float(param) if param else 0.2
            pyautogui.keyDown(action_name)
            time.sleep(duration)
            pyautogui.keyUp(action_name)
        logger.info("完成动作：%s, %s", character, action)


def is_grayscale_region_present(x1, y1, x2, y2, saturation_threshold=0.12, area_threshold=0.77):
    # 截取屏幕指定区域
    screenshot = pyautogui_real.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 提取S通道（饱和度）
    saturation = hsv_image[:, :, 1]

    # 计算饱和度低于阈值的像素数量
    low_saturation_pixels = np.sum(saturation < (saturation_threshold * 255))

    # 计算总像素数量
    total_pixels = saturation.size

    # 计算低饱和度像素占总像素的比例
    low_saturation_ratio = low_saturation_pixels / total_pixels

    # 如果低饱和度像素比例大于指定阈值，返回True，否则返回False
    if low_saturation_ratio > area_threshold:
        return True
    else:
        return False

def recognition_dead():
    dead0 = is_grayscale_region_present(1775,224,1825,287)
    dead1 = is_grayscale_region_present(1778,333, 1832,384)
    dead2 = is_grayscale_region_present(1778,427, 1830,477)
    dead3 = is_grayscale_region_present(1778,522, 1827,578)
    list_dead=[dead0,dead1,dead2,dead3]
    if dead0 or dead1 or dead3 or dead2:
        dead = True
        num = 0
        for i in list_dead:
            num = num + 1
            if i:
                dead_character = num
    else:
        dead = False
        logger.info('没有角色死亡')
        dead_character = None
        return dead_character
    if dead:
        logger.warning('存在角色死亡')
        logger.warning(f'死亡角色：{dead_character}号角色')
        return dead_character

def using_combat_file():
    config_file = rcv('./config.txt', 'AutoFight', 'using_combat_file')
    config_directory = './AutoFight/AutoFightconfig/'
    try:
        config_file = config_directory + config_file
    except TypeError:
        return False
    return config_file

def switch_character(target_key, target_character):
    max_attempts = 30  # 设置尝试次数
    for attempt in range(max_attempts):
        pyautogui.press(target_key)  # 按下目标角色的按键
        time.sleep(0.1)  # 等待 0.1 秒，确保切换完成
        current_characters = recognition_front_character()  # 获取当前屏幕上的角色编号

        # 检查切换是否成功
        if target_character in current_characters:
            logger.info(f"成功切换到角色：{target_character}, 按键：{target_key}")
            return True

        logger.warning(f"切换失败，重试 {attempt + 1}/{max_attempts} 次")

    logger.error(f"切换到角色 {target_character} 失败")
    return False

def main(config_file=using_combat_file()):
    stop_event.clear()
    characters_on_screen = get_characters_from_screen()
    zhongli_in_team = '钟离' in characters_on_screen
    last_zhongli_time = time.time() - 11  # 初始化为一个较早的时间

    if config_file:
        character_actions = parse_config(config_file)
    else:
        best_match_file = find_best_matching_config(characters_on_screen)
        if best_match_file:
            logger.info("使用最匹配的配置文件：%s", best_match_file)
            character_actions = parse_config(best_match_file)
        else:
            logger.error("没有找到匹配的配置文件")
            return

    character_key_mapping = {character: str(i + 1) for i, character in enumerate(characters_on_screen)}
    dead_character_keys = []
    time.sleep(0.4)  # 每个角色动作完成后稍作停顿

    while not stop_event.is_set():
        logger.info("角色按键映射：%s", character_key_mapping)

        # 检查死亡角色并更新死亡角色列表
        dead_index = recognition_dead()
        if dead_index is not None:
            dead_character_keys.append(str(dead_index))
            logger.warning("检测到角色死亡，角色按键：%s", dead_index)

        for character, actions in character_actions:
            character_key = character_key_mapping.get(character)

            if character_key in dead_character_keys:
                logger.warning("跳过死亡角色：%s", character)
                continue

            if character_key and not stop_event.is_set():
                # 检查是否需要切换到钟离
                if zhongli_in_team and time.time() - last_zhongli_time >= 11:
                    zhongli_key = character_key_mapping['钟离']
                    logger.debug(f"尝试切换到钟离，按键：{zhongli_key}")
                    pyautogui.press(zhongli_key)  # 切换到钟离
                    time.sleep(0.1)  # 等待角色切换
                    # 检查切换到钟离是否成功
                    if switch_character(zhongli_key, int(character_key_mapping['钟离'])):
                        perform_action('钟离', 'e(hold)')
                        last_zhongli_time = time.time()
                    else:
                        logger.error(f"切换到钟离失败，按键：{zhongli_key}")
                    time.sleep(0.2)  # 每个角色动作完成后稍作停顿

                # 添加角色切换成功检查
                if switch_character(character_key, int(character_key)):
                    for action in actions:
                        perform_action(character, action)

                    # 更新最后一次钟离技能的时间
                    if character == '钟离' and 'e(hold)' in actions:
                        last_zhongli_time = time.time()

                time.sleep(0.2)  # 每个角色动作完成后稍作停顿
    else:
        stop_event.clear()



def stop():
    stop_event.set()

if __name__ == "__main__":
    time.sleep(3)
    main()
