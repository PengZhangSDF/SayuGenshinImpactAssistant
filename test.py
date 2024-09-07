import cv2
import numpy as np
import pyautogui
import time

def screenshot_function_forCW(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    if x2 <= x1 or y2 <= y1:
        raise ValueError("Invalid region coordinates")

    # 截图指定部分
    try:
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    except OSError:
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    # 将截图转换为 OpenCV 格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return screenshot_cv

def perform_feature_matching(target_image_mat, template_image_mat, threshold=0.8, draw_on_window=False):
    if template_image_mat is None or target_image_mat is None:
        raise ValueError("Template image or target image is not set.")

    # 将目标图像转换为灰度图
    target_image_gray = cv2.cvtColor(target_image_mat, cv2.COLOR_BGR2GRAY)

    # 创建 ORB 特征检测器
    orb = cv2.ORB_create()

    # 计算目标图像和模板图像的特征点和描述符
    kp_target, des_target = orb.detectAndCompute(target_image_gray, None)
    kp_template, des_template = orb.detectAndCompute(template_image_mat, None)

    # 打印特征点和描述符
    if des_target is None or des_template is None:
        print("Descriptor computation failed for one or both images.")
        return None

    print(f"Number of keypoints in target image: {len(kp_target)}")
    print(f"Number of keypoints in template image: {len(kp_template)}")

    # 使用 BFMatcher 进行描述符匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_template, des_target)

    # 过滤匹配结果
    good_matches = [m for m in matches if m.distance <= threshold]

    if not good_matches:
        print("No good matches found.")
        return None  # 没有匹配

    # 计算匹配点的中心坐标
    points = np.array([kp_target[m.trainIdx].pt for m in good_matches])
    center_x = np.mean(points[:, 0])
    center_y = np.mean(points[:, 1])

    # 绘制匹配结果
    if draw_on_window:
        matching_result = target_image_mat.copy()
        matching_result = cv2.drawKeypoints(matching_result, kp_target, None, color=(0, 255, 0), flags=0)
        cv2.imshow("Matches", matching_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return (int(center_x), int(center_y))

# 使用示例
template_image_path = "./img/mjend.png"
template_image = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

# 获取屏幕截图
target_image_mat = screenshot_function_forCW(x1=0, y1=0, x2=1920, y2=1080)

# 进行特征匹配
center = perform_feature_matching(target_image_mat, template_image, threshold=0.8, draw_on_window=True)

if center:
    print(f"Template found at center coordinates: {center}")
else:
    print("Template not found.")
