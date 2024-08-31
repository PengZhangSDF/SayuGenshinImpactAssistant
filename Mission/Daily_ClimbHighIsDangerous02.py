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
print("Mission:ClimbHighIsDangerous02.py:当前工作目录：", os.getcwd())

def ClimbHighIsDangerous02():
    time.sleep(4)
    Package.CalibrateMap.teleport(350,557)
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
    key = 0
    pyautogui.keyDown('w')
    while not result:
        if times % 2 == 0 and times < 18:
            pyautogui.press('SPACE')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
            pyautogui.press('A')
        a, b = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous05.png')
        c, d = Sc.CompareWithin('./DailyImg/KeyIsEasyToLose01.png',0.5)
        if a != 0:
            result = True
        if c != 0 and key == 0:
            for i in range(1,12):
                time.sleep(0.2)
                pyautogui.press('v')
                pyautogui.press('SPACE')
                time.sleep(0.6)
                if i > 5:
                    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
                if i == 6:
                    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
            result = True
        if times > 500:
            return False
        time.sleep(0.3)
        time.sleep(0.4)
        times = times + 1
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png', notify=False)
        times = times + 1
        if a != 0:
            result = True
        if times > 500:
            return False
    utils.auto_fight_threading.stop_auto_fight_config()
    try:
        auto_fight_threading.join()
    except:
        pass
    Package.CalibrateMap.newlife()
    return True
