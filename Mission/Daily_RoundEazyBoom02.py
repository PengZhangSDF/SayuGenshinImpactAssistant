import Package.CalibrateMap

import time
import utils.auto_fight_threading
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:RoundEazyBoom02.py:当前工作目录：", os.getcwd())

def RoundEazyBoom02():
    time.sleep(4)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./DailyImg/RoundEazyBoom02.png')
    if a != 0:
        pyautogui.click(a, b)
    a, b = Sc.CompareWithin('./DailyImg/GoToDes.png')
    c, d = Sc.CompareWithin('./DailyImg/GoToDesCom.png')
    if a != 0 and c == 0:
        pyautogui.click(a, b)
        time.sleep(1)
    elif c != 0:
        pyautogui.press('Esc')
        time.sleep(1)
        pyautogui.press('v')
    time.sleep(1)
    c, d = Sc.CompareWithin('./img/mjend.png')
    if c == 0:
        pyautogui.press('Esc')
    pyautogui.press('4')
    Package.CalibrateMap.teleport(1330,869)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    result = False
    times = -1
    while not result:
        pyautogui.press('SPACE')
        times = times + 1
        if times % 6 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        a, b = Sc.CompareWithin('./DailyImg/RoundEazyBoom03.png')
        if a != 0:
            result = True
        time.sleep(0.6)
    time.sleep(5)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    pyautogui.keyUp('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        a,b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png',notify=False)
        if times > 1000:
            return False
        if a != 0:
            result = True
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    time.sleep(1)
    Package.CalibrateMap.newlife()
    return True