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
print("Mission:IrenesFutureKnight.py:当前工作目录：", os.getcwd())

def IrenesFutureKnight():
    time.sleep(3)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(838, 553)
    pydirectinput.moveRel(xOffset=0, yOffset=3000, duration=1, relative=True)
    FindTargrtAndMove.main('./DailyImg/WEITUO2.png')
    pyautogui.press('A')
    pyautogui.keyDown('w')
    time.sleep(1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.press('Ctrl')
    pydirectinput.moveRel(xOffset=0, yOffset=-3000, duration=1, relative=True)
    FindTargrtAndMove.main('./DailyImg/WEITUO2.png')
    time.sleep(1)
    result = False
    times = 0
    while not result:
        x, y = Sc.CompareWithin('./DailyImg/IrenesFutureKnight01.png', notify=False)
        if x != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    pydirectinput.moveRel(xOffset=-1000, yOffset=0, duration=1, relative=True)
    pydirectinput.moveRel(xOffset=-1000, yOffset=0, duration=1, relative=True)
    pyautogui.press('W')
    pydirectinput.moveRel(xOffset=-1000, yOffset=0, duration=1, relative=True)
    pydirectinput.moveRel(xOffset=-1000, yOffset=0, duration=1, relative=True)
    Mo.press_key('E', 3)
    time.sleep(1)
    pyautogui.press('v')
    time.sleep(1)
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        x, y = Sc.CompareWithin('./DailyImg/IrenesFutureKnight01.png', notify=False)
        if x != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
