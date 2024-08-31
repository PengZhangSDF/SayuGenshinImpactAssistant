import pyautogui
import keyboard
import time
import os
import re

# 文件存储路径
save_path = 'screenshots'
if not os.path.exists(save_path):
    os.makedirs(save_path)


# 获取文件夹中已有的最大文件编号
def get_next_file_number(path):
    max_number = 0
    for filename in os.listdir(path):
        match = re.match(r"(\d+)\.png", filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    return max_number + 1


# 初始化文件计数器
file_count = get_next_file_number(save_path)


def take_screenshot():
    global file_count
    screenshot = pyautogui.screenshot()
    filename = os.path.join(save_path, f"{file_count}.png")
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")
    file_count += 1


# 监听屏幕截图键（Print Screen）
print("Press 'Print Screen' to take a screenshot.")
while True:
    try:
        if keyboard.is_pressed('print screen'):
            take_screenshot()
            time.sleep(1)  # 避免重复截图
    except KeyboardInterrupt:
        print("Program terminated.")
        break
