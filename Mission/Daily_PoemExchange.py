import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:PoemExchange.py:当前工作目录：", os.getcwd())

def PoemExchange01():
    time.sleep(3)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./DailyImg/PoemExchange01.png',0.9)
    if a != 0:
        pyautogui.click(a, b)
    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/GoToDes.png')
    c, d = Sc.CompareWithin('./DailyImg/GoToDesCom.png')
    if a != 0 and c == 0:
        pyautogui.click(a, b)
        time.sleep(1)
    elif c != 0:
        time.sleep(1)
        pyautogui.press('v')
    c, d = Sc.CompareWithin('./img/mjend.png')
    if c == 0:
        pyautogui.press('Esc')
    time.sleep(1)
    Package.CalibrateMap.teleport(1696,647)
    pyautogui.keyDown('s')
    time.sleep(1)
    pyautogui.keyUp('s')
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        pyautogui.press('SPACE')
        a, b = Sc.CompareWithin('./DailyImg/PoemExchange02.png')
        if times % 4 == 0 and times < 12:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
        if a != 0:
            result = True
        time.sleep(0.8)
        if times > 135:
            return False
    pyautogui.keyUp('w')
    pyautogui.press('Ctrl')
    time.sleep(1)
    pyautogui.keyDown('w')
    result = False
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/PoemExchange03.png',0.55)
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
        if a != 0:
            result = True
        time.sleep(0.6)
        if times > 200:
            return False
    pyautogui.press('f')
    pyautogui.keyUp('w')
    AutoOpera.auto_opera()
