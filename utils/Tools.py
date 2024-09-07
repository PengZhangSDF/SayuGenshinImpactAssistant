import psutil
import win32gui
import time
import win32con
import os
import config

path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("Tools:当前工作目录：", os.getcwd())


# ############################################################################################################ 结束进程
def kill_process_by_name(process_name, debug=False):
    """结束进程，使用/f /im"""

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            if debug:
                print(f"Terminating process {proc.info['name']} with PID {proc.info['pid']}")
            proc.kill()


# 指定要关闭的进程名
# process_name = "chrome.exe"  # 示例：Chrome浏览器进程名

# 关闭指定进程
# kill_process_by_name(process_name)
# ########################################################################################################## 获取当前时间
import datetime


def get_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M')  # 仅保留小时和分钟部分
    return formatted_time


# 调用函数并打印当前时间的小时和分钟
# current_time = get_current_time()
# print(current_time)
# ##################################################################################################### 获取关键词窗口标题
def show_window_by_keyword(program_name, debug=False):
    """使用窗口名激活窗口"""

    def windowEnumerationHandler(hwnd, windowlist):
        windowlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    # 通过枚举获取所有窗口的句柄和标题
    windowlist = []
    win32gui.EnumWindows(windowEnumerationHandler, windowlist)

    # 遍历所有窗口，指定要操作的窗口的标题的关键词，比如“记事本”
    for i in windowlist:
        if program_name in i[1].lower():
            # 按规则显示窗口
            win32gui.ShowWindow(i[0], 4)
            # 激活窗口到前台
            win32gui.SetForegroundWindow(i[0])
            # 显示句柄和标题方便查看
            if debug:
                print(i)
            # 如果匹配“关键词”的窗口有多个，延时一下
            time.sleep(2)


# 使用实例
# program_name = "记事本"
# how_window_by_keyword(program_name)
# 获取所有窗口句柄
# ##################################################################################################### 置顶指定名称窗口
def windows_top(keyname: object, debug=False) -> object:
    """置顶指定标题窗口"""

    hwnd_title = {}

    def get_all_hwnd(hwnd, mouse):
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t:
            if debug:
                print(h, t)
    # 置顶窗口
    hwnd = win32gui.FindWindow(None, keyname)
    print(f"置顶窗口{hwnd}")
    # hwnd = win32gui.FindWindow('xx.exe', None)
    # 窗口需要正常大小且在后台，不能最小化
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    # 窗口需要最大化且在后台，不能最小化
    # ctypes.windll.user32.ShowWindow(hwnd, 3)
    if win32gui.IsWindow(hwnd):
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE |
                              win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)

        if __name__ == '__main__':
            pass
        # 取消置顶
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


# ############################################################################################### 获取指定的值从config.txt
# 打开txt文件并读取内容



# 定义一个函数来获取指定变量的值
def get_variable_value(variable_name):
    with open('./config.txt', 'r') as file:
        data = file.readlines()
    for line in data:
        if line.startswith(variable_name):
            return line.split('=')[-1].strip()

    # 获取指定变量的值
    # variable1 = get_variable_value('variable1')
    # variable2 = get_variable_value('variable2')

    # print(variable1)  # 输出: 100
    # print(variable2)  # 输出: Hello


# ################################################################################################## 关键词获取窗口标题
import difflib


def get_most_similar_window_title(keyword: str) -> str:
    hwnd_title = {}

    def get_all_hwnd(hwnd, mouse):
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            title = win32gui.GetWindowText(hwnd)
            similarity = difflib.SequenceMatcher(None, keyword, title).ratio()
            hwnd_title[hwnd] = {'title': title, 'similarity': similarity}

    win32gui.EnumWindows(get_all_hwnd, 0)

    # 找到相似度最高的窗口
    max_similarity = max(hwnd_title.values(), key=lambda x: x['similarity'])
    return max_similarity['title']


# ############################################################################################################# 多线程运行
import threading


def run_functions(func1, func2):
    # 创建线程
    thread1 = threading.Thread(target=func1)
    thread2 = threading.Thread(target=func2)

    # 启动线程
    thread1.start()
    thread2.start()

    # 等待线程完成
    thread1.join()
    thread2.join()

    print("Both functions have completed.")


# ########################################################################################################## 获取值2.0
import configparser


def read_config_value(file_path, section, key):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
    except configparser.ParsingError as e:
        print(f"Error 找不到文件: {e}")
        return None

    if config.has_section(section):
        if config.has_option(section, key):
            value = config.get(section, key)
            if value.strip() == "":  # 检查值是否为空或仅包含空格
                print(f"值 '{key}' in 表 '{section}' 是空的或者仅为空格")
                return None
            return value
        else:
            print(f"The key '{key}' is not found in section '{section}'")
            return None
    else:
        print(f"The section '{section}' is not found in the configuration file")
        return None

# =================================================================================================================
import win32process


def get_window_process_pid(window_title):
    pid = None  # 初始化 PID

    def callback(hwnd, extra):
        nonlocal pid  # 使用 nonlocal 来修改外部的 pid 变量
        try:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
                _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                pid = process_id  # 将 PID 保存到外部变量
                return False  # 停止枚举
        except Exception as e:
            print(f"Error in callback: {e}")
        return True  # 继续枚举其他窗口

    try:
        win32gui.EnumWindows(callback, None)
    except Exception as e:
        print(f"Error in EnumWindows: {e}")

    return pid  # 返回找到的 PID



