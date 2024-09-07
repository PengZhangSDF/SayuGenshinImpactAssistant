import time
from utils import ScreenCompare as Sc, Tools
import pyautogui
import os
def UpDateGame():
    update = False
    lists = []
    path_to_updater = Tools.get_variable_value('launcher_path')
    os.popen(path_to_updater)
    result = False
    while not result:
        time.sleep(1)
        a, b = Sc.CompareWithin('./img/MiHoYoL.png',checkGenshin=False)
        launcher_name = Tools.get_most_similar_window_title('米哈游启动器')
        Tools.windows_top(launcher_name)
        if a != 0:
            result = True
    a, b = Sc.CompareWithin('./img/GenShin.png',checkGenshin=False)
    if a != 0:
        pyautogui.click(a, b)
    time.sleep(1)
    a, b = Sc.CompareWithin('./img/update01.png',0.9,checkGenshin=False)
    if a != 0:
        pyautogui.click(a, b)
        lists.append('原神')
        update = True
    result = False
    while not result:
        a, b = Sc.CompareWithin('./img/StartGame.png',0.9,checkGenshin=False)
        time.sleep(2)
        if a != 0:
            result = True
    if not update:
        lists.append('全部游戏处于最新版本')
    return lists
if __name__ == '__main__':
    UpDateGame()