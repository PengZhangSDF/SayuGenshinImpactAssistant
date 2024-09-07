import time
import test02
import utils.auto_fight_threading
time.sleep(5)
utils.auto_fight_threading.start_auto_fight_config()
time.sleep(4)
test02.a()
time.sleep(10)
utils.auto_fight_threading.start_auto_fight_config()