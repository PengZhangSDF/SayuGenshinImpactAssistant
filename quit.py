import time

from utils import Tools
from urllib.parse import urlencode
import pyautogui
import cv2
import numpy as np
import urllib.parse
import urllib.request
import psutil
import os
import config
from utils.Tools import read_config_value
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("quit.py:当前工作目录：", os.getcwd())
key = read_config_value('./config.txt','Quit','key')
# kill_all = read_config_value('./config.txt','Quit','kill_all')
if key is not None:
    pass
else:
    key = 00000000000000000000000000000


def read_txt_file(file_path):
    with open(file_path, 'r', encoding='GBK') as file:
        content = file.read()
    return content


def screenshot_function(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    # screen_width, screen_height = pyautogui.size()

    # 截图指定部分
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 保存为PNG格式
    cv2.imwrite('screenshot_quit.png', screenshot_cv)

    return screenshot_cv


def sc_send(text, desp='', key='[SENDKEY]'):
    postdata = urllib.parse.urlencode({'text': text, 'desp': desp}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result


def genshin_quit(file_name,mission):
    times = 30

    if times >= 30:
        try:
            Tools.kill_process_by_name('YuanShen.exe')
            try:
                pid = str(Tools.get_window_process_pid('GenshinImpactAssistant'))
                os.popen(f'taskkill -f -pid {pid} ')
            except:
                pass

        except psutil.NoSuchProcess:
            pass

        time.sleep(5)
        ret = sc_send('原神自动化程序', f'原神通过Genshin_quit退出,包含每日任务{mission}的识别成功',
                      key=key)
        return '程序通过quit_genshin正常退出'

if __name__ == '__main__':
    genshin_quit('requirements.txt',True)


