import subprocess
import time

# 启动程序
process = subprocess.Popen(["./yap/yap.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 等待一段时间后停止程序
time.sleep(30)  # 例如，等待10秒

# 停止程序
process.terminate()
