import time
import Package.log_config

import Mission.Daily_ProductOrderAll
import Mission.Daily_qqMansOneStep01
import Mission.Daily_TheWayWoReward
import Mission.Daily_RoundEazyBoom
import Mission.Daily_qqMansOneStep02
import Mission.Daily_MengDeBeerPeople
import Mission.Daily_RoundEazyBoom02
import Mission.Daily_AdventurersLimitAbility
import Mission.Daily_IrenesFutureKnight
import Mission.Daily_Impregnable
import Mission.Daily_ClimbHighIsDangerous02
import Mission.Daily_qqMansOneStep03
import Mission.Daily_NoOneNoticeGY
import Mission.Daily_MissionAtCriticalMoment02
import Mission.Daily_WineryCleaning2
import Mission.Daily_ClimbHighIsDangerous01
import Mission.Daily_Impregnable02
import Mission.Daily_RoadIsBlock01
import Mission.Daily_RoundBigRush
import Mission.Daily_ClimbHighIsDangerous03
import Mission.Daily_LanguageExchange01
import Mission.Daily_FatherCanDo
import Mission.Daily_MissionAtCriticalMoment
import utils.WhichPage

from utils import auto_fight_threading
from utils import ScreenCompare as Sc, MouseKey as Mo
import Package.CalibrateMap
import pydirectinput
from utils.GIautogui import GIautogui as pyautogui
import os
import config
path = config.get_config_directory()
from utils.Tools import read_config_value
# 更改工作目录为脚本所在目录
os.chdir(path)
logger = Package.log_config.logger
# 打印当前工作目录
def auto_daily_mission():
    def mission_compare():
        mission = []
        result = False
        if not result:
            pyautogui.press('j')
            time.sleep(1)
            x, y = Sc.CompareWithin('./img/HomeOfDaily.png')
            if x != 0:
                Mo.click_mouse('left', x=x, y=y)
            time.sleep(1)
            # 语言交流_坠星山谷
            a, b = Sc.CompareWithin('./DailyImg/LanguageExchange02.png')
            c, d = Sc.CompareWithin('./DailyImg/LanguageExchange01.png')
            if a != 0 and c != 0:
                mission1 = '语言交流_坠星山谷'
                mission.append(mission1)
            # 钥匙是易丢品_晨曦酒庄
            a, b = Sc.CompareWithin('./img/KeyIsEasyToLose.png')
            c, d = Sc.CompareWithin('./img/KeyIsEasyToLose2.png')
            if a != 0 and c != 0:
                mission1 = '钥匙是易丢品_晨曦酒庄'
                mission.append(mission1)
            # 冒险家能力极限
            a, b = Sc.CompareWithin('./img/AdventurersLimitAbility.png')
            if a != 0:
                mission0 = '冒险家能力极限'
                mission.append(mission0)
            time.sleep(0.1)
            # 父亲能做的事
            a, b = Sc.CompareWithin('./img/FatherCanDo.png')
            if a != 0:
                mission0 = '父亲能做的事'
                mission.append(mission0)
            # 无人注意的盖伊
            a, b = Sc.CompareWithin('./img/NoOneNoticeGY01.png')
            c, d = Sc.CompareWithin('./img/NoOneNoticeGY02.png')
            if a != 0 or c != 0:
                mission0 = '无人注意的盖伊'
                mission.append(mission0)
            # 清洁大扫除2
            a, b = Sc.CompareWithin('./img/WineryCleaning2.png')
            if a != 0:
                mission0 = '清洁大扫除2'
                mission.append(mission0)
            # 蒙德酒客
            a, b = Sc.CompareWithin('./img/MengDeBeerPeople.png',0.8)
            c, d = Sc.CompareWithin('./img/MengDeBeerPeople02.png',0.8)
            if a != 0 or c != 0:
                mission0 = '蒙德酒客'
                mission.append(mission0)
            # 艾琳，未来的骑士
            a, b = Sc.CompareWithin('./img/IrenesFutureKnight.png')
            if a != 0:
                mission0 = '艾琳，未来的骑士'
                mission.append(mission0)
            # 报答神明的方式识别
            a, b = Sc.CompareWithin('./DailyImg/TheWayToReward03.png', 0.6)
            if a != 0:
                mission1 = '报答神明的方式'
                mission.append(mission1)
            a, b = Sc.CompareWithin('./img/ProductOrder.png',0.9)
            # 餐品预定识别
            if a != 0:
                mission1 = '餐品预定'
                mission.append(mission1)
            pyautogui.press('Esc')
            a, b = Sc.CompareWithin('./img/ThatMansHelp.png')
            c, d = Sc.CompareWithin('./DailyImg/ThatMansHelp02.png')
            if a != 0 and c != 0:
                mission1 = '那位先生的委托'
                mission.append(mission1)
            time.sleep(2)
            # 丘丘人的一小步识别模块
            Package.CalibrateMap.open_map()
            time.sleep(1)
            Sc.screenshot_function(706, 970, 792, 1055)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '丘丘人的一小步_晨曦酒庄'
                mission.append(mission2)
            # 丘丘人的一小步03
            Sc.screenshot_function(1149,332,1207,392)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '丘丘人的一小步_低语森林'
                mission.append(mission2)
            # 诗歌交流
            Sc.screenshot_function(1497,636,1560,700)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '诗歌交流'
                mission.append(mission2)
            # 圆滚滚的打团骚乱识别01
            Sc.screenshot_function(977, 431, 1027, 481)
            result = Sc.compare_image('./DailyImg/MissionRoundBigRush01.png')
            if result:
                mission2 = '圆滚滚的大团骚乱_蒙德城'
                mission.append(mission2)
            # 攀高危险_风起地
            Sc.screenshot_function(1148,921,1198,971)
            result = Sc.compare_image('./DailyImg/ClimbHighIsDangerous01.png')
            if result:
                mission2 = '攀高危险_风起地'
                mission.append(mission2)
            # 攀高危险_明冠山地
            Sc.screenshot_function(144,744,194,794)
            result = Sc.compare_image('./img/climbhighisdangerous.png')
            if result:
                mission2 = '攀高危险_明冠山地'
                mission.append(mission2)
            # 圆滚滚的易爆品_风起地
            Sc.screenshot_function(1405,1036,1465,1079)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '圆滚滚的易爆品_风起地'
                mission.append(mission2)
            # 此路不通_苍风高地
            Sc.screenshot_function(833, 955, 913, 1045)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '此路不通_苍风高地'
                mission.append(mission2)
            # 丘丘人的一小步02 风龙废墟
            pydirectinput.moveTo(800, 500)
            Mo.drag_mouse('left', 1000)
            Mo.drag_mouse('up', 500)
            time.sleep(0.2)
            Sc.screenshot_function(600, 555, 630, 585)
            result = Sc.compare_image('./img/weituo3030.png', 0.8)
            if result:
                mission3 = '丘丘人的一小步_风龙废墟'
                mission.append(mission3)
            pyautogui.FAILSAFE = False
            time.sleep(1)
            pydirectinput.moveTo(1200, 1000)
            Mo.drag_mouse('right', 1000)
            time.sleep(0.5)
            Mo.drag_mouse('down', 900)
            pydirectinput.moveTo(500, 1000)
            Mo.drag_mouse('down', 800)
            time.sleep(1)
            a, b = Sc.CompareWithin('./img/RoundEasyBoom.png', 0.95)
            if a != 0:
                mission4 = '圆滚滚的易爆品'
                mission.append(mission4)
            a, b = Sc.CompareWithin('./DailyImg/MissionAtCriticalMoment01.png', sim_num=0.95)
            if a != 0:
                mission5 = '临危受命_达达乌帕谷'
                mission.append(mission5)
            Sc.screenshot_function(1511,669,1581,729)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '临危受命_达达乌帕谷2'
                mission.append(mission2)
            Sc.screenshot_function(1379,310,1449,380)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission2 = '攀高危险_风啸山坡'
                mission.append(mission2)
            pydirectinput.moveTo(500, 1000)
            Mo.drag_mouse('down', 800)
            pydirectinput.moveTo(500, 1000)
            time.sleep(1)
            # 固若金汤_龙脊雪山_南
            a, b = Sc.CompareWithin('./img/GuRuoJinTang.png')
            if a != 0:
                mission1 = '固若金汤_龙脊雪山_南'
                mission.append(mission1)
            # 固若金汤_龙脊雪山_西
            Sc.screenshot_function(728,407,788,467)
            result = Sc.CompareWithin_Noscreenshot('./DailyImg/WEITUO.png')
            if result:
                mission1 = '固若金汤_龙脊雪山_西'
                mission.append(mission1)
            pyautogui.FAILSAFE = True
            pyautogui.press('Esc')
            return mission

    # 读取配置文件中的 times 值
    times = int(read_config_value('./config.txt', 'AutoDaily', 'found_times'))

    # 初始化一个空列表来存储每次 mission_compare 的结果
    missions = []

    # 进行 times 次 mission_compare
    for _ in range(times):
        mission = mission_compare()
        missions.append(mission)
        time.sleep(1)

    # 使用 set 计算并集
    mission_union = set()
    for mission in missions:
        mission_union |= set(mission)

    # 将结果转换回列表（如果需要）
    mission = list(mission_union)
    logger.info(mission_union)

    pyautogui.press('F11')
    logger.info(mission)
    result = True

    for task in mission:
        if task == '报答神明的方式':
            result = Mission.Daily_TheWayWoReward.the_way_to_reward()
        elif task == '艾琳，未来的骑士':
            Mission.Daily_IrenesFutureKnight.IrenesFutureKnight()
        elif task == '清洁大扫除2':
            Mission.Daily_WineryCleaning2.WineryCleaning2()
        #elif task == '那位先生的委托':                           此委托废弃2024.8.15
            #Daily_ThatMansHelp02.daily_thatmanshelp()
        elif task == '无人注意的盖伊':
            result = Mission.Daily_NoOneNoticeGY.NoOneNoticeGY()
        elif task == '丘丘人的一小步_晨曦酒庄':
            result = Mission.Daily_qqMansOneStep01.qqMansOneStep01()
        elif task == '语言交流_坠星山谷':
            Mission.Daily_LanguageExchange01.LanguageExchange01()
        elif task == '攀高危险_风起地':
            result = Mission.Daily_ClimbHighIsDangerous01.ClimbHighIsDangerous()
        elif task == '钥匙是易丢品_晨曦酒庄':
            pass
        elif task == '餐品预定':
            result = Mission.Daily_ProductOrderAll.product_order()
        elif task == '固若金汤_龙脊雪山_西':
            Mission.Daily_Impregnable.Impregnable01()
        elif task == '丘丘人的一小步_风龙废墟':
            result = Mission.Daily_qqMansOneStep02.qqmansonestep02()
        elif task == '圆滚滚的易爆品':
            result = Mission.Daily_RoundEazyBoom.roundeazyboom()
        elif task == '冒险家能力极限':
            result = Mission.Daily_AdventurersLimitAbility.AdventuresLimitAbility()
        elif task == '圆滚滚的大团骚乱_蒙德城':
            result = Mission.Daily_RoundBigRush.RoundBigrush01()
        elif task == '父亲能做的事':
            result = Mission.Daily_FatherCanDo.FatherCanDO()
        elif task == '临危受命_达达乌帕谷':
            result = Mission.Daily_MissionAtCriticalMoment.MissionAtCM()
        elif task == '攀高危险_明冠山地':
            result = Mission.Daily_ClimbHighIsDangerous02.ClimbHighIsDangerous02()
        elif task == '此路不通_苍风高地':
            result = Mission.Daily_RoadIsBlock01.TheRoadIsBlock()
        elif task == '攀高危险_风啸山坡':
            result = Mission.Daily_ClimbHighIsDangerous03.ClimbHighIsDangerous03()
        elif task == '临危受命_达达乌帕谷2':
            result = Mission.Daily_MissionAtCriticalMoment02.MissionAtCM02()
        elif task == '固若金汤_龙脊雪山_南':
            result = Mission.Daily_Impregnable02.Impregnable02()
        elif task == '丘丘人的一小步_低语森林':
            result = Mission.Daily_qqMansOneStep03.qqMansOneStep03()
        elif task == '蒙德酒客':
            result = Mission.Daily_MengDeBeerPeople.MengDeBeerPeople()
        elif task == '圆滚滚的易爆品_风起地':
            result = Mission.Daily_RoundEazyBoom02.RoundEazyBoom02()
        else:
            mission.append('没有可以运行的委托')
        auto_fight_threading.stop_auto_fight_config()
    if not result:
        mission.append('每日委托出现错误，任务中止')
        utils.WhichPage.take_to_page('main')
    logger.info('委托执行完成')
    utils.WhichPage.take_to_page('main')
    time.sleep(1)
    Package.CalibrateMap.teleport(960, 543)
    time.sleep(5)
if __name__ == '__main__':
    auto_daily_mission()