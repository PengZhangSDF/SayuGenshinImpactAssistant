import time

import cv2
import numpy as np
import mss
from ultralytics import YOLO
import win32gui, win32ui, win32api, win32con
import os
import config
path = config.get_config_directory()
import Package.log_config
logger = Package.log_config.logger
os.chdir(path)

# 打印当前工作目录
logger.info("FindTree.py:当前工作目录：", os.getcwd())
# 加载训练好的YOLOv8模型
model = YOLO('./AutoFight/best.pt')
model.to('cpu')

# 初始化屏幕截图工具
sct = mss.mss()
class RectangleDrawer:
    def __init__(self):
        self.dc = win32gui.GetDC(0)
        self.dcObj = win32ui.CreateDCFromHandle(self.dc)
        self.hwnd = win32gui.WindowFromPoint((0, 0))
        self.past_coordinates = None

    def draw_rectangle(self, x1, y1, x2, y2, color=(255, 0, 0)):
        if self.past_coordinates:
            self.clear_previous_rectangle()

        red = win32api.RGB(*color)

        rect = win32gui.CreateRoundRectRgn(x1, y1, x2, y2, 2, 2)
        win32gui.RedrawWindow(self.hwnd, (x1, y1, x2, y2), rect, win32con.RDW_INVALIDATE)

        for x in range(x1, x2):
            win32gui.SetPixel(self.dc, x, y1, red)
            win32gui.SetPixel(self.dc, x, y2, red)
        for y in range(y1, y2):
            win32gui.SetPixel(self.dc, x1, y, red)
            win32gui.SetPixel(self.dc, x2, y, red)

        self.past_coordinates = (x1, y1, x2, y2)

    def clear_previous_rectangle(self):
        x1, y1, x2, y2 = self.past_coordinates
        rect = win32gui.CreateRoundRectRgn(x1, y1, x2, y2, 2, 2)
        win32gui.RedrawWindow(self.hwnd, (x1, y1, x2, y2), rect, win32con.RDW_INVALIDATE)


def find_tree(sct):
    time.sleep(0.1)
    # 获取屏幕尺寸
    monitor = sct.monitors[0]
    drawer = RectangleDrawer()
    # 捕获整个屏幕
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)

    # 将图像从BGRA转换为RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

    # 使用模型进行预测
    results = model(frame)

    # 遍历检测结果
    for result in results:
        boxes = result.boxes.xyxy  # 边界框坐标
        labels = result.boxes.cls  # 标签
        scores = result.boxes.conf  # 置信度

        for box, label, score in zip(boxes, labels, scores):
            # 确认标签是否为树
            if result.names[int(label)] == 'tree':
                x1, y1, x2, y2 = map(int, box)
                drawer.draw_rectangle(x1=x1, y1=y1, x2=x2, y2=y2)

                # 获取树的中心横坐标
                tree_x = (x1 + x2) // 2

                # 打印树的中心横坐标和边界框坐标
                logger.info(f"Tree中心坐标: {tree_x}, 方框坐标: ({x1}, {y1}, {x2}, {y2})")
                return tree_x
            else:
                return None
if __name__ == '__main__':
    sct = mss.mss()
    result = find_tree(sct)
    logger.info(result)