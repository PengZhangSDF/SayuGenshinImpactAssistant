import time

from utils import ScreenCompare as Sc, AutoOpera
import Package.CalibrateMap
from utils.GIautogui import GIautogui as pydirectinput
from utils.GIautogui import GIautogui as pyautogui
import Mission.Daily_ProductOrderAll
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:ProductOrder02.py:当前工作目录：", os.getcwd())


def product_order02():
    """餐品预定   清泉镇"""
    time.sleep(1)
    times = 0
    pyautogui.press('J')
    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/ProductOrder04.png', notify=False)
    pyautogui.press('Esc')
    if a != 0:
        a = 1
    if a != 1:
        exit()
    time.sleep(1)
    Package.CalibrateMap.teleport(950, 808)
    pyautogui.keyDown('W')
    time.sleep(6)
    pydirectinput.moveTo(1700, 540)
    pydirectinput.moveRel(xOffset=600, yOffset=0, duration=1, relative=True)
    pydirectinput.moveRel(xOffset=600, yOffset=0, duration=1, relative=True)
    pydirectinput.moveRel(xOffset=600, yOffset=0, duration=1, relative=True)
    pydirectinput.moveRel(xOffset=80, yOffset=0, duration=1, relative=True)
    for i in range(0, 8):
        time.sleep(1)
        pyautogui.press('SPACE')
    pyautogui.press('Ctrl')
    result = False
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder05.png', notify=False)
        if a != 0:
            result = True
        if times >= 500:
            return False
    pyautogui.press('F')
    pyautogui.keyUp('W')
    AutoOpera.auto_opera()
    pyautogui.press('J')
    time.sleep(1)
    a, b = Sc.CompareWithin('./DailyImg/ProductOrder04.png', notify=False)
    pyautogui.press('Esc')
    time.sleep(1)
    if a != 0:
        Package.CalibrateMap.teleport(950, 808)
        pydirectinput.moveRel(xOffset=350, yOffset=0, duration=1, relative=True)
        pyautogui.keyDown('W')
        time.sleep(5)
        pydirectinput.moveRel(xOffset=50, yOffset=0, duration=1, relative=True)
        time.sleep(14)
        pydirectinput.press('Ctrl')
        result = False
        times = 0
        while not result:
            a, b = Sc.CompareWithin('./DailyImg/ProductOrder06.png', notify=False)
            times = times + 1
            if a != 0:
                result = True
            if times >= 500:
                return False
        pyautogui.press('F')
        pyautogui.keyUp('W')
        time.sleep(1)
        AutoOpera.auto_opera()
        pyautogui.press('J')
        time.sleep(1)
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder04.png', notify=False)
        pyautogui.press('Esc')
        time.sleep(1)
        if a != 0:
            Package.CalibrateMap.teleport(950, 808)
            pydirectinput.moveRel(xOffset=600, yOffset=0, duration=1, relative=True)
            time.sleep(0.2)
            pydirectinput.moveRel(xOffset=600, yOffset=0, duration=1, relative=True)
            time.sleep(0.2)
            pydirectinput.moveRel(xOffset=375, yOffset=0, duration=1, relative=True)
            time.sleep(0.2)
            pyautogui.keyDown('W')
            time.sleep(13)
            result = False
            times = 0
            for i in range(0, 5):
                pyautogui.press('SPACE')
                time.sleep(0.7)
            pyautogui.press('Ctrl')
            while not result:
                a, b = Sc.CompareWithin('./DailyImg/ProductOrder07.png', notify=False)
                times = times + 1
                if a != 0:
                    result = True
                if times > 800:
                    return False
            pyautogui.press('F')
            pyautogui.keyUp('W')
            time.sleep(1)
            AutoOpera.auto_opera()
    Mission.Daily_ProductOrderAll.product_order_home()
    Package.CalibrateMap.newlife()
    return True
