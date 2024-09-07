import threading
import time
from AutoFight import AutoFightConfig
stop_event = threading.Event()
def main_threading():
    AutoFightConfig.main()
def start_auto_fight_config():
    # 启动 AutoFightConfig.main() 的线程
    stop_event.clear()
    auto_fight_thread = threading.Thread(target=main_threading)
    auto_fight_thread.start()
    return auto_fight_thread

def stop_auto_fight_config():
    AutoFightConfig.stop()  # 调用 AutoFightConfig.stop()
    stop_event.clear()  # 清除停止事件

# 用法
# import utils.auto_fight_threading
# auto_fight_threading = utils.auto_fight_threading.start_auto_fight_config()
# utils.auto_fight_threading.stop_auto_fight_config()
# auto_fight_threading.join()


if __name__ == "__main__":
    time.sleep(1)
    auto_fight_thread = start_auto_fight_config()

    # 等待一段时间，模拟其他工作
    time.sleep(5)

    stop_auto_fight_config()
    auto_fight_thread.join()  # 确保线程结束
    # 多次调用
    time.sleep(3)
    auto_fight_thread = start_auto_fight_config()

    # 等待一段时间，模拟其他工作
    time.sleep(5)

    stop_auto_fight_config()
    auto_fight_thread.join()  # 确保线程结束
