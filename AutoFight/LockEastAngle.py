import time
import cv2
import numpy as np
from PIL import ImageGrab
from utils.GIautogui import GIautogui as pydirectinput
import configparser
import os
import config
import threading
from Package.log_config import logger
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)
stop_event = threading.Event()

# 打印当前工作目录
logger.info(f"FindTree.py:当前工作目录：{os.getcwd()}")
def find_peaks(data):
    peak_indices = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            peak_indices.append(i)
    return peak_indices


def right_shift(array, k):
    return np.concatenate((array[-k:], array[:-k]))


def left_shift(array, k):
    return np.concatenate((array[k:], array[:k]))


def shift(array, k):
    if k > 0:
        return right_shift(array, k)
    else:
        return left_shift(array, -k)


def compute_orientation(grey_image):
    # 截取小地图区域
    mat = grey_image[19:231, 62:274]  # Rect(62, 19, 212, 212)

    # 高斯模糊
    mat = cv2.GaussianBlur(mat, (3, 3), 0)

    # 极坐标展开
    center_point = (mat.shape[1] // 2, mat.shape[0] // 2)
    polar_mat = cv2.warpPolar(mat, (360, 360), center_point, 360, cv2.INTER_LINEAR + cv2.WARP_POLAR_LINEAR)

    # 提取感兴趣区域并旋转
    polar_roi_mat = polar_mat[:, 10:80]
    polar_roi_mat = cv2.rotate(polar_roi_mat, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Scharr算子计算
    scharr_result = cv2.Scharr(polar_roi_mat, cv2.CV_32F, 1, 0)

    # 寻找波峰
    array = scharr_result.flatten()
    left_peaks = find_peaks(array)
    right_peaks = find_peaks(-array)

    # 统计波峰
    left = np.zeros(360, dtype=int)
    right = np.zeros(360, dtype=int)
    for peak in left_peaks:
        left[peak % 360] += 1
    for peak in right_peaks:
        right[peak % 360] += 1

    # 优化波峰数据
    left2 = np.maximum(left - right, 0)
    right2 = np.maximum(right - left, 0)

    # 计算综合波峰数据
    sum = np.zeros(360, dtype=int)
    for i in range(-2, 3):
        all_values = left2 * shift(right2, -90 + i) * (3 - abs(i)) // 3
        sum += all_values

    # 卷积计算最终结果
    result = np.zeros(360, dtype=int)
    for i in range(-2, 3):
        all_values = shift(sum, i) * (3 - abs(i)) // 3
        result += all_values

    # 计算结果角度
    max_index = np.argmax(result)
    angle = max_index + 45
    if angle > 360:
        angle -= 360

    return angle


def capture_screen_greyscale():
    # 截取整个屏幕
    screen = ImageGrab.grab()

    # 将图像转换为灰度图像
    grey_image = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)

    return grey_image


# 示例用法



def move_view(xOffset, duration=0.5):
    pydirectinput.moveRel(int(xOffset), 0, duration=duration, relative=True)

def get_current_angle():
    grey_image = capture_screen_greyscale()
    angle = compute_orientation(grey_image)
    return angle

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

def read_offset_per_degree_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'Enigma' in config and 'offset_per_degree' in config['Enigma']:
        try:
            return config.getfloat('Enigma', 'offset_per_degree')
        except ValueError:
            return None
    return None

def save_offset_per_degree_to_config(config_file, offset_per_degree):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'Enigma' not in config:
        config['Enigma'] = {}
    config['Enigma']['offset_per_degree'] = str(offset_per_degree)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def adjust_view_to_east():
    config_file = './config.txt'
    offset_per_degree = read_offset_per_degree_from_config(config_file)

    if offset_per_degree is None:
        offset_per_degree = calculate_offset_per_degree()
        save_offset_per_degree_to_config(config_file, offset_per_degree)

    while True:
        current_angle = get_current_angle()
        if current_angle >= 355 or current_angle <= 5:
            pass
        if current_angle < 180:
            xOffset = -current_angle * offset_per_degree
        else:
            xOffset = (360 - current_angle) * offset_per_degree

        move_view(xOffset)
        time.sleep(0.1)





def adjust_view_to_east_once():
    config_file = './config.txt'
    offset_per_degree = read_offset_per_degree_from_config(config_file)

    if offset_per_degree is None:
        offset_per_degree = calculate_offset_per_degree()
        save_offset_per_degree_to_config(config_file, offset_per_degree)


    current_angle = get_current_angle()
    if current_angle >= 355 or current_angle <= 5:
        pass

    if current_angle < 180:
        xOffset = -current_angle * offset_per_degree
    else:
        xOffset = (360 - current_angle) * offset_per_degree

    move_view(xOffset)
    time.sleep(0.1)

