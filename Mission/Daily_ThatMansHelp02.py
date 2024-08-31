import time
import utils.auto_fight_threading
from utils import ScreenCompare as Sc, AutoOpera
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pydirectinput
from utils.GIautogui import GIautogui as pyautogui
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:ThatMansHelp.py:当前工作目录：", os.getcwd())

def daily_thatmanshelp():
    time.sleep(3)

    pyautogui.moveTo(1700,540)
    pydirectinput.moveTo(1700,540)
    pydirectinput.moveRel(xOffset=-1100,yOffset=0,duration=1,relative=True)
    time.sleep(0.5)
    pyautogui.keyDown('W')
    time.sleep(1)
    pydirectinput.press('SPACE')
    time.sleep(2)
    pydirectinput.moveRel(xOffset=400,yOffset=0,duration=1,relative=True)
    time.sleep(3)
    pyautogui.click(500,500)
    time.sleep(2)
    pyautogui.press('Ctrl')
    result = False
    while not result:
        x, y = Sc.CompareWithin('./DailyImg/ThatMansHelp01.png', 0.8,notify=False)
        if x != 0:
            result = True
    pyautogui.press('F')
    pyautogui.keyUp('W')
    AutoOpera.auto_opera()
    Package.CalibrateMap.teleport(1197,618)
    pydirectinput.moveRel(xOffset=1050,yOffset=0,duration=1,relative=True)
    pyautogui.keyDown('W')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ThatMansHelp03.png', sim_num=0.6, notify=False)
        pyautogui.press('SPACE')
        time.sleep(1)
        if a != 0:
            result = True
    time.sleep(1)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    pyautogui.keyUp('W')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ThatMansHelp04.png')
        if a != 0:
            result = True
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    pyautogui.press('4')
    Package.CalibrateMap.teleport(838,553)
    pyautogui.moveTo(1700,540)
    pydirectinput.moveTo(1700,540)
    pydirectinput.moveRel(xOffset=-1100,yOffset=0,duration=1,relative=True)
    time.sleep(0.5)
    pyautogui.keyDown('W')
    time.sleep(1)
    pydirectinput.press('SPACE')
    time.sleep(2)
    pydirectinput.moveRel(xOffset=400,yOffset=0,duration=1,relative=True)
    time.sleep(3)
    pyautogui.click(500,500)
    time.sleep(2)
    pyautogui.press('Ctrl')
    result = False
    while not result:
        x, y = Sc.CompareWithin('./DailyImg/ThatMansHelp01.png', 0.8,notify=False)
        if x != 0:
            result = True
    pyautogui.press('F')
    pyautogui.keyUp('W')
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
    return True