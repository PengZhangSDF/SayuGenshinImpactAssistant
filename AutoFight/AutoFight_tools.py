import time
# -*- coding: utf-8 -*-


import cv2
import numpy as np
from mss import mss
import config
import os
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
def adjust_brightness_threshold(brightness_avg, base_brightness=100):
    # 根据屏幕当前亮度动态调整亮度阈值
    if brightness_avg < 100:  # 假设 100 为默认屏幕亮度
        return base_brightness - (100 - brightness_avg)  # 根据亮度降低调整阈值
    else:
        return base_brightness

def is_vibrant(x1=1785, y1=934, x2=1854, y2=1002, saturation_threshold=50, brightness_threshold=200):
    # 截取屏幕指定区域
    with mss() as sct:
        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        screenshot = np.array(sct.grab(monitor))

    # 转换为 HSV 色彩空间
    hsv_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # 获取饱和度(S)和亮度(V)通道
    saturation = hsv_image[:, :, 1]
    brightness = hsv_image[:, :, 2]

    # 计算亮度的平均值
    avg_brightness = np.mean(brightness)

    # 动态调整亮度阈值
    adjusted_brightness_threshold = adjust_brightness_threshold(avg_brightness, brightness_threshold)

    # 计算饱和度的平均值
    avg_saturation = np.mean(saturation)

    # 基于调整后的亮度和饱和度判断是否色彩绚丽
    return avg_saturation > saturation_threshold and avg_brightness > adjusted_brightness_threshold
# 示例使用
if __name__ == '__main__':
    x1, y1, x2, y2 = 1785, 934, 1854, 1002
    result = is_vibrant(x1, y1, x2, y2)
    print("色彩绚丽:", result)