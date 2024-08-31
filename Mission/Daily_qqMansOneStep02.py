import Package.CalibrateMap
from utils import ScreenCompare as Sc
import utils.auto_fight_threading
import time
from utils.GIautogui import GIautogui as pyautogui
from utils.GIautogui import GIautogui as pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:qqMansOneStep02.py:当前工作目录：", os.getcwd())


def qqmansonestep02():
    times = 0
    time.sleep(5)
    Package.CalibrateMap.teleport(482, 570, 1000, 500)
    pydirectinput.moveRel(xOffset=-1800, yOffset=0, duration=1, relative=True)
    time.sleep(1)
    pyautogui.keyDown('W')
    time.sleep(2)
    pydirectinput.moveRel(xOffset=200, yOffset=0, duration=1, relative=True)
    result = False
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep01.png', sim_num=0.6, notify=False)
        if a != 0:
            result = True
        if times > 1000:
            return False
        time.sleep(1)
        pyautogui.press('SPACE')
    time.sleep(4)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    pyautogui.keyUp('W')
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png', notify=False)
        times = times + 1
        if a != 0:
            result = True
        if times > 1000:
            return False
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    Package.CalibrateMap.newlife()
    return True
