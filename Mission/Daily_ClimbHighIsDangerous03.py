import time
import utils.auto_fight_threading
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, MouseKey
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:ClimbHighIsDangerous03.py:当前工作目录：", os.getcwd())

def ClimbHighIsDangerous03():
    time.sleep(4)
    Package.CalibrateMap.teleport(1494,576,0,-800)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous06.png')
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
    result = False
    times = 0
    pyautogui.keyDown('w')
    while not result:
        if times % 2 == 0 and times < 18:
            pyautogui.press('SPACE')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
            if times % 10 == 0:
                MouseKey.press_key('e', 3)
            pyautogui.press('A')
        a, b = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous05.png')
        if a != 0:
            result = True
        times = times + 1
        if times > 500:
            return False
    time.sleep(3)
    pyautogui.keyUp('w')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    times = 3
    while times < 140:
        times = times + 1
        time.sleep(0.2)
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png')
        if a != 0:
            times = 200
        if times % 4 == 0:
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
            pyautogui.keyDown('w')
            pyautogui.press('A')
        if times > 135:
            return False
        time.sleep(0.4)
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    pyautogui.keyUp('w')
    Package.CalibrateMap.newlife()
    return True