import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
from utils.GIautogui import GIautogui as pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:NoOneNoticeGY.py:当前工作目录：", os.getcwd())

def NoOneNoticeGY():
    time.sleep(3)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./img/NoOneNoticeGY01.png',0.9)
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
    Package.CalibrateMap.teleport(960,538)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    pyautogui.keyDown('w')
    time.sleep(8.5)
    pyautogui.keyUp('w')
    time.sleep(0.5)
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0 and times <= 12:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
        a, b = Sc.CompareWithin('./DailyImg/NoOneNoticeGY01.png',0.7)
        time.sleep(0.8)
        times = times + 1
        if a != 0:
            result = True
            pyautogui.keyUp('w')
        if times > 120:
            return False
    result = False
    pyautogui.press('f')
    AutoOpera.auto_opera()

    Package.CalibrateMap.teleport(669,946)
    pyautogui.press('v')
    pyautogui.press('v')
    pydirectinput.moveRel(xOffset=400,yOffset=0,duration=1,relative=True)
    pydirectinput.moveRel(xOffset=0,yOffset=-1000,duration=1,relative=True)
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.keyDown('w')
    time.sleep(18.5)
    pyautogui.press('SPACE')
    time.sleep(0.8)
    pyautogui.press('SPACE')
    time.sleep(4)
    pyautogui.keyDown('d')
    time.sleep(2)
    pyautogui.press('SPACE')
    time.sleep(2)
    pyautogui.press('SPACE')
    time.sleep(2)
    pyautogui.press('SPACE')
    pyautogui.keyUp('d')
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.keyDown('d')
    time.sleep(1)
    pyautogui.press('SPACE')
    time.sleep(1)
    pyautogui.press('SPACE')
    time.sleep(1)
    pyautogui.press('SPACE')
    pyautogui.keyUp('d')
    time.sleep(5)
    pyautogui.keyUp('w')
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        a,b = Sc.CompareWithin('./DailyImg/FatherCanDo02.png')
        times = times + 1
        if a != 0:
            pyautogui.press('f')
            pyautogui.keyUp('w')
            result = True
        if times > 1000:
            return False
    AutoOpera.auto_opera()