import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, MouseKey as Mo, AutoOpera
from utils.GIautogui import GIautogui as pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:WineryCleaning2.py:当前工作目录：", os.getcwd())

def WineryCleaning2():
    time.sleep(3)
    pyautogui.press('J')
    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/GoToDes.png')
    c, d = Sc.CompareWithin('./DailyImg/GoToDesCom.png')
    if a != 0 and c == 0:
        pyautogui.click(a, b)
        time.sleep(1)
        pyautogui.press('Esc')
    elif c != 0:
        pyautogui.press('Esc')
        time.sleep(1)
        pyautogui.press('v')
    Package.CalibrateMap.teleport(669,946)
    pyautogui.press('v')
    pydirectinput.moveRel(xOffset=400,yOffset=0,duration=1,relative=True)
    pydirectinput.moveRel(xOffset=0,yOffset=-1000,duration=1,relative=True)
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
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
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    pyautogui.press('SPACE')
    time.sleep(3)
    pyautogui.keyUp('w')
    time.sleep(1)
    result = False
    times = 0
    pyautogui.keyDown('w')
    pyautogui.press('Ctrl')
    time.sleep(5)
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/WineryCleaning01.png')
        times = times + 1
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
        if times > 1000:
            return False
    AutoOpera.auto_opera()
    time.sleep(3)
    pyautogui.press('3')
    pyautogui.press('A')
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    Mo.press_key('e',duration=2)
    time.sleep(8)
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1.5)
    Mo.press_key('e',duration=3)
    time.sleep(8)
    pyautogui.press('W')
    time.sleep(1.5)
    Mo.press_key('e',duration=3)
    time.sleep(8)
    pyautogui.press('D')
    time.sleep(1.5)
    Mo.press_key('e',duration=3)
    time.sleep(8)
    pyautogui.press('D')
    time.sleep(1.5)
    Mo.press_key('e',duration=3)
    time.sleep(8)
    pyautogui.press('W')
    time.sleep(1.5)
    Mo.press_key('e',duration=3)
    time.sleep(3)
    pyautogui.press('v')
    result = FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    if not result:
        return False
    pyautogui.press('W')
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.press('W')
    time.sleep(1)
    pyautogui.press('D')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    result = False
    pyautogui.keyDown('W')
    pyautogui.press('Ctrl')
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/WineryCleaning01.png')
        times = times + 1
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
        if times > 1000:
            return False
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
    return True
