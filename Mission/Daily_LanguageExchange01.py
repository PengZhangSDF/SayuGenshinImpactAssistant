import time
import utils.auto_fight_threading
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:LanguageExchange01.py:当前工作目录：", os.getcwd())

def LanguageExchange01():
    time.sleep(3)
    pyautogui.press('4')
    pyautogui.press('j')
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
    Package.CalibrateMap.teleport(1608,333)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/LanguageExchange03.png')
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/LanguageExchange03.png')
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    time.sleep(10)
    pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    time.sleep(5)
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/zhuizong.png')
        if a != 0:
            result = True
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/LanguageExchange03.png')
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
