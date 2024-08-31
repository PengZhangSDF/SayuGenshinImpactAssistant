import cv2
import numpy as np
import os
import json

import utils.ScreenCompare


def load_existing_records(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []


def save_teleport_points(file_path, teleport_points):
    with open(file_path, 'w') as f:
        json.dump(teleport_points, f, indent=4)


def is_similar(region1, region2, threshold=0.99):
    # 使用均方误差（MSE）比较两张图片的相似度
    if region1.shape != region2.shape:
        return False
    mse = np.mean((region1 - region2) ** 2)
    return mse < (1 - threshold) * 255 ** 2


def find_teleport_points(screenshot_path, templates, file_path='teleport_points.json', feature_area=50,
                         min_distance=10):
    screenshot = cv2.imread(screenshot_path)

    # 加载现有记录
    teleport_points = load_existing_records(file_path)
    used_points = [tuple(point["coordinates"]) for point in teleport_points]
    last_point = used_points[-1] if used_points else None

    for template_name, template_path in templates.items():
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            too_close = False
            for used_pt in used_points:
                if np.linalg.norm(np.array(pt) - np.array(used_pt)) < min_distance:
                    too_close = True
                    break

            if too_close:
                continue

            top_left_x = max(pt[0] - feature_area // 2, 0)
            top_left_y = max(pt[1] - feature_area // 2, 0)
            bottom_right_x = min(pt[0] + template.shape[1] + feature_area // 2, screenshot.shape[1])
            bottom_right_y = min(pt[1] + template.shape[0] + feature_area // 2, screenshot.shape[0])

            region = screenshot[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

            similar = False
            for point in teleport_points:
                recorded_region = np.array(point["feature"])
                if is_similar(region, recorded_region):
                    similar = True
                    break

            if similar:
                continue

            identifier = f"{template_name}_{len([p for p in teleport_points if p['id'].startswith(template_name)]) + 1:03}"
            relative_coords = (int(pt[0] - last_point[0]), int(pt[1] - last_point[1])) if last_point else (0, 0)

            teleport_points.append({
                "id": identifier,
                "coordinates": (int(pt[0]), int(pt[1])),
                "relative_coordinates": relative_coords,
                "feature": region.tolist()
            })

            used_points.append(pt)
            last_point = pt

    save_teleport_points(file_path, teleport_points)


def genshin_tp(identifier, file_path='teleport_points.json'):
    teleport_points = load_existing_records(file_path)
    for point in teleport_points:
        if point["id"] == identifier:
            return point["coordinates"]
    return None


# 示例使用
templates = {
    "Buddha": "./img/Buddha.png",
    "Enigma01": "./img/enigma01.png",
    "Enigma02": "./img/enigma02.png",
    "TeleportPoint": "./img/teleport_point.png"
}
utils.ScreenCompare.screenshot_function(checkGenshin=False)
find_teleport_points('screenshot.png', templates)
coords = genshin_tp('Buddha002')
if coords:
    print(f"坐标: {coords}")
else:
    print("未找到指定的 Buddha")
