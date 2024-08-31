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
print("Mission:ClimbHighIsDangerous01.py:当前工作目录：", os.getcwd())

def ClimbHighIsDangerous():
    time.sleep(3)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(0.8)
    a, b = Sc.CompareWithin('./img/HomeOfDaily.png',0.6)
    if a != 0:
        pyautogui.click(a,b)
    a, b = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous02.png')
    time.sleep(0.2)
    if a != 0:
        pyautogui.click(a,b)
    c, d = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous03.png')
    time.sleep(0.2)
    if d == 0:
        return False
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
    time.sleep(1 )
    Package.CalibrateMap.teleport(1322,863)
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    time.sleep(10)
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ClimbHighIsDangerous04.png')
        times = times + 1
        if a != 0:
            result = True
        if times > 1000:
            return False
        time.sleep(1)
        pyautogui.press('SPACE')
    time.sleep(1)
    pyautogui.press('SPACE')
    time.sleep(1)
    pyautogui.press('SPACE')
    time.sleep(7)
    pyautogui.keyUp('w')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    times = 3
    while times < 120:
        times = times + 1
        time.sleep(0.2)
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png')
        if a != 0:
            times = 200
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
            pyautogui.press('A')
        if times % 10 == 0:
            MouseKey.press_key('e', 3)
        time.sleep(0.4)
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    if times != 200:
        FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        pyautogui.keyDown('w')
        time.sleep(4)
        pyautogui.keyUp('w')
        utils.auto_fight_threading.stop_auto_fight_config()
        auto_fight_threading.join()
        result = False
        times = 0
        while not result:
            times = times + 1
            time.sleep(0.4)
            a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png')
            if a != 0:
                result = True
            if times > 500:
                return False
            time.sleep(0.4)
    Package.CalibrateMap.newlife()
    return True


if __name__ == '__main__':
    ClimbHighIsDangerous()