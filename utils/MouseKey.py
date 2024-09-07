from utils.GIautogui import GIautogui as pyautogui
import time
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:MouseKey.py:当前工作目录：", os.getcwd())

def click_mouse(button='left', duration=0.1, x=None, y=None, tick_delay=0.1, times=1):
    """Click the mouse button at the specified coordinates."""
    if button == 'left':
        pyautogui.click(x=x, y=y, duration=duration)
    elif button == 'middle':
        pyautogui.middleClick(x=x, y=y, duration=duration)
    elif button == 'scroll':
        for i in range(0,times):
            pyautogui.scroll(duration, x=x, y=y)
    elif button == 'right':
        pyautogui.rightClick(x=x, y=y, duration=duration)
    time.sleep(tick_delay)


def move_mouse(direction, distance):
    """包含形参up,down,left,right"""
    if direction == 'up':
        pyautogui.move(0, -distance, duration=0.25)
    elif direction == 'down':
        pyautogui.move(0, distance, duration=0.25)
    elif direction == 'left':
        pyautogui.move(-distance, 0, duration=0.25)
    elif direction == 'right':
        pyautogui.move(distance, 0, duration=0.25)

def press_key(key, duration, tick_delay=0.1):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)
    time.sleep(tick_delay)

def drag_mouse(direction, distance):
    """在屏幕上进行鼠标点划操作"""
    if direction == 'left':
        pyautogui.drag(distance, 0, duration=0.5)  # 向
    elif direction == 'right':
        pyautogui.drag(-distance, 0, duration=0.5)  # 向
    elif direction == 'down':
        pyautogui.drag(0, -distance, duration=0.5)  # 向
    elif direction == 'up':
        pyautogui.drag(0, distance, duration=0.5)  # 向

# 调用示例
#drag_mouse('right', 100)  # 向右拖动100个像素


# 使用示例
#click_mouse('left', 0.1)
#move_mouse('down', 100)
#press_key('ctrl', 1)
