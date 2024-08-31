import Package.CalibrateMap
import utils.auto_fight_threading
import time
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, MouseKey as Mo
from utils.GIautogui import GIautogui as pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:Impregnable02.py:当前工作目录：", os.getcwd())

def Impregnable02():
    time.sleep(4)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./DailyImg/Impregnable0.png')
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
    Package.CalibrateMap.open_map()
    pyautogui.moveTo(900, 700)
    time.sleep(0.5)
    Mo.drag_mouse('up',-800)
    pyautogui.moveTo(900, 700)
    time.sleep(0.5)
    Mo.drag_mouse('up',-800)
    time.sleep(0.5)
    pyautogui.click(1088,831)
    time.sleep(1)
    x1, y1 = Sc.CompareWithin('./img/TeleportPoint.png')
    x2, y2 = Sc.CompareWithin('./img/TeleportPoint2.png')
    x3, y3 = Sc.CompareWithin('./img/TeleportPoint3.png')
    x4, y4 = Sc.CompareWithin('./img/teleport.png')
    if x1 != 0 or x2 != 0 or x3 != 0 and x4 == 0:
        if x1 != 0:
            Mo.click_mouse(x=x1, y=y1)
        elif x2 != 0 and x1 == 0:
            Mo.click_mouse(x=x2, y=y2)
        elif x3 != 0 and x1 == 0:
            Mo.click_mouse(x=x3, y=y3)
        time.sleep(1)
    Mo.click_mouse("left", 0.1, 1692, 1008, 3)  # 传送
    result = False
    while not result:
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
    time.sleep(1)
    pyautogui.press('v')
    pyautogui.keyDown('w')
    for i in range(1,10):
        time.sleep(0.5)
        pyautogui.press('SPACE')
        time.sleep(0.5)
        pyautogui.press('D')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    result = False
    times = 0
    while not result:
        times = times + 1
        pyautogui.press('SPACE')
        a, b = Sc.CompareWithin('./DailyImg/Impregnable3.png')
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        if a != 0:
            result = True
        if times % 4 == 0 and 16 >= times >= 8:
            pyautogui.keyDown('d')
        if times % 8 == 0:
            pyautogui.keyUp('d')
        time.sleep(0.8)
        if times > 135:
            return False
    pyautogui.keyUp('d')
    pyautogui.keyUp('w')
    FindTargrtAndMove.main('./DailyImg/Impregnable1.png')
    result = False
    times = 0
    pyautogui.press('Ctrl')
    pydirectinput.moveRel(xOffset=-100,yOffset=0,duration=1,relative=True)
    pyautogui.keyDown('w')
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/Run.png')
        if a != 0:
            result = True
            pyautogui.press('f')
        if times > 200:
            return False
    pyautogui.keyUp('w')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    times = 0
    while not result:
        a,b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png',notify=False)
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
        times = times + 1
        if a != 0:
            result = True
        if times > 1000:
            return False
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    Package.CalibrateMap.newlife()
    return True




