import time
import pickle
from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyboardListener, KeyCode
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Controller
from utils.GIautogui import GIautogui as pyautogui
import pydirectinput
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:KeyMouseRe.py:当前工作目录：", os.getcwd())

pyautogui.MINIMUM_DURATION = 0.0001


def record_actions(file_name):
    actions = []

    def on_click(x, y, button, pressed):
        if pressed:
            actions.append(('click', x, y, button))
            print(f"Click at ({x}, {y}) recorded")

    def on_move(x, y):
        actions.append(('move', x, y, time.time()))
        time.sleep(0.1)
        print(f"Mouse moved to ({x}, {y},{time.time()}) recorded")

    def on_press(key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        actions.append(('press_key', key_str, time.time()))
        print(f"Key {key_str} pressed")

    def on_release(key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        actions.append(('release_key', key_str, time.time()))
        print(f"Key {key_str} release")

    with open(file_name, 'wb') as file:
        listener = MouseListener(on_click=on_click, on_move=on_move)
        k_listener = KeyboardListener(on_press=on_press, on_release=on_release)

        listener.start()
        k_listener.start()

        try:
            while True:
                time.sleep(0.01)
        except KeyboardInterrupt:
            listener.stop()
            k_listener.stop()

        pickle.dump(actions, file)


def play_actions(file_name):
    mouse = MouseController()
    keyboard = KeyboardController()

    with open(file_name, 'rb') as file:
        timestamp = 0
        actions = pickle.load(file)
        start_time = actions[0][2]
        print(actions[0], actions[1], actions[2], actions[3])
        last_action_time = None
        for action in actions:
            if last_action_time is not None:
                time_diff = action[3] - last_action_time
            else:
                time_diff = 0
            if action[0] == 'click':
                x, y = action[1], action[2]
                mouse.position = (x, y)
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(0.01)

            elif action[0] == 'move':
                x, y = action[1], action[2]
                pydirectinput.moveTo(x=x, y=y, duration=0.1, relative=True)
                print(f'Mouse moved to {x},{y},with time delay{time_diff}')
                time.sleep(0.01)

            elif action[0] == 'press_key':
                key_str = action[1]
                timestamp = action[2]
                keyboard = Controller()
                time_diff = timestamp - start_time
                if time_diff > 10 ** 6:
                    time_diff = 0
                try:
                    print(f"{key_str}press with tick delay{time_diff}")
                    time.sleep(time_diff)
                    keyboard.press(key_str)
                    keyboard.release(key_str)
                except AttributeError:
                    print(f"Unknown key: {key_str}")
                except ValueError:
                    keyboard = Controller()
                    # 将字符串变量转换为对应的 Key 枚举成员
                    key = eval(key_str)
                    # 按下键盘上的对应按键
                    keyboard.press(key)


            elif action[0] == 'release_key':
                key_str = action[1]
                timestamp = action[2]
                keyboard = Controller()
                time_diff = timestamp - start_time
                if time_diff > 10 ** 6:
                    time_diff = 0
                try:
                    print(f"{key_str}release with tick delay{time_diff}")
                    time.sleep(time_diff)
                    keyboard.release(key_str)
                except AttributeError:
                    print(f"Unknown key: {key_str}")
                except ValueError:
                    keyboard = Controller()
                    # 将字符串变量转换为对应的 Key 枚举成员
                    key = eval(key_str)
                    # 按下键盘上的对应按键
                    keyboard.release(key)
            start_time = timestamp


file_name = "AutoDailyMission01.pkl"


def record_action(file_name):
    time.sleep(1)
    try:
        print("开始记录鼠标键盘操作，请按 F2 + C 结束...")
        record_actions(file_name)
    except KeyboardInterrupt:
        print("录制结束")


def play_action(file_name):
    time.sleep(1)
    print("开始播放鼠标键盘操作...")
    play_actions(file_name)

time.sleep(5)
record_action("AutoDailyMission01.pkl")
print('record will start in 30s')
time.sleep(5)
play_action("AutoDailyMission01.pkl")
