import subprocess
from StartGenshin import ocr
import pyautogui
import cv2
import numpy as np
from Package.log_config import logger
import os
import config
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
print("utils:OCR.py:当前工作目录：", os.getcwd())
def screenshot_function(x1=0, y1=0, x2=1920, y2=1080):
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 截图指定部分
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # 将截图转换为OpenCV格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 保存为PNG格式
    cv2.imwrite('./screenshot.png', screenshot_cv)

    return screenshot_cv
# res = ocr.run('../test.png')

def call_main_exe(x1, y1, x2, y2):
    try:
        result = subprocess.run(["./ocr/ocr.exe", str(x1), str(y1), str(x2), str(y2)], capture_output=True, text=True)
    except FileNotFoundError:
        result = subprocess.run(["../ocr/ocr.exe", str(x1), str(y1), str(x2), str(y2)], capture_output=True, text=True)
    output_list = [item.replace('\n', '$') for item in result.stdout.split(',')]
    try:
        single_string = output_list[0]
    except IndexError:
        return ['Error:nothing is found in this area']
    else:
        split_list = single_string.split('$')
        print(split_list)
        return split_list


# a = call_main_exe(1641,29,1688,61)
# print(a)
def ppocr(x1=0, y1=0, x2=1920, y2=1080, model='all', path_to_img='../screenshot.png'):
    """识别截图或指定图片内的文字
        model = 'int'(返回图片内的数字[123,456])
              = 'all'(返回全部内容{'example','123'})
              = 'box and text'(返回值和坐标,返回{'example':(x1,x2,y1,y2)})                """


    logger.info("当前工作目录：%s", os.getcwd())
    return_list = []
    return_book = {}
    if path_to_img == '../screenshot.png':
        screenshot_function(x1,y1,x2,y2)
    res = ocr.run(path_to_img)
    logger.info(res)
    try:
        text_list = [item['text'] for item in res['data']]
    except TypeError:
        text_list = [f'在#{path_to_img}#里没有文本']
    # 创建所需的字典，坐标以整数形式存储

    if model == 'int':
        logger.debug(f'ppocr,model=int,list={text_list}')
        for text in text_list:
            try:
                result = float(text)
            except ValueError:
                continue
            except IndexError:
                continue
            except:
                logger.info('一个未知的错误导致OCR没有正常运行')
            else:
                return_list.append(result)
    elif model == 'box and text':
        for item in res['data']:
            try:
                text = item['text']
            except TypeError:
                return ['没有识别到文字']
            x1, y1 = item['box'][0]  # 左上角坐标
            x2, y2 = item['box'][2]  # 右下角坐标
            return_book[text] = (x1, y1, x2, y2)
        print(return_book)
        return return_book
    else:

        return_list = text_list
    logger.info(return_list)
    print(return_list)
    return return_list

