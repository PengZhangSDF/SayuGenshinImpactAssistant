import time
import utils.auto_fight_threading
from utils import ScreenCompare as Sc, MouseKey as Mo, AutoOpera
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pydirectinput
from utils.GIautogui import GIautogui as pyautogui
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:TheWayWoReward.py:当前工作目录：", os.getcwd())


# 委托名称：报答神明的方式
def the_way_to_reward():
    time.sleep(3)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(838,553)
    pyautogui.moveTo(1700,540)
    pydirectinput.moveTo(1700,540)
    pydirectinput.moveRel(xOffset=-1100,yOffset=0,duration=1,relative=True)
    time.sleep(0.5)
    pyautogui.keyDown('W')
    time.sleep(1)
    pydirectinput.press('SPACE')
    time.sleep(10)
    pydirectinput.moveRel(xOffset=300,yOffset=0,duration=1,relative=True)
    time.sleep(5)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(2)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(2)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(4)
    pydirectinput.moveRel(xOffset=200,yOffset=0,duration=1,relative=True)
    result = False
    times = 0
    while not result:
        x,y = Sc.CompareWithin('./DailyImg/TheWayToReward01.png',notify=False)
        if x!=0:
            result = True
        times = times + 1
        if times > 1000:
            return False
    pyautogui.keyUp('W')
    Mo.press_key('F',0.1)
    time.sleep(5) # 进入教堂
    pydirectinput.moveRel(xOffset=80,yOffset=0,duration=1,relative=True)
    pyautogui.keyDown('W')
    result = False
    times = 0
    while not result:
        pyautogui.press('SPACE')
        x,y = Sc.CompareWithin('./DailyImg/TheWayToReward02.png',notify=False)
        if x!=0:
            result = True
        times = times + 1
        if times > 1000:
            return False
    pyautogui.press('F')
    pyautogui.keyUp('W')
    pyautogui.press('F')
    time.sleep(3)
    result = False
    while not result:
        result = AutoOpera.auto_opera()
    Package.CalibrateMap.teleport(673,942)
    pyautogui.press('3')
    time.sleep(0.5)
    pyautogui.press('E')
    time.sleep(0.5)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    times = 0
    while not result:
        times = times + 1
        time.sleep(10)
        pyautogui.press('J')
        time.sleep(1)
        result = Sc.CompareWithin('./DailyImg/TheWayToReward03.png',notify=False)
        if result:
            utils.auto_fight_threading.stop_auto_fight_config()
            auto_fight_threading.join()
        pyautogui.press('Esc')
        if times > 10:
            return False
    time.sleep(3)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(838,553)
    pyautogui.moveTo(1700,540)
    pydirectinput.moveTo(1700,540)
    pydirectinput.moveRel(xOffset=-1100,yOffset=0,duration=1,relative=True)
    time.sleep(0.5)
    pyautogui.keyDown('W')
    time.sleep(1)
    pydirectinput.press('SPACE')
    time.sleep(10)
    pydirectinput.moveRel(xOffset=300,yOffset=0,duration=1,relative=True)
    time.sleep(5)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(2)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(2)
    pydirectinput.moveRel(xOffset=-300,yOffset=0,duration=1,relative=True)
    time.sleep(4)
    pydirectinput.moveRel(xOffset=200,yOffset=0,duration=1,relative=True)
    result = False
    times = 0
    while not result:
        x,y = Sc.CompareWithin('./DailyImg/TheWayToReward01.png',notify=False)
        times = times + 1
        if x!=0:
            result = True
        if times > 1000:
            return False
    pyautogui.keyUp('W')
    Mo.press_key('F',0.1)
    time.sleep(5) # 进入教堂
    pydirectinput.moveRel(xOffset=80,yOffset=0,duration=1,relative=True)
    pyautogui.keyDown('W')
    result = False
    times = 0
    while not result:
        pyautogui.press('SPACE')
        times = times + 1
        x,y = Sc.CompareWithin('./DailyImg/TheWayToReward02.png',notify=False)
        if x != 0:
            result = True
        if times>1000:
            return False
    pyautogui.press('F')
    pyautogui.keyUp('W')
    pyautogui.press('F')
    time.sleep(3)
    result = False
    while not result:
        result = AutoOpera.auto_opera()
    time.sleep(5)
    Package.CalibrateMap.newlife()
    return True


