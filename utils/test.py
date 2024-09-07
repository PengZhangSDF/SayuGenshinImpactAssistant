import cv2
import numpy as np
import logging
import time
import pyautogui

logger = logging.getLogger(__name__)


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


def CompareWithin_Continue(path_small, sim_num=0.75, notify=True, timesmax=200):
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
        # 使用 screenshot_function() 截取当前屏幕并转换为 BGR 格式
        img_a = screenshot_function_forCW()

        # 模板匹配
        q = time.time()
        result_matrix = cv2.matchTemplate(img_a, img_b, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_matrix)
        w = time.time()

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


