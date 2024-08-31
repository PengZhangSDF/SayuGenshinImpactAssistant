import threading
import time
from utils.GIautogui import GIautogui as pyautogui
from AutoFight import FindTree
from AutoFight.LockEastAngle import adjust_view_to_east_once
import mss
import config
import os
import Package.log_config
logger = Package.log_config.logger
from ultralytics import YOLO
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
logger.info("FindTreeMain.py:当前工作目录：", os.getcwd())

SCREEN_WIDTH = 1920  # 屏幕宽度，按实际需要调整
CENTER_THRESHOLD = 25  # 中心区域允许的范围

# 创建一个Event对象
stop_event = threading.Event()
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
logger.info(f"FindTree.py:当前工作目录：{os.getcwd()}")
# 加载训练好的YOLOv8模型
model = YOLO('./AutoFight/best.pt')
def find_tree_not_exist(sct, stop_event):
    times = 0
    while not stop_event.is_set():
        tree_x = FindTree.find_tree(sct)
        if tree_x is None:
            times += 1
            # 如果没有检测到树，尝试左右移动直到检测到树
            if times % 2 == 0:
                pyautogui.keyDown('a')
                time.sleep(times + 0.1)
                pyautogui.keyUp('a')
            else:
                pyautogui.keyDown('d')
                time.sleep(times + 0.1)
                pyautogui.keyUp('d')
            time.sleep(0.2)
            logger.info('寻找树')
        else:
            return tree_x



def move_character(stop_event):
    sct = mss.mss()  # 在线程内部初始化 mss
    task_completed = False

    while not stop_event.is_set() and not task_completed:
        tree_x = FindTree.find_tree(sct)
        if tree_x is None:
            pyautogui.keyUp('d')
            pyautogui.keyUp('a')
            tree_x = find_tree_not_exist(sct, stop_event)
        if tree_x is not None:
            pyautogui.keyUp('d')
            pyautogui.keyUp('a')
            fail_count = 0
            success_count = 0
            if tree_x > SCREEN_WIDTH / 2 - CENTER_THRESHOLD:
                pyautogui.keyDown('d')  # 持续按下 'd' 键
                time.sleep(0.05)
                logger.info('树在右边，向右走')
                try:
                    while True:
                        new_tree_x = FindTree.find_tree(sct)
                        if new_tree_x is None:
                            fail_count += 1
                        else:
                            fail_count = 0  # 重置计数器
                            success_count += 1
                        if success_count > 1:
                            success_count = 0
                            break
                        if fail_count >= 5:
                            raise TypeError("连续5次未检测到树")
                        if SCREEN_WIDTH / 2 - CENTER_THRESHOLD <= new_tree_x <= SCREEN_WIDTH / 2 + CENTER_THRESHOLD:
                            task_completed = True
                            break
                        if stop_event.is_set():
                            break
                        time.sleep(0.05)  # 等待一段时间再检测
                except TypeError:
                    pyautogui.keyUp('d')
                    tree_x = find_tree_not_exist(sct, stop_event)
                pyautogui.keyUp('d')  # 释放 'd' 键

            elif tree_x < SCREEN_WIDTH / 2 + CENTER_THRESHOLD:
                pyautogui.keyDown('a')  # 持续按下 'a' 键
                logger.info('树在左边，向左走')
                time.sleep(0.05)
                try:
                    while True:
                        new_tree_x = FindTree.find_tree(sct)
                        if new_tree_x is None:
                            fail_count += 1
                        else:
                            fail_count = 0  # 重置计数器
                            success_count += 1
                        if success_count > 1:
                            success_count = 0
                            break
                        if fail_count >= 5:
                            raise TypeError("连续5次未检测到树")
                        if SCREEN_WIDTH / 2 - CENTER_THRESHOLD <= new_tree_x <= SCREEN_WIDTH / 2 + CENTER_THRESHOLD:
                            task_completed = True
                            break
                        if stop_event.is_set():
                            break
                        time.sleep(0.05)  # 等待一段时间再检测
                except TypeError:
                    pyautogui.keyUp('a')
                    tree_x = find_tree_not_exist(sct, stop_event)
                pyautogui.keyUp('a')  # 释放 'a' 键
            else:
                task_completed = True
                break
    times = 0
    while times < 1:
        tree_x = FindTree.find_tree(sct)
        while tree_x < SCREEN_WIDTH / 2 + 20:
            tree_x = FindTree.find_tree(sct)
            for _ in range(10):
                pyautogui.press('a')
            time.sleep(0.1)
            logger.info('树在左边，向左走')
        times = times + 1
        while tree_x > SCREEN_WIDTH / 2 + 20:
            tree_x = FindTree.find_tree(sct)
            for _ in range(10):
                pyautogui.press('d')
            time.sleep(0.1)
            logger.info('树在右边，向右走')
        # 树的横坐标在允许范围内，停止移动


    logger.info("定位古树线程结束")
    stop_event.set()  # 通知其他线程结束

def keep_east_direction(stop_event):
    while not stop_event.is_set():
        adjust_view_to_east_once()
    else:
        stop_event.clear()

    logger.info("锁定东方向视角线程结束.")

def main_threading():
    # 创建线程
    move_thread = threading.Thread(target=move_character, args=(stop_event,))
    east_thread = threading.Thread(target=keep_east_direction, args=(stop_event,))

    # 启动线程
    east_thread.start()
    time.sleep(1)
    move_thread.start()

    # 等待移动线程完成
    move_thread.join()

    # 设置事件标志，通知东向调整线程结束
    stop_event.set()

    # 等待东向调整线程完成
    east_thread.join()
    stop_event.clear()
    stop_event.clear()
    logger.info("所有线程结束.")

if __name__ == "__main__":
    main_threading()
