import time
import utils.auto_fight_threading
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, MouseKey as Mo, AutoOpera
import pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:RoundBigRush.py:当前工作目录：", os.getcwd())

def RoundBigrush01():
    time.sleep(5)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(960, 543)
    Package.CalibrateMap.teleport(960, 543)
    pyautogui.press('J')

    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/MissionRoundBigRush02.png')
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
    pyautogui.press('D')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    time.sleep(8)
    pyautogui.keyUp('w')
    pyautogui.press('v')
    a,b = Sc.CompareWithin('./DailyImg/notify01.png')
    if a != 0:
        pyautogui.keyDown('d')
        time.sleep(1.5)
        pyautogui.keyUp('d')
        pyautogui.keyDown('w')
        time.sleep(7)
        pyautogui.keyUp('w')

    if a == 0:
        FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        pyautogui.keyDown('d')
        time.sleep(1.5)
        pyautogui.keyUp('d')
        pyautogui.press('v')
        FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        pyautogui.keyDown('w')
        time.sleep(7)
        pyautogui.keyUp('w')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/MissionRoundBigRush03.png')
        if a != 0:
            result = True
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    time.sleep(0.5)
    pydirectinput.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/MissionRoundBigRush04.png')
        times = times + 1
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
        if times > 150:
            return False
    AutoOpera.auto_opera()
    pyautogui.press('4')
    Package.CalibrateMap.teleport(529,251)
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    time.sleep(9.5)
    pyautogui.press('SPACE')
    result = False
    times = 0
    while not result:
        pyautogui.press('v')
        a, b = Sc.CompareWithin('./DailyImg/MissionRoundBigRush05.png',sim_num=0.65)
        if a != 0:
            result = True
        times = times + 1
        if times > 1500:
            return False
    time.sleep(4)
    pyautogui.keyUp('w')
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/MissionRoundBigRush06.png',0.8)
        c, d = Sc.CompareWithin('./DailyImg/MissionRoundBigRush07.png',0.8)
        if a != 0 and c == 0:
            result = True
    time.sleep(5)
    pyautogui.keyUp('w')
    pyautogui.press('3')
    time.sleep(0.3)
    Mo.press_key('E',3)
    pyautogui.press('Ctrl')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png')
        times = times + 1
        if a != 0:
            result = True
        if times > 1000:
            utils.auto_fight_threading.stop_auto_fight_config()
            auto_fight_threading.join()
            return False
    return True