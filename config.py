import os

def get_config_directory():
    # 获取当前文件(config.py)的目录路径
    config_directory = os.path.dirname(os.path.abspath(__file__))
    return config_directory

if __name__ == "__main__":
     # 测试输出 config.py 的目录路径
     print(get_config_directory())
