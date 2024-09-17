import os

import Check_TODO
import pydirectinput
import AutoReward
import subprocess
import UpDateGame
import utils.WhichPage
from utils import Tools
import StartGenshin
import AutoEnigma
import quit
from utils import  waiting_finish
import AutoDailyMission
import time
# from utils.threading_control import yuanshen_pause
import pyautogui as Mo
from utils import ScreenCompare as Sc
"""欢迎使用GI GenshinImpact Python源码
    这段文字帮助你理解代码结构
    不要理解了，反正写的差"""
def run_GIA():
    a = 0
    times = 0
    while a == 0 and times < 4:
        Windows = Tools.get_most_similar_window_title('GenshinImpactAssistant')
        Tools.windows_top(Windows)
        time.sleep(2)
        x, y = Sc.CompareWithin('./img/GIA.png',checkGenshin=False)
        Mo.click(x=x, y=y)
        time.sleep(1)
        a, b = Sc.CompareWithin('./img/GIAweituo.png',sim_num=0.9,checkGenshin=False)
        c, d = Sc.CompareWithin('./img/GIAqidong.png',checkGenshin=False)
        times = times + 1
        if a != 0:
            Mo.click(a,b)
            time.sleep(1)
            Mo.click(c,d)
    Windows = Tools.get_most_similar_window_title('原神')
    Tools.windows_top(Windows)
    Mo.click(50,500)
    Mo.click(1840,500)
    Mo.click(900,20)
    Mo.click(900,1000)
    utils.WhichPage.take_to_page('main')
    time.sleep(5)
    # 等待GIA完成，完全等待时间可以设置
    waiting_finish.waiting()
    try:
        pid = str(Tools.get_window_process_pid('GenshinImpactAssistant'))
        os.popen(f'taskkill -f -pid {pid} ')
    except:
        pass

    return mission

def str_to_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()  # 去除前后空格并转为小写
        if value in {"true", "yes", "1"}:
            return True
        elif value in {"false", "no", "0"}:
            return False
    raise ValueError(f"Cannot convert {value} to boolean")


# 日志文件相关设置
IFStartGenshin = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'startGenshin'))
IFCheck_schedule = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'check_schedule'))
IFRun_Enigma = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'run_Enigma'))
IFQ_Run_Enigma = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'q_run_Enigma'))
IFRun_daily_mission = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'run_daily_mission'))
IFGet_reward = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'get_reward'))
IFRun_GIA = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'run_gia'))
IFUpdate = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'update'))
IFQuit_Genshin = str_to_bool(Tools.read_config_value('./config.txt', 'Run', 'quit_genshin'))
IFDecompose_Relics = str_to_bool(Tools.read_config_value('./config.txt','Enigma','decompose_relics'))
IFSkip_Auto_Daily_Program = str_to_bool(Tools.read_config_value('./config.txt','AutoDaily','skip_auto_daily_program'))
from Package.log_config import logger, FILE_NAME
logger.info(f'日志输出：{FILE_NAME}')
if IFRun_GIA:
    GIA_path = Tools.get_variable_value('gia_path')
    logger.info(f'启动GIA:{GIA_path}')
    try:
        subprocess.Popen(GIA_path)
    except OSError:
        logger.critical('请填写GIA路径')
        logger.critical('请正确填写GIA路径')
        logger.critical('不要尝试填写py文件等不可直接运行的文件')
        exit()

pydirectinput.moveRel(50, 50)
time.sleep(8)
# 更新游戏
if IFUpdate:
    a = UpDateGame.UpDateGame()
    logger.info(f'游戏更新完成,包含以下游戏：{a}')
# 启动原神
if IFStartGenshin:
    yuanshen_path = Tools.get_variable_value('yuanshen_path')
    try:
        subprocess.Popen(yuanshen_path)
    except OSError:
        logger.critical('请填写原神路径')
        logger.critical('请正确填写原神路径')
        logger.critical('请不要尝试填写其他路径')
        exit()
    logger.info(f'启动原神{yuanshen_path}')
    logger.info('启动原神')
    # 原神启动模块
    StartGenshin.Start()

# 检查进度
if IFCheck_schedule:
    run_Enigma, run_daily = Check_TODO.checktodo()
    print(run_Enigma, run_daily)
    if not run_Enigma:
        logger.warning('体力低于20,体力模块将不启动')
else:
    run_Enigma = True
    run_daily = True

# 每日委托启动相关
if run_daily and IFRun_daily_mission:
    # if not run_Enigma or run_Enigma is not True:
    #     BGI_path = Tools.get_variable_value('bgi_path')
    #     os.popen(BGI_path)
    logger.info('启动每日委托')
    from StartGenshin import ocr
    if not IFSkip_Auto_Daily_Program:
        mission = AutoDailyMission.auto_daily_mission()
        logger.info(mission)
    else:
        mission = ['程序内置委托模块跳过']
    if IFRun_GIA:
        run_GIA()
        mission_result = False
else:
    mission = ['每日委托完成，本次运行跳过']
    mission_result = True
logger.info(mission)

if IFRun_Enigma:
    if run_Enigma or IFQ_Run_Enigma:
        logger.info('寻找秘境')
        time.sleep(2)

        # 秘境寻找模块

        result = AutoEnigma.start()
        if not result:
            utils.WhichPage.take_to_page('main')
            logger.error('自动秘境启动失败!')

        time.sleep(5)
        # 秘境战斗模块
        result = AutoEnigma.run()
        if not result:
            utils.WhichPage.take_to_page('main')
            logger.error('自动秘境运行中断!')
        # 返回蒙德，否则OCR识别会出错 原神4.7更新
        if IFDecompose_Relics:
            result = AutoEnigma.decompose_relics()
        AutoEnigma.back_to_home()
        time.sleep(1)
ocr.exit()
if IFGet_reward:
    logger.info('开始领取奖励')
    reward = AutoReward.GetReward()
    time.sleep(5)
if IFQuit_Genshin:
    logger.info('退出原神')
    result = quit.genshin_quit(FILE_NAME, mission)
    logger.info(result)
os.popen('taskkill -f -im PaddleOCR-json.exe')
exit()