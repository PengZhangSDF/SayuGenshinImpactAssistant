import time

import numpy as np
import pyautogui
import cv2
from Package.log_config import logger
import os
import config
import win32gui
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:ScreenCompare.py:当前工作目录：", os.getcwd())

def is_genshin_focused():
    hwnd = win32gui.GetForegroundWindow()
    window_text = win32gui.GetWindowText(hwnd)
    return '原神' in window_text


def wait_for_focus():
    while not is_genshin_focused():
        print('非原神窗口，操作暂停 5 秒')
        time.sleep(5)


def screenshot_function(x1=0, y1=0, x2=1920, y2=1080, checkGenshin=True):
    if checkGenshin:
        wait_for_focus()
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    if x2 <= x1 or y2 <=y1:
        logger.error('x1,x2或者y1,y2值不符合预期')

    # 截图指定部分
    try:
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    except OSError:
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 保存为PNG格式
    cv2.imwrite('./screenshot.png', screenshot_cv)

    return screenshot_cv


def compare_image(image, sim_num=0.9, pprint=True, checkGenshin=True):
    if checkGenshin:
        wait_for_focus()
    # 读取两个图像
    image1 = cv2.imread('./screenshot.png')
    image2 = cv2.imread(image)

    # 将图像转换为灰度图像
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算SSIM
    ssim = cv2.SIFT_create()
    kp1, des1 = ssim.detectAndCompute(gray_image1, None)
    kp2, des2 = ssim.detectAndCompute(gray_image2, None)

    # 比较描述符
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 计算相似度
    similar_points = 0
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # 设定阈值
            similar_points += 1

    if len(matches) > 0:
        similarity = similar_points / len(matches)
    else:
        similarity = 0.0  # 或者其他适当的处理方式

    if pprint:
        logger.info(f"Similarity: {similarity},设定值{sim_num}")

    if similarity > sim_num:
        return True
    else:
        return False


# 使用示例
# image_comparator = ImageComparator()
# path_to_image = 'your_image_path.jpg'
# result = image_comparator.compare_images(path_to_image, x1, y1, x2, y2)
# print(result)


