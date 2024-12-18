import Package.CalibrateMap
import utils.auto_fight_threading
import time
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:RoadIsBlock01.py:当前工作目录：", os.getcwd())

def TheRoadIsBlock():
    time.sleep(4)
    Package.CalibrateMap.teleport(672,937)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./img/RoadIsBlock.png')
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
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/TheRoadIsBlock01.png', sim_num=0.6, notify=False)
        if a != 0:
            result = True
        if times > 500:
            return False
        if times % 2 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        if times %8 == 0:
            pyautogui.press('x')
        pyautogui.press('SPACE')
    time.sleep(4)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    pyautogui.keyUp('w')
    result = False
    times = 0
    while not result:
        a,b = Sc.CompareWithin('./DailyImg/WeiTuo3.png',notify=False)
        times = times + 1
        if a != 0:
            result = True
        if times > 500:
            return False
        pyautogui.press('v')
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    times = 0
    result = False
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/TheRoadIsBlock02.png', notify=False)
        if a != 0:
            result = True
        if times >= 300:
            return False
    pyautogui.press('f')
    pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
    return True



