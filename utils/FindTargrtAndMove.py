import time
import cv2
import numpy as np
from utils.GIautogui import GIautogui as pydirectinput
from mss import mss
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:FindTargrtAndMove.py:当前工作目录：", os.getcwd())

def main(img='./DailyImg/WEITUO2.png', Adjustment=True):
    def capture_screen():
        with mss() as sct:
            monitor = sct.monitors[0]  # 选择正确的显示器
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def find_template(template, img):
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < 0.8:  # 设置匹配度阈值为0.8
            return None
        else:
            return max_loc

    def adjust_view(target_loc, screen_width):
        if target_loc is None:
            return  # 如果target_loc为None,则直接返回
        template_width = 50  # 你的图标模板的宽度
        template_center = target_loc[0] + template_width // 2
        move_x = (template_center - screen_width // 2) * 0.5
        pydirectinput.moveRel(int(move_x), 0, relative=True)
        return move_x

    time.sleep(0.1)
    template_img = cv2.imread(img, cv2.IMREAD_COLOR)
    cv2.waitKey(1000)
    while True:
        img = capture_screen()
        target_loc = find_template(template_img, img)
        if target_loc is None:  # 如果找不到目标元素
            print("未找到目标元素,程序停止")
            return False
        move_x = adjust_view(target_loc, img.shape[1])
        if -2 <= move_x <= 2 and Adjustment is True:
            return True
        time.sleep(0.1)  # 添加一些延迟


def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def find_and_align(target_image_path, screenshot):
    target_img = cv2.imread(target_image_path, cv2.IMREAD_COLOR)
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 使用SIFT特征提取
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(target_gray, None)
    kp2, des2 = sift.detectAndCompute(screenshot_gray, None)

    # 使用FLANN匹配器
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # 如果匹配数少于4个点，认为没有匹配区域
    if len(good_matches) < 4:
        return None

    # 获取匹配点的坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

    # 使用单应性矩阵进行变换
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    h, w = target_img.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    # 计算中心点
    center = np.mean(dst, axis=0).reshape(-1)

    # 在截图中绘制匹配区域
    screenshot_with_box = cv2.polylines(screenshot, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('Matches', screenshot_with_box)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return center

def adjust_view(target_loc, screen_width):
    if target_loc is None:
        return  # 如果target_loc为None,则直接返回
    template_width = 50  # 你的图标模板的宽度
    template_center = target_loc[0] + template_width // 2
    move_x = (template_center - screen_width // 2) * 0.5
    pydirectinput.moveRel(int(move_x), 0, relative=True)
    return move_x

def main_2():
    screenshot = capture_screen()
    screen_width = screenshot.shape[1]
    target_loc = find_and_align('./img/adventure.png', screenshot)
    move_x = adjust_view(target_loc, screen_width)
    if target_loc is not None:
        print(f"Moved view by {move_x} pixels.")
    else:
        print("Target image not found in the screenshot.")

