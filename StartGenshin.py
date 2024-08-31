import time
import os
from utils import ScreenCompare as Sc, Tools, MouseKey as Mo
import Package.CalibrateMap
import logging
import sys
import ctypes
import pyautogui
import Package.log_config
from python.PPOCR_api import GetOcrApi
import config
logger = Package.log_config.logger
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_path = os.path.join(project_root, 'config.txt')
ocr = GetOcrApi(exePath='./PaddleOCR-json_v1.4.0/PaddleOCR-json.exe')
logger.info('Paddle OCR主引擎已经启动')


def print_one_by_one(text):  # 此处的print_one_by_one可以自定义名称

    sys.stdout.write("\r " + " " * 60 + "\r")  # /r 光标回到行首, \n 换行

    sys.stdout.flush()  # 把缓冲区全部输出

    for c in text:
        pyautogui.press(c)

        sys.stdout.flush()

        time.sleep(0.1)


def get_current_language():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    hkl = user32.GetKeyboardLayout(0)
    lid = hkl & 0xFFFF
    return lid


# 切换到英国英语输入法
def switch_to_english():
    ENGLISH_LANGUAGE_ID = 2057
    max_attempts = 1  # 最大尝试次数
    attempt = 0

    while attempt < max_attempts:
        current_language = get_current_language()
        if current_language == ENGLISH_LANGUAGE_ID:
            print("已切换到英国英语输入法")
            return
        else:
            print("尝试切换输入法...")
            pyautogui.hotkey('alt', 'shift')
            time.sleep(1)  # 等待切换生效
            attempt += 1


def Start():
    result = False
    time.sleep(10)
    Tools.windows_top('原神')
    Tools.windows_top('YuanShen')
    Tools.windows_top('Yuanshen')
    while not result:
        Sc.screenshot_function(1772, 52, 1858, 164)
        result = Sc.compare_image('./img/login.png', 0.7)
        Mo.click_mouse(x=1085, y=705)
        time.sleep(2)
        if result:
            logging.info("识别完成:大门")

    while Sc.compare_image('./img/login.png', 0.7):
        Sc.screenshot_function(1772, 52, 1858, 164)
        Mo.click_mouse()
        logging.info('尝试进入')
        time.sleep(2)
        a, b = Sc.CompareWithin('./img/login1.png')
        if a != 0:
            switch_to_english()
            x1, y1 = Sc.CompareWithin('./img/login1.png')
            x2, y2 = Sc.CompareWithin('./img/login2.png')
            x3, y3 = Sc.CompareWithin('./img/login3.png')
            account = Tools.get_variable_value('account')
            password = Tools.get_variable_value('password')
            if account is None or password is None:
                pass
            else:
                pyautogui.click(x1, y1)
                time.sleep(1)
                print_one_by_one(account)
                pyautogui.click(x2, y2)
                time.sleep(1)
                print_one_by_one(password)
                pyautogui.click(x3, y3)
                Mo.click_mouse(x=1085, y=705)
    result = False
    while not result:
        Mo.click_mouse('left', 0.1, 1000, 900)
        a = Sc.screenshot_function(33, 24, 80, 71)
        result = Sc.compare_image('./img/mjend.png', 0.7)
        time.sleep(2)
    logging.info("识别完成：主界面")

    result = Package.CalibrateMap.newlife()
    if not result:
        return False
    else:
        return True
