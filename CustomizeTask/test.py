# -*- coding: utf-8 -*-

import time
import math
import pydirectinput
import cvAutoTrack.cvAutoTrack
import config
import os
import configparser
import numpy as np
from Package.log_config import logger

path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 初始化auto_tracker
auto_tracker = cvAutoTrack.cvAutoTrack.AutoTracker()

def get_current_angle():
    success, angle_of_view = auto_tracker.get_rotation()
    if success:
        return angle_of_view
    return None

def move_view(xOffset, duration=0.5):
    pydirectinput.moveRel(int(0-xOffset), 0, duration=duration, relative=True)

def adjust_view_to_angle(target_angle, offset_per_degree, tolerance=1.0):
    while True:
        current_angle = get_current_angle()
        if current_angle is None:
            logger.error("Failed to get current angle.")
            return False

        angle_difference = target_angle - current_angle

        # 确保角度差在[-180, 180]范围内
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        # 如果在误差范围内，则停止调整
        if abs(angle_difference) <= tolerance:
            logger.debug(f"Current angle: {current_angle}, Target angle: {target_angle}, Angle difference: {angle_difference}")
            logger.debug(f"Angle is within tolerance of {tolerance} degrees.")
            break

        xOffset = angle_difference * offset_per_degree
        move_view(xOffset)

        logger.debug(f"当前角度: {current_angle}, 目标角度: {target_angle}, 角度差: {angle_difference}")
        logger.debug(f"调整位移 {xOffset} pixels to align with target angle {target_angle}.")
        time.sleep(0.5)  # 等待视角调整完成

    return True

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
            logger.info("Error: No angle movement detected.")
            return initial_xOffset_per_degree  # 使用初始估计值

        move_view(-xOffset)
        time.sleep(0.1)

    return np.mean(offsets)

def test_view_adjustment():
    # 计算每度偏移值
    offset_per_degree = calculate_offset_per_degree()
    logger.info(f"Calculated offset per degree: {offset_per_degree}")

    # 测试转向0度
    logger.info("Testing view adjustment to 0 degrees")
    adjust_view_to_angle(0, offset_per_degree)
    time.sleep(2)

    # 测试转向90度
    logger.info("Testing view adjustment to 90 degrees")
    adjust_view_to_angle(90, offset_per_degree)
    time.sleep(2)

    # 测试转向180度
    logger.info("Testing view adjustment to 180 degrees")
    adjust_view_to_angle(180, offset_per_degree)
    time.sleep(2)

    # 测试转向-90度
    logger.info("Testing view adjustment to -90 degrees")
    adjust_view_to_angle(-90, offset_per_degree)
    time.sleep(2)

    # 测试转向-179度
    logger.info("Testing view adjustment to -179 degrees")
    adjust_view_to_angle(-179, offset_per_degree)
    time.sleep(2)

    # 测试转向179度
    logger.info("Testing view adjustment to 179 degrees")
    adjust_view_to_angle(179, offset_per_degree)
    time.sleep(2)

if __name__ == "__main__":
    time.sleep(5)  # 等待5秒以便进入游戏窗口
    test_view_adjustment()