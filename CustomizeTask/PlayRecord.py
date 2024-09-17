# -*- coding: utf-8 -*-

import json
import time
import math
import pydirectinput
import cvAutoTrack.cvAutoTrack
import config
import threading
import os
import configparser
import numpy as np
from Package.log_config import logger

path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
stop_event = threading.Event()

# 初始化auto_tracker
auto_tracker = cvAutoTrack.cvAutoTrack.AutoTracker()

def calculate_offset_per_degree():
    initial_xOffset_per_degree = 10
    test_angle = 10
    offsets = []

    for _ in range(3):
        initial_angle = get_current_angle()
        target_angle = (initial_angle + test_angle) % 360

        if target_angle > 180:
            xOffset = -test_angle * initial_xOffset_per_degree
        else:
            xOffset = test_angle * initial_xOffset_per_degree

        move_view(xOffset)
        time.sleep(0.5)
        new_angle = get_current_angle()
        actual_angle_moved = abs(new_angle - initial_angle)

        if actual_angle_moved != 0:
            offset_per_degree = xOffset / actual_angle_moved
            offset_per_degree = abs(offset_per_degree)
            offsets.append(offset_per_degree)
        else:
            logger.info("错误：未检测到角度移动。")
            return initial_xOffset_per_degree  # 使用初始估计值

        move_view(-xOffset)
        time.sleep(0.1)

    return np.mean(offsets)

def read_offset_per_degree_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'Enigma' in config and 'offset_per_degree' in config['Enigma']:
        try:
            return config.getfloat('Enigma', 'offset_per_degree')
        except ValueError:
            return None
    return None

def get_current_position():
    success, x, y, arrow_angle = auto_tracker.get_transform()
    if success:
        return x, y, arrow_angle
    return None, None, None

def get_current_angle():
    success, angle_of_view = auto_tracker.get_rotation()
    if success:
        return angle_of_view
    return None

def move_view(xOffset, duration=0.5):
    pydirectinput.moveRel(int(0 - xOffset), 0, duration=duration, relative=True)

def calculate_target_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle = math.degrees(math.atan2(delta_y, delta_x))
    # 将角度转换到 [-180, 180] 范围内
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360
    return angle

def adjust_view_to_angle(target_angle, offset_per_degree, tolerance=1.0):
    while True:
        current_angle = get_current_angle()
        if current_angle is None:
            logger.error("获取当前角度失败。")
            return False

        angle_difference = target_angle - current_angle

        # 确保角度差在[-180, 180]范围内
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        # 如果在误差范围内，则停止调整
        if abs(angle_difference) <= tolerance:
            logger.debug(f"当前角度: {current_angle}, 目标角度: {target_angle}, 角度差: {angle_difference}")
            logger.debug(f"角度在误差范围 {tolerance} 度内。")
            break

        xOffset = angle_difference * offset_per_degree  # 修正方向
        move_view(xOffset)

        logger.debug(f"当前角度: {current_angle}, 目标角度: {target_angle}, 角度差: {angle_difference}")
        logger.debug(f"调整视角 {xOffset} 像素以对齐目标角度 {target_angle}。")
        time.sleep(0.5)  # 等待视角调整完成

    return True

def move_forward():
    pydirectinput.keyDown('w')
    logger.debug("开始前进。")

def stop_moving():
    pydirectinput.keyUp('w')
    logger.debug("停止前进。")

def execute_action(action):
    if action == 'autofight':
        print('autofight')
        logger.info('执行自动战斗')
    elif action == 'click':
        pydirectinput.click()
        logger.info('鼠标点击')
    elif action == 't':
        pydirectinput.press('t')
        logger.info('按下键 t')

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def save_offset_per_degree_to_config(config_file, offset_per_degree):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'Enigma' not in config:
        config['Enigma'] = {}
    config['Enigma']['offset_per_degree'] = str(offset_per_degree)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def playback_actions(data, offset_per_degree):
    for i in range(len(data) - 1):
        x1, y1, _, _, action = data[i]
        x2, y2, _, _, _ = data[i + 1]

        logger.info(f"开始从 ({x1}, {y1}) 移动到 ({x2}, {y2})，执行动作 {action}")

        # 开始前进
        move_forward()

        # 持续调整视角并前进
        while True:
            current_x, current_y, _ = get_current_position()
            if current_x is None or current_y is None:
                logger.error("获取当前位置失败。")
                break

            # 计算当前位置和目标位置的距离
            distance = math.hypot(x2 - current_x, y2 - current_y)
            logger.debug(f"当前距离目标: {distance} 米。")

            # 如果距离小于10米，停止修正方向
            if distance <= 10:
                logger.debug("距离目标小于10米，停止角度调整。")
                break

            # 计算实时目标角度
            target_angle = calculate_target_angle(current_x, current_y, x2, y2)
            logger.debug(f"当前位置: ({current_x}, {current_y})，目标位置: ({x2}, {y2})，目标角度: {target_angle}")

            # 调整视角到目标方向
            if not adjust_view_to_angle(target_angle, offset_per_degree):
                logger.error("调整视角到目标角度失败。")
                break

            # 每隔1秒修正一次
            time.sleep(1)

        # 当距离到达阈值0.35时停止前进
        while True:
            current_x, current_y, _ = get_current_position()
            if current_x is None or current_y is None:
                logger.error("获取当前位置失败。")
                break

            distance = math.hypot(x2 - current_x, y2 - current_y)
            logger.debug(f"当前距离目标: {distance} 米。")

            if distance <= 0.35:
                logger.info(f"到达目标: ({x2}, {y2})")
                break

            # 持续前进
            time.sleep(0.1)

        # 停止前进
        stop_moving()

        # 执行当前路径点的操作
        execute_action(action)

def main():
    # 从配置文件读取每度偏移值
    config_file = './config.txt'
    offset_per_degree = read_offset_per_degree_from_config(config_file)
    if offset_per_degree is None:
        offset_per_degree = calculate_offset_per_degree()
        save_offset_per_degree_to_config(config_file, offset_per_degree)

    # 读取录制的JSON文件
    data = read_json_file('./CustomizeTask/game_record.json')

    # 回放记录的操作
    playback_actions(data, offset_per_degree)

if __name__ == "__main__":
    time.sleep(5)  # 等待5秒以便进入游戏窗口
    main()