import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
import Mission.Daily_ProductOrder01
import Mission.Daily_ProductOrder03
import Mission.Daily_ProductOrder02
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:ProductOrderAll.py:当前工作目录：", os.getcwd())


def product_order_home():
    times = 0
    time.sleep(4)
    Package.CalibrateMap.teleport(960, 543)
    pyautogui.press('4')
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./img/ProductOrder.png')
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
    pyautogui.keyDown('w')
    for i in range(0,5):
        time.sleep(0.8)
        pyautogui.press('SPACE')
    pyautogui.keyUp('w')
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder01.png')
        c, d = Sc.CompareWithin('./DailyImg/ProductOrder03.png')
        if a != 0 and c == 0:
            result = True
        if times % 4 == 0:
            pyautogui.press('v')
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
            FindTargrtAndMove.main('./DailyImg/WeiTuo3.png')
        times = times + 1
    pyautogui.press('f')
    pyautogui.keyUp('w')
    AutoOpera.auto_opera()



def product_order():
    """餐品预定   晨曦酒庄"""
    product_order_home()
    time.sleep(1)
    pyautogui.press('f')
    AutoOpera.auto_opera()
    pyautogui.press('j')
    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/ProductOrder04.png', notify=False)
    c, d = Sc.CompareWithin('./DailyImg/ProductOrder08.png')
    pyautogui.press('Esc')
    if a != 0 and c == 0:
        result = Mission.Daily_ProductOrder02.product_order02()
    elif c != 0:
        result = Mission.Daily_ProductOrder03.ProductOrder03()
    else:
        result = Mission.Daily_ProductOrder01.product_order01()
    if result:
        return True
    else:
        return False