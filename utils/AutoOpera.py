import pydirectinput

from utils import ScreenCompare as Sc, MouseKey as Mo
from utils.GIautogui import GIautogui as pyautogui
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:AutoOpera.py:当前工作目录：", os.getcwd())

def auto_opera():
    a = 0
    while a < 10:
        x, y = Sc.CompareWithin('./img/juqing2.png', notify=False)
        p, q = Sc.CompareWithin('./img/juqing.png', notify=False)
        m, n = Sc.CompareWithin('./img/juqing3.png', notify=False)
        u, i = Sc.CompareWithin('./img/juqing4.png', notify=False)
        o, p = Sc.CompareWithin('./DailyImg/Give.png', notify=False)
        if x == 0 and y == 0 and p == 0 and q == 0 and m == 0 and n == 0:
            a = a + 1
        elif u != 0 and i != 0:
            a = 10
        elif o != 0:
            l, k = Sc.CompareWithin('./img/object.png', 0.9)
            if l != 0:
                pyautogui.click(l, k)
            h,j = Sc.CompareWithin('./img/put.png')
            if h != 0:
                pyautogui.click(h, j)
            pyautogui.click(o, p)

            pydirectinput.click(o, p)
        else:
            Mo.press_key('SPACE', 0.1)
            m1, n1 = Sc.CompareWithin('./img/juqing3.png', notify=False)
            if m1 != 0:
                Mo.click_mouse(x=m1,y=n1)
            else:
                Mo.click_mouse(x=1429, y=806)
    return True
