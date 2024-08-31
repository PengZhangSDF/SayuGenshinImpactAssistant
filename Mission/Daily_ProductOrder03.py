import Package.CalibrateMap
import Mission.Daily_ProductOrderAll
import time
import utils.auto_fight_threading
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:ProductOrder03.py:当前工作目录：", os.getcwd())

def ProductOrder03():
    time.sleep(4)
    Package.CalibrateMap.teleport(995,1011)
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder09.png',0.6)
        if a != 0:
            result = True
    time.sleep(1)
    pyautogui.keyUp('w')
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder10.png',0.6)
        times = times + 1
        if a != 0:
            result = True
            utils.auto_fight_threading.stop_auto_fight_config()
            auto_fight_threading.join()
        if times > 240:
            return False
    pyautogui.press('v')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.press('Ctrl')
    pyautogui.keyDown('w')
    result = False
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/ProductOrder11.png')
        if a != 0:
            result = True
            pyautogui.press('f')
            pyautogui.keyUp('w')
    AutoOpera.auto_opera()
    Mission.Daily_ProductOrderAll.product_order_home()
    return True