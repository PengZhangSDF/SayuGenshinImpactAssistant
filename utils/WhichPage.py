import time

from utils.GIautogui import GIautogui as pyautogui
from utils import ScreenCompare as Sc
from Package.log_config import logger
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:WhichPage.py:当前工作目录：", os.getcwd())
def which_page():
    """检测所处界面
        返回 str:
            Main 主界面
            map.teleport 地图已经点击锚点或者切换地图界面
            map.choose 地图选择内容
            map.main 地图主界面
            menu 菜单
            mission 任务界面
            book 冒险之证
            dead 死亡界面
            """
    a, b = Sc.CompareWithin('./img/Dead.png')
    if a != 0:
        return '死亡'
    Sc.screenshot_function(36,28,76,78)
    result = Sc.compare_image('./img/mjend2.png')
    if result:
        return 'Main'
    c1, d1 = Sc.CompareWithin('./img/telepoint.png')
    c2, d2 = Sc.CompareWithin('./img/map.png')
    c3, d3 = Sc.CompareWithin('./img/Map02.png')
    if c1 != 0:
        if c2 != 0:
            return 'map.teleport'
        if c3 != 0:
            return 'map.choose'
        if c2 == 0 and c3 == 0:
            return 'map.main'
    a, b = Sc.CompareWithin('./img/menu.png')
    if a != 0:
        return 'menu'
    a, b = Sc.CompareWithin('./img/mission.png')
    if a != 0:
        return 'mission'
    a, b = Sc.CompareWithin('./img/mxbook.png')
    if a != 0:
        return 'book'


def take_to_page(page_to_which):
    """支持main,map,book,menu界面的打开"""
    page = which_page()
    logger.info(f'当前页面：{page}')
    result = False
    while not result:
        time.sleep(1)
        page = which_page()
        if page == 'Main':
            result = True
        elif page == 'dead':
            a, b = Sc.CompareWithin('./img/Dead.png')
            pyautogui.click(a, b)
        else:
            pyautogui.press('Esc')
    time.sleep(1)
    logger.info(f'切换到页面{page_to_which}')
    if page_to_which == 'main':
        return True
    if page_to_which == 'map':
        pyautogui.press('m')
        return True
    if page_to_which == 'book':
        pyautogui.press('F1')
        return True
    if page_to_which == 'menu':
        pyautogui.press('Esc')
        return True
