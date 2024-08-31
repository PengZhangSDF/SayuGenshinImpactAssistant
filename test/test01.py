from utils.threading_control import yuanshen_pause
import test02
def a():
    test02.b()

yuanshen_pause(a,title_='计算器')