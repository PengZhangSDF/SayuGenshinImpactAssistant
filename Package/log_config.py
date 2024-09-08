import logging
import sys
import datetime
import os
import config

# 确保日志文件夹存在
path = config.get_config_directory()
os.makedirs(os.path.join(path, 'logs'), exist_ok=True)

# 获取当前时间并格式化文件名
current_time = datetime.datetime.now()
formatted_time = current_time.strftime('%Y年%m月%d日')
FILE_NAME = os.path.join(path, 'logs', formatted_time + '.txt')

def setup_logger():
    class Logger(object):
        def __init__(self, filename='default.log', stream=sys.stdout):
            self.terminal = stream
            try:
                self.log = open(filename, 'a')
            except Exception as e:
                print(f"无法打开日志文件: {e}")
                self.log = None

        def write(self, message):
            try:
                if self.terminal:
                    self.terminal.write(message)
                if self.log:
                    self.log.write(message)
            except Exception as e:
                print(f"日志写入失败: {e}")

        def flush(self):
            try:
                if self.terminal:
                    self.terminal.flush()
                if self.log:
                    self.log.flush()
            except Exception as e:
                print(f"日志刷新失败: {e}")

    class FileLoggerHandler(logging.Handler):
        def __init__(self, filename='default.log', stream=sys.stdout):
            super().__init__()
            self.logger_writer = Logger(filename, stream)

        def emit(self, record):
            try:
                msg = self.format(record)
                self.logger_writer.write(msg + '\n')
            except Exception as e:
                print(f"日志记录失败: {e}")

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            # 仅保留文件名而不是完整路径
            record.pathname = os.path.basename(record.pathname)
            return super().format(record)

    # 配置日志记录器
    formatter = CustomFormatter('[%(levelname)8s] %(pathname)s:%(lineno)d - %(message)s')
    file_logger_handler = FileLoggerHandler(FILE_NAME, sys.stdout)
    file_logger_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger_handler)

    # 只重定向 sys.stdout 和 sys.stderr 到文件，不影响其他日志输出
    sys.stdout = Logger(FILE_NAME, sys.stdout)
    sys.stderr = Logger(FILE_NAME, sys.stderr)

    return logger

logger = setup_logger()
