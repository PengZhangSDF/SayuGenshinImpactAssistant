import time
import utils.ScreenCompare as Sc
from utils.GIautogui import GIautogui as pyautogui_Mo
import pyautogui
import config
import os
import cv2
import numpy as np
import Package.CalibrateMap
import AutoEnigma
import Package.log_config
import threading
from AutoFight import AutoFightConfig
from utils.OCR import ppocr
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
stop_event = threading.Event()
logger = Package.log_config.logger
def is_grayscale_region_present(x1, y1, x2, y2, saturation_threshold=0.12, area_threshold=0.77):
    # 截取屏幕指定区域
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
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
def autofight():
    AutoFightConfig.main()

def wait_screen(path_to_img,timesmax = 200):
    x, y = Sc.CompareWithin_Continue(path_to_img, timesmax=timesmax)
    return x, y


def go_into_enigma():
    time.sleep(1)
    pyautogui_Mo.press('f')  # 点击秘境
    x, y = wait_screen('./img/true.png')  # 单人挑战
    if x != 0:
        time.sleep(0.5)
        pyautogui_Mo.click(x, y)
    time.sleep(1)
    x, y = wait_screen('./img/true.png')  # 开始挑战
    if x != 0:
        time.sleep(0.5)
        pyautogui_Mo.click(x, y)
    a, b = Sc.CompareWithin('./img/true.png')  # 可能出现的额外的确认
    if a != 0:
        time.sleep(0.5)
        pyautogui_Mo.click(a, b)


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
    if dead:
        logger.warning('存在角色死亡')
        logger.warning(f'死亡角色：{dead_character}号角色')
        Package.CalibrateMap.newlife()
        AutoEnigma.start()
        go_into_enigma()
        x, y = wait_screen('./img/Enigma_close.png')  # 秘境提示点击
        if x != 0:
            time.sleep(0.5)
            pyautogui_Mo.click(x, y)

def recognition_dead02():
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
        return False
    if dead:
        logger.warning('存在角色死亡')
        logger.warning(f'死亡角色：{dead_character}号角色')
        return True
def fight_in_Enigma(times):
    x, y = wait_screen('./img/Enigma_close.png')  # 秘境提示点击
    if x != 0:
        time.sleep(0.5)
        pyautogui_Mo.click(x, y)
    time.sleep(1)
    recognition_dead()
    time.sleep(0.5)
    pyautogui_Mo.keyDown('w')
    while True:
        result = ppocr(1105,524,1131,550,model='all')
        if'F' in result or result == ['F']:
            x=1
            pyautogui_Mo.press('f')
            break
    logger.info('检测到交互键')
    if x != 0:
        pyautogui_Mo.press('f')
    if x != 0:
        pyautogui_Mo.press('f')
        pyautogui_Mo.keyUp('w')
        main_thread = threading.Thread(target=autofight)
        main_thread.start()
        # 等待结束停止AutoFight线程
        from AutoFight import FindTreeMain  # 我劝你别在10秒内打完！！！！！
        while True:
            x, y = Sc.CompareWithin('./img/successful.png')
            result = ppocr(801,240,1128,335,model='all')

            if result == ['挑战失败']:
                # 队伍全部阵亡，停止自动战斗并返回错误
                logger.error("错误代码AF001：队伍全部阵亡")
                AutoFightConfig.stop()
                logger.info('停止自动战斗')
                main_thread.join()
                stop_event.clear()
                logger.info("自动战斗已停止")
                return 'E:AF001'
            if x != 0:
                break
        logger.info('检测到挑战成功')
        if x != 0:
            AutoFightConfig.stop()
            logger.info('停止自动战斗')

        # 等待主线程结束
        main_thread.join()
        stop_event.clear()
        logger.info("自动战斗已停止")
        time.sleep(3)
        pyautogui_Mo.click(button='MIDDLE')
        FindTreeMain.main_threading()

        # 走到古化石树
        pyautogui_Mo.keyDown('w')
        time.sleep(0.35)
        pyautogui_Mo.keyDown('shift')
        while True:
            result = ppocr(1105, 524, 1131, 550, model='all')
            if 'F' in result or result == ['F']:
                x = 1
                pyautogui_Mo.press('f')
                break
        if x != 0:
            pyautogui_Mo.press('f')
            pyautogui_Mo.keyUp('shift')
        time.sleep(1)
        a, b = Sc.CompareWithin('./img/shuzhi.png')
        if a != 0:
            pyautogui_Mo.click(a, b)
            time.sleep(1)
            logger.info('优先使用树脂')
            shuzhi = True
        else:
            logger.info('没有浓缩树脂了！')
            shuzhi = False
        for _ in range(10):
            pyautogui_Mo.click(1847, 36)
            time.sleep(0.25)
        x1, y1 = wait_screen('./img/true.png')
        time.sleep(1)
        result = ppocr(1200, 916, 1250, 952, model='int')
        try:
            result_num = int(result[0])
        except (IndexError, TypeError):
            result_num = 0

        if isinstance(result_num, int):
            pass
        else:
            if isinstance(result, list) and isinstance(result[0], str) and '没有文本' in result[0]:
                logger.error(f"Error: {result[0]}，这个错误并不致命，只是OCR识别识别导致可能的秘境运行停止")
                if shuzhi:
                    result_num = 20
                else:
                    result_num = 0
            elif shuzhi:
                result_num = 20
            else:
                result_num = 0

        if result_num  >= 20:
            pyautogui_Mo.click(x1, y1)
            finish = False
        else:
            a, b = Sc.CompareWithin('./img/cancel.png')
            logger.info('没有体力了！自动秘境结束')
            pyautogui_Mo.click(a, b)
            finish = True
        return finish

def main():
    if recognition_dead02():
        logger.warning('存在角色死亡')
        Package.CalibrateMap.newlife()
        AutoEnigma.start()
    go_into_enigma()
    times = 1
    finish = fight_in_Enigma(times)
    if finish == 'E:AF001':
        x, y = Sc.CompareWithin('./img/true.png')
        if x != 0:
            pyautogui_Mo.click(x, y)
            Sc.CompareWithin_Continue('./img/mjend2.png')
            AutoEnigma.start()
            go_into_enigma()

    while not finish:
        times = times + 1
        finish = fight_in_Enigma(times)
        if finish == 'E:AF001':
            x, y = Sc.CompareWithin('./img/true.png')
            if x != 0:
                pyautogui_Mo.click(x, y)
                Sc.CompareWithin_Continue('./img/mjend2.png')
                AutoEnigma.start()
                go_into_enigma()
    logger.info('自动秘境结束')



if __name__ == '__main__':
    time.sleep(2)
    main()
