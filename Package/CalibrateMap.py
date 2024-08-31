from utils import ScreenCompare as Sc, WhichPage, MouseKey as Mo

from utils.GIautogui import GIautogui as pyautogui
import time
from utils.GIautogui import GIautogui as pydirectinput
import os
import config
import Package.log_config
logger = Package.log_config.logger
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Package.CalibrateMap.py:当前工作目录：", os.getcwd())
def newlife():
    result = False
    def teleport_newlife():
        Mo.press_key('m', 0.1)
        time.sleep(2)
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)
        a = Sc.screenshot_function(1429, 0, 1919, 70)
        a, b = Sc.CompareWithin('./img/map.png', 0.8)
        if a != 0:
            pass
        else:
            Mo.click_mouse('left', 0.1, 1847, 1016, 2)
        pyautogui.FAILSAFE = False
        a1, b1 = Sc.CompareWithin('./img/cyjydxkq.png')
        Mo.click_mouse('left', 0.1, a1, b1, 2)  # 层岩巨渊
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)  # 地图选择
        a2, b2 = Sc.CompareWithin('./img/mengde.png')
        Mo.click_mouse('left', 0.1, a2, b2, 2)  # 蒙德
        time.sleep(1)
        Mo.click_mouse(x=1331, y=868, tick_delay=2)
        Mo.click_mouse("left", 0.1, 1692, 1008, 3)  # 传送
        pyautogui.FAILSAFE = True
    teleport_newlife()
    page = WhichPage.which_page()
    result = False
    times = 0
    while not result:
        times = times + 1
        Sc.screenshot_function(36, 28, 76, 78)
        result = Sc.compare_image('./img/mjend2.png')
        if times > 60:
            WhichPage.take_to_page('main')
            time.sleep(0.5)
            teleport_newlife()
            times = 0
    pyautogui.keyDown('s')
    time.sleep(1.2)
    pyautogui.keyUp('s')
    time.sleep(1.8)
    return True

def teleport(x, y,xOffset=0,yOffset=0):
    def teleport_to_dirction(x, y, xOffset, yOffset):
        result = False
        Mo.press_key('M', 0.1)
        time.sleep(2)
        if not result:
            Mo.click_mouse('left', 0.1, 1847, 1016, 2)
            a = Sc.screenshot_function(1429, 0, 1919, 70)
            a, b = Sc.CompareWithin('./img/map.png', 0.8)
            if a != 0:
                pass
            else:
                Mo.click_mouse('left', 0.1, 1847, 1016, 2)
            pyautogui.FAILSAFE = False
            time.sleep(0.2)
            a1, b1 = Sc.CompareWithin('./img/cyjydxkq.png')
            Mo.click_mouse('left', 0.1, a1, b1, 2)  # 层岩巨渊
            time.sleep(0.2)
            Mo.click_mouse('left', 0.1, 1847, 1016, 2)  # 地图选择
            time.sleep(0.2)
            a2, b2 = Sc.CompareWithin('./img/mengde.png')
            Mo.click_mouse('left', 0.1, a2, b2, 2)  # 蒙德
            logger.info('尝试识别：蒙德初始位置')
            pydirectinput.moveTo(800, 500)
            if xOffset != 0 or yOffset != 0:
                if xOffset >= 0 and yOffset >= 0:
                    pyautogui.moveTo(500, 100)
                elif xOffset <= 0 <= yOffset:
                    pyautogui.moveTo(1500, 100)
                elif xOffset <= 0 and yOffset <= 0:
                    pyautogui.moveTo(1500, 1000)
                elif xOffset >= 0 >= yOffset:
                    pyautogui.moveTo(500, 1000)
                Mo.drag_mouse('left', xOffset)
                Mo.drag_mouse('up', yOffset)
            time.sleep(1)
            Mo.click_mouse(x=x, y=y, tick_delay=2)
            x1, y1 = Sc.CompareWithin('./img/TeleportPoint.png')
            x2, y2 = Sc.CompareWithin('./img/TeleportPoint2.png')
            x3, y3 = Sc.CompareWithin('./img/TeleportPoint3.png')
            x4, y4 = Sc.CompareWithin('./img/teleport.png')
            if x1 != 0 or x2 != 0 or x3 != 0 and x4 == 0:
                if x1 != 0:
                    Mo.click_mouse(x=x1, y=y1)
                elif x2 != 0 and x1 == 0:
                    Mo.click_mouse(x=x2, y=y2)
                elif x3 != 0 and x1 == 0:
                    Mo.click_mouse(x=x3, y=y3)
                time.sleep(1)
            Mo.click_mouse("left", 0.1, 1692, 1008, 3)  # 传送

    teleport_to_dirction(x,y,xOffset,yOffset)
    result = False
    times = 0
    while not result:
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
        time.sleep(0.5)
        times = times + 1
        if times > 70:
            WhichPage.take_to_page('main')
            times = 0
            teleport_to_dirction(x, y, xOffset, yOffset)
    time.sleep(3)
    pyautogui.FAILSAFE = True
    return True


def open_map():
    result = False
    Mo.press_key('M', 0.1)
    time.sleep(2)
    while not result:
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)
        a = Sc.screenshot_function(1429, 0, 1919, 70)
        a, b = Sc.CompareWithin('./img/map.png', 0.8)
        if a != 0:
            pass
        else:
            Mo.click_mouse('left', 0.1, 1847, 1016, 2)
        pyautogui.FAILSAFE = False
        a1, b1 = Sc.CompareWithin('./img/cyjydxkq.png')
        Mo.click_mouse('left', 0.1, a1, b1, 2)  # 层岩巨渊
        Mo.click_mouse('left', 0.1, 1847, 1016, 2)  # 地图选择
        a2, b2 = Sc.CompareWithin('./img/mengde.png')
        Mo.click_mouse('left', 0.1, a2, b2, 2)  # 蒙德
        result = True
    return True
