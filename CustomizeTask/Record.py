# -*- coding: utf-8 -*-

import json
import time
import cvAutoTrack.cvAutoTrack
from pynput import keyboard, mouse
import threading
# 初始化auto_tracker
auto_tracker = cvAutoTrack.cvAutoTrack.AutoTracker()


def initialize_tracker():
    initialized = auto_tracker.init()  # 初始化
    return initialized


def get_rotation():
    success, angle_of_view = auto_tracker.get_rotation()  # 获取视角
    return success, angle_of_view


def get_transform():
    success, x, y, arrow_angle = auto_tracker.get_transform()  # 获取坐标和小箭头方向
    return success, x, y, arrow_angle


# 键盘和鼠标记录开始和结束控制
recording = False
data = []


# 按键处理函数
def on_press(key):
    global recording, data

    try:
        if key == keyboard.Key.home:
            recording = True
            print("记录开始")
        elif key == keyboard.Key.end:
            recording = False
            save_to_json()
            print("记录结束")
            return False  # 结束监听

        if recording:
            # 使用 key 的 name 判断按键
            if hasattr(key, 'char'):
                key_char = key.char
            elif hasattr(key, 'name'):
                key_char = key.name
            else:
                key_char = None

            # 仅在按下这些键时记录
            if key_char in ['space', 'f', 'e', 'z', 'j', 't']:
                timestamp = time.time()
                success_transform, x, y, arrow_angle = get_transform()
                success_rotation, angle_of_view = get_rotation()

                if success_transform and success_rotation:
                    action = key_char if key_char != 'z' else 'path'
                    if key_char == 'j':
                        action = 'autofight'
                    elif key_char == 't':
                        action = 't'

                    event = [round(x, 2), round(y, 2), round(angle_of_view, 1), round(arrow_angle, 1), action]
                    data.append(event)
                    print(f"记录事件: {event}")

    except AttributeError:
        print("按下无法识别的按键")


# 鼠标点击处理函数
def on_click(x, y, button, pressed):
    global recording, data
    if recording and pressed and button == mouse.Button.left:  # 检测左键点击
        timestamp = time.time()
        success_transform, x, y, arrow_angle = get_transform()
        success_rotation, angle_of_view = get_rotation()

        if success_transform and success_rotation:
            action = 'click'
            event = [round(x, 2), round(y, 2), round(angle_of_view, 1), round(arrow_angle, 1), action]
            data.append(event)
            print(f"记录事件: {event}")


def save_to_json():
    with open("game_record.json", "w") as file:
        json.dump(data, file, indent=4)


# 开启键盘监听
def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


# 开启鼠标监听
def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


# 主程序
if __name__ == "__main__":
    if initialize_tracker():
        print("auto_tracker 初始化成功")

        # 同时监听键盘和鼠标事件
        keyboard_thread = threading.Thread(target=start_keyboard_listener)
        mouse_thread = threading.Thread(target=start_mouse_listener)

        keyboard_thread.start()
        mouse_thread.start()

        keyboard_thread.join()  # 确保主线程保持活动状态
        mouse_thread.join()
    else:
        print("auto_tracker 初始化失败")
