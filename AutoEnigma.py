import time
from utils import ScreenCompare as Sc, OCR, MouseKey as Mo
from utils.GIautogui import GIautogui as pyautogui
import utils.WhichPage
import Package.log_config
import os
import config
from AutoFight import AutoEnigmaMain as AE

path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
logger = Package.log_config.logger
# 打印当前工作目录
print("AutoEnigma.py:当前工作目录：", os.getcwd())

# BGI_path = Tools.get_variable_value('BGI_path')
file_path = './config/Enigma.txt'


def read_enigma_section(file_path, section_name):
    """读取指定段落中的所有值"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    section_values = []
    found_section = False

    for line in lines:
        line = line.strip()
        if line == section_name:
            found_section = True
            continue

        if found_section:
            if line.startswith('[') and line.endswith(']'):
                break
            section_values.append(line)

    return section_values


def find_enigma_section(file_path):
    """找出 Enigma_now 的值在哪个段落"""
    enigma_now_value = read_enigma_section(file_path, '[Enigma_now]')
    if not enigma_now_value:
        print("秘境名称不存在于列表中，将进行全部查找，这可能导致程序崩溃.")
        return None

    enigma_now_value = enigma_now_value[0]  # 取出 Enigma_now 的值

    sections = {
        'first': '[Enigma_first]',
        'second': '[Enigma_second]',
        'third': '[Enigma_third]'
    }

    for key, section in sections.items():
        section_values = read_enigma_section(file_path, section)
        if enigma_now_value in section_values:
            return key

    return None

def find_if_arrive():
    x1, y1, x2, y2 = 1173,403, 1429,623
    target_found = False

    # 读取 Enigma_now 的值
    enigma_now_value = read_enigma_now_value('./config/Enigma.txt')
    if not enigma_now_value:
        logger.warning("Enigma_now value not found in the config file.")
        return False

    # 尝试找到目标文本
    while not target_found:
        result = OCR.ppocr(x1=x1, x2=x2, y1=y1, y2=y2, model='box and text')
        try:
            for text, coords in result.items():
                if text == enigma_now_value:
                    return True
        except AttributeError:
            return False

        if not target_found:
            return False




def read_enigma_now_value(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    enigma_now_value = None
    found_section = False

    for line in lines:
        line = line.strip()
        if line == '[Enigma_now]':
            found_section = True
            continue

        if found_section:
            if line.startswith('[') and line.endswith(']'):
                break
            enigma_now_value = line
            break

    return enigma_now_value


def find_and_click_enigma_now():
    x1, y1, x2, y2 = 746, 250, 955, 825
    target_found = False

    # 读取 Enigma_now 的值
    enigma_now_value = read_enigma_now_value('./config/Enigma.txt')
    if not enigma_now_value:
        logger.warning("Enigma_now value not found in the config file.")
        return

    # 尝试找到目标文本
    while not target_found:
        result = OCR.ppocr(x1=x1, x2=x2, y1=y1, y2=y2, model='box and text')

        for text, coords in result.items():
            if text == enigma_now_value:
                x2, y2 = coords[2], coords[3]
                target_found = True
                break

        if not target_found:
            # 下滑一个单元
            Mo.click_mouse("left", 0.1, 843, 828)  # 鼠标复位
            time.sleep(0.5)
            Mo.click_mouse('scroll', -200, 1016, 332, times=28)  # 下滚一个单元

    # 如果找到了目标文本，点击其右下角的指定位置
    if target_found:
        click_x = x2 + 680 + 746
        click_y = y2 + 40 + 250
        pyautogui.click(click_x,click_y)
        pyautogui.click(click_x-40,click_y-40)
        logger.info(f'秘境点击{click_x},{click_y}')


def start():
    # 寻找副本逻辑
    result = False
    while not result:
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
    logger.info("识别完成：主界面")
    # 进入游戏，传送至副本
    logger.info('打开冒险之证')
    result = False
    while not result:
        Mo.press_key('F1', 0.1, 3)
        time.sleep(2.5)
        Sc.screenshot_function(229, 706, 359, 786)
        result = Sc.compare_image('./img/mxbook.png', 0.8)
    logger.info('识别成功：冒险之证')
    result = False
    while not result:
        Mo.click_mouse("left", 0.1, 283, 441, 1)  # 点击秘境
        Mo.click_mouse("left", 0.1, 1031, 219, 0.5)  # 点击选择
        result = find_enigma_section(file_path)
        logger.info(result)
        if result == 'first':
            x, y = Sc.CompareWithin('./img/Residue.png')
            if x != 0:
                pyautogui.click(x, y)
        elif result == 'second':
            x, y = Sc.CompareWithin('./img/weapon_en.png')
            if x != 0:
                pyautogui.click(x, y)
        elif result == 'third':
            x, y = Sc.CompareWithin('./img/talent_en.png')
            if x != 0:
                pyautogui.click(x, y)
        else:
            pyautogui.click(1015, 312)
        result = True
        time.sleep(0.5)
    result = False
    find_and_click_enigma_now()

    time.sleep(1)
    Mo.click_mouse("left", 0.1, 1688, 1004)  # 传送
    result = False
    while not result:
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
        time.sleep(0.2)
    logger.info("识别完成：主界面")
    result = find_if_arrive()
    if read_enigma_now_value('./config/Enigma.txt') == '无妄引咎密宫':
        logger.debug('调试01')
        while not result:
            pyautogui.keyDown('a')
            result = find_if_arrive()
        pyautogui.keyUp('a')
    elif read_enigma_now_value('./config/Enigma.txt') == '太山府' or read_enigma_now_value('./config/Enigma.txt')=='芬德尼尔之顶':
        logger.debug('调试02')
        pass

    else:
        while not result:
            logger.debug('调试03')
            pyautogui.keyDown('w')
            result = find_if_arrive()
        pyautogui.keyUp('w')
    print(result)
    logger.info('到达位置，打开程序')
    result = Sc.CompareWithin('img/jiaohu.png')
    if result:
        return True
    else:
        return False


def run():
    # 开始秘境
    AE.main()
    time.sleep(30)
    result = False
    while result == False:
        Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
        time.sleep(5)
    logger.info("识别完成，已经退出秘境")
    Mo.press_key('F11', 0.25)
    return True

def decompose_relics():
    utils.WhichPage.take_to_page('main')
    pyautogui.press('b')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/relics_tag.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(0.5)
    x,y = Sc.CompareWithin('./img/relics.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(2)
    x, y = Sc.CompareWithin('./img/quick_choose.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(1)
    while True:
        x, y = Sc.CompareWithin('./img/syw_2.png')
        if x == 0:
            break
        pyautogui.click(x, y)
    x, y = Sc.CompareWithin('./img/true.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(0.5)
    x, y = Sc.CompareWithin('./img/re_2.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(0.5)
    x, y = Sc.CompareWithin('./img/true_black.png')
    if x != 0:
        pyautogui.click(x, y)
    utils.WhichPage.take_to_page('main')

def back_to_home():
    """返回蒙德"""
    result = False
    while not result:
        Mo.press_key('M', 0.1, 2)
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)
        a = Sc.screenshot_function(1429, 0, 1919, 70)
        a, b = Sc.CompareWithin('./img/map.png', 0.8)
        if a != 0 and b != 0:
            result = True
        time.sleep(5)
    logger.info('识别完成：地图选择')
    result = False
    while not result:
        pyautogui.FAILSAFE = False
        a1, b1 = Sc.CompareWithin('./img/cyjydxkq.png')
        Mo.click_mouse('left', 0.1, a1, b1, 2)  # 层岩巨渊
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)  # 地图选择
        a2, b2 = Sc.CompareWithin('./img/mengde.png')
        Mo.click_mouse('left', 0.1, a2, b2, 2)  # 蒙德
        logger.info('尝试识别：蒙德初始位置')
        time.sleep(3)
        Mo.click_mouse(x=1194, y=615, tick_delay=2)
        Mo.click_mouse("left", 0.1, 1688, 1004, 3)  # 传送
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
        time.sleep(2)
        pyautogui.FAILSAFE = True
    logger.info('识别完成：蒙德初始位置')
    return True
if __name__ == '__main__':
    time.sleep(2)
    start()