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
print("Mission:ProductOrder01.py:当前工作目录：", os.getcwd())


def product_order01():
    """餐品预定   晨曦酒庄"""
    time.sleep(1)
    times = 0
    Package.CalibrateMap.teleport(671,945)
    pydirectinput.moveRel(xOffset=215,yOffset=0,duration=1,relative=True)
    pyautogui.keyDown('W')
    pyautogui.press('SPACE')
    for i in range(0,20):
        time.sleep(1.5)
        pyautogui.press('SPACE')
    pydirectinput.moveRel(xOffset=-20,yOffset=0,duration=1,relative=True)
    for i in range(0,3):
        time.sleep(1.5)
        pyautogui.press('SPACE')
    pyautogui.press('Ctrl')
    result = False
    while not result:
        a,b = Sc.CompareWithin('./DailyImg/ProductOrder02.png',notify=False)
        if a!=0:
            result = True
        times = times + 1
        if times > 1500:
            return False
    pyautogui.press('F')
    pyautogui.press('F')
    pyautogui.keyUp('W')
    time.sleep(1)
    AutoOpera.auto_opera()
    time.sleep(2)
    Mission.Daily_ProductOrderAll.product_order_home()
    Package.CalibrateMap.newlife()
    return True
