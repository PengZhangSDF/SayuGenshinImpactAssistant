import utils.ScreenCompare as Sc
import time
import pyautogui as pyautogui_real
import Package
import cv2
import numpy as np
import utils.WhichPage as WhichPage
from utils import Tools
import os
import config
logger = Package.log_config.logger
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("waiting_finish.py:当前工作目录：", os.getcwd())
def screenshot_function(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    # screen_width, screen_height = pyautogui.size()

    # 截图指定部分
    screenshot = pyautogui_real.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 保存为PNG格式
    cv2.imwrite('screenshot_quit.png', screenshot_cv)

    return screenshot_cv

def waiting():
    times = 0
    warning = 0
    time_start = time.time()
    while times < 30:
        Sc.screenshot_function()
        time.sleep(0.3)
        screenshot_function()
        result = Sc.compare_image('screenshot_quit.png', pprint=False)

        if result:
            times = times + 1
            logger.info(f'识别原神无动作退出，剩余时间{30 - times}秒')
        elif not result:
            warning = warning + 1
            times = 0
        time_pass = time.time() - time_start
        if time_pass > 1800:
            times = 31
            Tools.kill_process_by_name('cmd.exe')
            os.popen('taskkill /f /im python.exe /t')
            logger.error('GIA耗时过长，退出')
    logger.warning(f'识别原神出现画面变化{warning}次')
    if times >= 30:
        WhichPage.take_to_page('main')
        time.sleep(2)