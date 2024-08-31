import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, MouseKey as Mo, AutoOpera
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:MengDeBeerPeople.py:当前工作目录：", os.getcwd())

def MengDeBeerPeople():
    time.sleep(3)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./img/MengDeBeerPeople02.png',0.9)
    if a != 0:
        pyautogui.click(a, b)
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
    Package.CalibrateMap.teleport(960,538)
    pyautogui.keyDown('w')
    time.sleep(3)
    pyautogui.keyUp('w')
    FindTargrtAndMove.main('./DailyImg/WeiTuo5.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0 and times <= 12:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo5.png')
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople01.png',0.7)
        time.sleep(0.8)
        pyautogui.press('x')
        times = times + 1
        pyautogui.press('SPACE')
        if times > 210:
            return False
        if a != 0:
            result = True
            pyautogui.keyUp('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople01.png',0.7 )
        g, h = Sc.CompareWithin('./DailyImg/MengDeBeerPeople04.png',0.7)
        e, f = Sc.CompareWithin('./DailyImg/MengDeBeerPeople03.png',0.7)
        if a != 0 and g == 0 :
            pyautogui.press('f')
            time.sleep(1)
            x, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople07.png', 0.7)
            if x == 0:
                result = True
            else:
                AutoOpera.auto_opera()
                times = 0
        if times < 10:
            Mo.press_key('a',0.1)
        if times > 10:
            Mo.press_key('d', 0.1)
        if times > 210:
            return False


    pyautogui.press('f')
    result = False
    while not result:
        time.sleep(0.5)
        a, b = Sc.CompareWithin('./img/mjend.png')
        if a != 0:
            result = True
    pyautogui.keyUp('w')
    time.sleep(2)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo4.png')
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople02.png',0.65)
        if times == 12 or times == 48:
            pyautogui.press('SPACE')
            time.sleep(0.7)
            pyautogui.press('SPACE')
            time.sleep(0.7)
            pyautogui.press('SPACE')
        time.sleep(0.3)
        times = times + 1
        if times > 210:
            return False
        if a != 0:
            result = True
            pyautogui.keyUp('w')
    pyautogui.keyUp('w')
    pyautogui.press('f')
    AutoOpera.auto_opera()

    Package.CalibrateMap.teleport(960,538)
    pyautogui.keyDown('w')
    time.sleep(10)
    pyautogui.keyUp('w')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0 and times <= 12:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople05.png',0.64)
        time.sleep(0.8)
        pyautogui.press('x')
        times = times + 1
        if times > 210:
            return False
        if times % 4 == 0:
            pyautogui.press('SPACE')
        if a != 0:
            result = True
            pyautogui.keyUp('w')
    pyautogui.press('f')
    AutoOpera.auto_opera()
    pyautogui.press('f')
    AutoOpera.auto_opera()

    Package.CalibrateMap.teleport(960,538)
    pyautogui.keyDown('w')
    time.sleep(3)
    pyautogui.keyUp('w')
    FindTargrtAndMove.main('./DailyImg/WeiTuo5.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0 and times <= 12:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo5.png')
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople01.png',0.7)
        time.sleep(0.8)
        pyautogui.press('x')
        times = times + 1
        if times > 210:
            return False
        pyautogui.press('SPACE')
        if a != 0:
            result = True
            pyautogui.keyUp('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople01.png',0.7 )
        g, h = Sc.CompareWithin('./DailyImg/MengDeBeerPeople04.png',0.7)
        e, f = Sc.CompareWithin('./DailyImg/MengDeBeerPeople03.png',0.7)
        if a != 0 and g == 0 :
            pyautogui.press('f')
            time.sleep(1)
            x, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople07.png', 0.7)
            if x == 0:
                result = True
            else:
                AutoOpera.auto_opera()
                times = 0
            if times > 210:
                return False
        if times < 10:
            Mo.press_key('a',0.1)
        if times > 10:
            Mo.press_key('d', 0.1)

    result = False
    while not result:
        time.sleep(0.5)
        a, b = Sc.CompareWithin('./img/mjend.png')
        if a != 0:
            result = True
    pyautogui.keyUp('w')
    time.sleep(2)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
        a, b = Sc.CompareWithin('./DailyImg/MengDeBeerPeople02.png',0.65)
        if times == 12 or times == 48:
            pyautogui.press('SPACE')
            time.sleep(0.7)
            pyautogui.press('SPACE')
            time.sleep(0.7)
            pyautogui.press('SPACE')
        time.sleep(0.3)
        times = times + 1
        if times > 210:
            return False
        if a != 0:
            result = True
            pyautogui.keyUp('w')
    pyautogui.keyUp('w')
    pyautogui.press('f')
    AutoOpera.auto_opera()
    return True