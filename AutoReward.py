import time

from utils import FindTargrtAndMove, ScreenCompare as Sc, WhichPage, MouseKey as Mo
import Package.CalibrateMap
import pydirectinput
from utils.GIautogui import GIautogui as pyautogui
import Package.log_config
import cv2
import numpy as np
import os
import config
from utils.Tools import read_config_value
import pyautogui as pyautogui_real
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)



logger = Package.log_config.logger
def screenshot_function(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    # screen_width, screen_height = pyautogui.size()

    # 截图指定部分
    screenshot = pyautogui_real.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 保存为PNG格式
    cv2.imwrite('screenshot_quit.png', screenshot_cv)

    return screenshot_cv


def str_to_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()  # 去除前后空格并转为小写
        if value in {"true", "yes", "1"}:
            return True
        elif value in {"false", "no", "0"}:
            return False
    raise ValueError(f"Cannot convert {value} to boolean")


def teleport(x, y, xOffset=0, yOffset=0):
    def teleport_to_dirction(x, y, xOffset, yOffset):
        result = False
        pyautogui.press('m')
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
            a2, b2 = Sc.CompareWithin('./img/FengDan.png')
            Mo.click_mouse('left', 0.1, a2, b2, 2)  # 蒙德
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

    teleport_to_dirction(x, y, xOffset, yOffset)
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


def GetReward():
    Package.CalibrateMap.newlife()
    result_use = str_to_bool(read_config_value('./config.txt','AutoDaily','use_experience_point'))
    if result_use:
        pyautogui.press('F1')
        time.sleep(1)
        x, y = Sc.CompareWithin('./img/WeiTuo.png')
        if x != 0:
            pyautogui.click(x, y)
        time.sleep(1)
        x, y = Sc.CompareWithin('./img/getreward.png')
        if x != 0:
            pyautogui.click(x, y)
            time.sleep(1)
            pyautogui.click(800, 800)
        time.sleep(1)
        pyautogui.press('Esc')
    time.sleep(1)
    teleport(962, 537)
    pyautogui.press('Ctrl')
    time.sleep(1)
    FindTargrtAndMove.main('./img/adventure.png')
    FindTargrtAndMove.main('./img/adventure.png')
    time.sleep(1)
    pyautogui.keyDown('w')
    result = False
    while not result:
        x, y = Sc.CompareWithin('./img/KaiSeLin.png')
        if x != 0:
            pyautogui.press('f')
            pyautogui.keyUp('w')
            result = True
    time.sleep(2)
    pyautogui.press('SPACE')
    time.sleep(1.5)
    # 领取每日委托奖励
    x, y = Sc.CompareWithin('./img/icon_daily_reward.png')
    if x != 0:
        pyautogui.click(x, y)
        time.sleep(2)
        pyautogui.press('SPACE')
        time.sleep(3)
        a = 0
        if a == 0:
            pyautogui.click(900, 700)
            time.sleep(2)
            pyautogui.click(900, 700)
            time.sleep(2)
    time.sleep(3)
    pyautogui.press('f')
    time.sleep(2)
    pyautogui.press('SPACE')
    time.sleep(2)
    # 领取探索派遣奖励
    x, y = Sc.CompareWithin('./img/icon_explore.png')
    if x != 0:
        pyautogui.click(x, y)
        time.sleep(2)
        x, y = Sc.CompareWithin('./img/collect.png', 0.92)
        if x != 0:
            pyautogui.click(x, y)
        time.sleep(2)
        x, y = Sc.CompareWithin('./img/re.png', 0.92)
        if x != 0:
            pyautogui.click(x, y)
        time.sleep(1)
        pyautogui.press('Esc')
    else:
        x, y = Sc.CompareWithin('./img/bye.png')
        pyautogui.click(x, y)
    time.sleep(2)
    pyautogui.press('F4')
    time.sleep(2)
    pyautogui.click(960, 42)
    time.sleep(0.5)
    x, y = Sc.CompareWithin('./img/getAll.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(3)
    pyautogui.click(862, 33)
    time.sleep(1)
    pyautogui.click(862, 33)
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/getAll.png')
    if x != 0:
        pyautogui.click(x, y)
        time.sleep(1)
        pyautogui.click(900, 800)
    time.sleep(3)
    pyautogui.press('Esc')
    time.sleep(2)
    pyautogui.press('Esc')
    time.sleep(2)
    x, y = Sc.CompareWithin('./img/email.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(2)
    x, y = Sc.CompareWithin('./img/collect.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(942, 939)
    time.sleep(1)
    pyautogui.press('Esc')
    time.sleep(1)
    pyautogui.press('Esc')

if __name__ == '__main__':
    GetReward()