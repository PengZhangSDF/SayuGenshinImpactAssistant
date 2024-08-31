import time

import Package.CalibrateMap
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc, AutoOpera

import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Mission:AdventurersLimitAbility.py:当前工作目录：", os.getcwd())
def AdventuresLimitAbility():
    time.sleep(5)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(960, 543)

    def move_and_click():
        pyautogui.keyDown('W')
        for i in range(0, 10):
            pyautogui.press('SPACE')
            time.sleep(1)
        time.sleep(1)
        pyautogui.press('Ctrl')
        result = False
        while not result:
            a, b = Sc.CompareWithin('./DailyImg/AdventurersLimitAbility01.png')
            if a > 0:
                pyautogui.press('F')
                pyautogui.keyUp('W')
                return True

    time.sleep(1)
    FindTargrtAndMove.main()
    move_and_click()
    AutoOpera.auto_opera()
    Package.CalibrateMap.teleport(481, 519)
    pyautogui.press('J')
    time.sleep(1)
    a, b = Sc.CompareWithin('./img/HomeOfDaily.png', 0.6)
    if a != 0:
        pyautogui.click(a, b)
    time.sleep(0.5)
    a, b = Sc.CompareWithin('./DailyImg/GoToDes.png')
    pyautogui.click(a, b)
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('W')
    time.sleep(10)
    pyautogui.keyUp('W')
    pyautogui.press('V')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('W')
    time.sleep(6)
    pyautogui.keyUp('W')
    pyautogui.press('U')
    time.sleep(20)
    pyautogui.press('U')
    pyautogui.press('4')
    Package.CalibrateMap.teleport(960, 543)
    time.sleep(1)
    FindTargrtAndMove.main()
    move_and_click()
    AutoOpera.auto_opera()
    Package.CalibrateMap.newlife()
    return True
