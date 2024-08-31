import time

from utils import ScreenCompare as Sc, OCR, WhichPage
from utils.GIautogui import GIautogui as pyautogui
import config
import os
path = config.get_config_directory()
os.chdir(path)

# 打印当前工作目录
print("Check_TODO:当前工作目录：", os.getcwd())

def checktodo():
    time.sleep(3)
    pyautogui.press('m')
    time.sleep(1.5)
    x, y = Sc.CompareWithin('./img/TiLi.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(1.5)
    result = OCR.ppocr(1638, 29, 1692, 61)
    for i in result:
        try:
            num = int(i)
        except ValueError:
            if i == "\x1b[0m":
                pass
            else:
                num = 200
    print(num)
    if num > 20:
        DoEnigma = True
    else:
        DoEnigma = False
    pyautogui.press('Esc')
    WhichPage.take_to_page('book')
    time.sleep(2)
    x, y = Sc.CompareWithin('./img/WeiTuo.png')
    if x != 0:
        pyautogui.click(x, y)
    time.sleep(1)
    result = OCR.ppocr(514, 363, 598, 398)
    for i in result:
        if i == '4/4' or i == '414':
            DoDailyMission = False
        else:
            DoDailyMission = True
    WhichPage.take_to_page('main')
    return DoEnigma,DoDailyMission
