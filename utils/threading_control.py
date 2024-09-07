import ctypes
import sys
import threading
import time
import win32gui
import Package.log_config
logger = Package.log_config.logger


def get_foreground_window_title():
    window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(window)
    return window_title


class _MyThread(threading.Thread):
    def __init__(self, target=None, args=(), kwargs=None, daemon=True):
        super(_MyThread, self).__init__(target=target, args=args, kwargs=kwargs, daemon=daemon)
        self.flag = threading.Event()

    def stop(self):
        logger.info(f'停止线程{self.name}')
        if not self.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)
        if res == 0:
            raise ValueError('找不到线程ID')
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError('线程已停止')



class MyThread(threading.Thread):
    dict = [{"kill": False} for i in range(1000)]

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True, dict_={}):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  args=args, kwargs=kwargs, daemon=daemon)
        if dict_:
            self.killed = dict_
        else:
            self.killed = {"kill": False}
        self._return = None

    def start(self):
        logger.info(f'开启线程{self}')
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed["kill"]:
            if event == 'line':
                if self.killed["kill"] == 1:
                    raise SystemExit
                elif self.killed["kill"] == 2:
                    while self.killed["kill"]:
                        time.sleep(0.1)
        return self.localtrace

    def stop(self):
        logger.info(f'停止线程{self}')
        self.killed["kill"] = 1

    def pause(self):
        logger.info(f'暂停线程{self}')
        self.killed["kill"] = 2

    def resume(self):
        logger.info(f"恢复线程{self}")
        self.killed["kill"] = False

    def join(self, *args, **kwargs):
        threading.Thread.join(self, *args, **kwargs)
        return self._return


def test_func():
    for i in range(10):
        time.sleep(0.1)
        print(i)
    return True,False

def yuanshen_pause(func,args=(),title_ = '原神'):
    start = True
    main_thread = MyThread(target=func,args=args)
    main_thread.start()
    while main_thread.is_alive():
        title = get_foreground_window_title()
        if title == title_:
            if not start:
                main_thread.resume()
                start = True
        else:
            if start:
                main_thread.pause()
                start = False
            if not start:
                time.sleep(2)
                logger.info(f"非{title_}窗口，暂停操作")
    return main_thread.join()

if __name__ == '__main__':
    result = yuanshen_pause(test_func)
    print(f"Function returned: {result}")