# 打印当前工作目录
# print("AutoEnigma.py:当前工作目录：", os.getcwd())
def screenshot_function_forCW(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    if x2 <= x1 or y2 <=y1:
        logger.error('x1,x2或者y1,y2值不符合预期')

    # 截图指定部分
    try:
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    except OSError:
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return screenshot_cv

def CompareWithin(path_small, sim_num=0.75, notify=False,checkGenshin=True):
    if checkGenshin:
        wait_for_focus()
    # 使用 screenshot_function() 截取当前屏幕并转换为 BGR 格式
    img_a = screenshot_function_forCW()

    # 读取小图像文件
    img_b = cv2.imread(path_small, cv2.IMREAD_UNCHANGED)

    # 确保尺寸关系：a.png 尺寸大于 b.png
    try:
        if img_a.shape[0] < img_b.shape[0] or img_a.shape[1] < img_b.shape[1]:
            logger.error(f"Error: 图片 {path_small} 尺寸应该大于当前屏幕截图")
            return 0, 0
    except AttributeError:
        logger.error('请确认文件路径')
        return 0, 0

    # 模板匹配
    result = cv2.matchTemplate(img_a, img_b, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = sim_num  # 设定阈值
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + img_b.shape[1], top_left[1] + img_b.shape[0])
        target_center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        if notify:
            logger.info(f"{path_small} 包含当前屏幕截图. 中心坐标: {target_center}")
        x, y = target_center
        return x, y
    else:
        if notify:
            logger.warning(f"{path_small} 不存在于当前屏幕截图在相似度 {sim_num} 下.")
        return 0, 0


# time.sleep(5)
# CompareWithin('./img/screenshot.png','./img/CBKJDLR.png')
def CompareWithin_Noscreenshot(path_small, sim_num=0.75, notify=False,checkGenshin=True):
    """不截图识别screenshot的元素
        -->bool"""
    if checkGenshin:
        wait_for_focus()
    path_big = './screenshot.png'
    # 读取图像文件
    img_a = cv2.imread(path_big, cv2.IMREAD_UNCHANGED)
    img_b = cv2.imread(path_small, cv2.IMREAD_UNCHANGED)

    # 确保尺寸关系：a.png 尺寸大于 b.png
    try:
        if img_a.shape[0] < img_b.shape[0] or img_a.shape[1] < img_b.shape[1]:
            logger.error(f"Error: Image {path_small} should be larger than image {path_big}")
    except AttributeError:
        logger.error('请确认文件路径')
        exit()
    else:
        # 模板匹配
        result = cv2.matchTemplate(img_a, img_b, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = sim_num  # 设定阈值
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + img_b.shape[1], top_left[1] + img_b.shape[0])
            target_center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
            if notify:
                logger.info(f"{path_small} 包含 {path_big}.中心坐标: {target_center}")
            x, y = target_center
            return True
        else:
            if notify:
                logger.warning(f"{path_small}不存在于 {path_big}在相似度 {sim_num}下..")
            return False



class ScreenCount:
    def __init__(self, screenshot_path):
        screenshot_function()
        self.screenshot = cv2.imread(screenshot_path)
        if self.screenshot is None:
            raise ValueError(f"Cannot open screenshot file: {screenshot_path}")

    def quantity(self, template_path, sim_sum=0.9):
        template = cv2.imread(template_path, 0)
        if template is None:
            raise ValueError(f"Cannot open template file: {template_path}")

        screenshot_gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= sim_sum)
        return len(list(zip(*loc[::-1])))

    def location(self, template_path, sim_sum=0.9):
        template = cv2.imread(template_path, 0)
        if template is None:
            raise ValueError(f"Cannot open template file: {template_path}")

        screenshot_gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= sim_sum)
        points = list(zip(*loc[::-1]))

        # To avoid overlapping points, let's filter out close matches
        filtered_points = []
        for pt in points:
            if not any(np.linalg.norm(np.array(pt) - np.array(fp)) < min(w, h) for fp in filtered_points):
                filtered_points.append(pt)

        # Convert points to bounding box coordinates (top-left and bottom-right)
        bounding_boxes = [(pt[0], pt[1], pt[0] + w, pt[1] + h) for pt in filtered_points]

        # Sort the bounding boxes from top-left to bottom-right
        bounding_boxes.sort(key=lambda x: (x[1], x[0]))

        return bounding_boxes


def CompareWithin_Continue(path_small, sim_num=0.75, notify=False, timesmax=200,checkGenshin=True):
    if checkGenshin:
        wait_for_focus()
    # 读取小图像文件
    img_b = cv2.imread(path_small, cv2.IMREAD_UNCHANGED)

    # 确保图像文件正确加载
    if img_b is None:
        logger.error(f"Error: 无法读取图片 {path_small}")
        return 0, 0, False

    # 初始化变量
    result = False
    times = 0
    x, y = 0, 0
    img_a = screenshot_function_forCW()
    try:
        if img_a.shape[0] < img_b.shape[0] or img_a.shape[1] < img_b.shape[1]:
            logger.error(f"Error: 图片 {path_small} 尺寸应该大于当前屏幕截图")
            return 0, 0, False
    except AttributeError:
        logger.error('请确认文件路径')
        return 0, 0, False
    while not result and times < timesmax:
        # 截取当前屏幕并转换为 BGR 格式
        img_a = screenshot_function_forCW()

        # 模板匹配
        result_matrix = cv2.matchTemplate(img_a, img_b, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_matrix)

        threshold = sim_num  # 设定阈值
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + img_b.shape[1], top_left[1] + img_b.shape[0])
            target_center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
            if notify:
                logger.info(f"{path_small} 包含当前屏幕截图. 中心坐标: {target_center}")
            x, y = target_center
            result = True
        else:
            if notify:
                logger.warning(f"{path_small} 不存在于当前屏幕截图在相似度 {sim_num} 下.")
            times += 1

    return x, y