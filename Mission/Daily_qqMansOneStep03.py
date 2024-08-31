import Package.CalibrateMap
import utils.auto_fight_threading
import time
from utils.GIautogui import GIautogui as pyautogui
from utils import FindTargrtAndMove, ScreenCompare as Sc
from utils import WhichPage
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
# 1387,260
# 打印当前工作目录
print("Mission:qqMansOneStep02.py:当前工作目录：", os.getcwd())
def qqMansOneStep03():
    time.sleep(1)
    pyautogui.press('4')
    Package.CalibrateMap.teleport(1387,260)
    pyautogui.press('j')
    time.sleep(1)
    x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
    if x != 0:
        pyautogui.click(x=x, y=y)
    a, b = Sc.CompareWithin('./img/qqMansOneStep.png')
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

    WhichPage.take_to_page('main')
    FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    pyautogui.keyDown('w')
    result = False
    times = 0
    while not result:
        times = times + 1
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep03.png', sim_num=0.6, notify=False)
        if a != 0:
            result = True
        if times > 500:
            return False
        pyautogui.press('v')
        if times % 10 == 0:
            FindTargrtAndMove.main('./DailyImg/WEITUO.png')
    time.sleep(3)
    auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
    pyautogui.keyUp('w')
    result = False
    times = 0
    while not result:
        a, b = Sc.CompareWithin('./DailyImg/qqMansOneStep02.png', notify=False)
        times = times + 1
        if a != 0:
            result = True
        if times > 1000:
            return False
    utils.auto_fight_threading.stop_auto_fight_config()
    auto_fight_threading.join()
    Package.CalibrateMap.newlife()

if __name__ == '__main__':
    time.sleep(4)
    qqMansOneStep03()