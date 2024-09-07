import pyautogui
import pydirectinput
import time
import win32gui

class GenshinAutoGUI:
    def __init__(self):
        self.keydown_state = {}
        self.FAILSAFE = False
        if not self.FAILSAFE:
            pyautogui.FAILSAFE = False
    def is_genshin_focused(self):
        hwnd = win32gui.GetForegroundWindow()
        window_text = win32gui.GetWindowText(hwnd)
        return '原神' in window_text

    def wait_for_focus(self):
        while not self.is_genshin_focused():
            time.sleep(5)

    def keyDown(self, key):
        self.wait_for_focus()
        pyautogui.keyDown(key)
        self.keydown_state[key] = True

    def keyUp(self, key):
        self.wait_for_focus()
        pyautogui.keyUp(key)
        self.keydown_state[key] = False

    def press(self, key):
        self.wait_for_focus()
        pyautogui.press(key)

    def hotkey(self, *keys):
        self.wait_for_focus()
        pyautogui.hotkey(*keys)

    def moveTo(self, x, y, duration=0.0):
        self.wait_for_focus()
        pyautogui.moveTo(x, y, duration)

    def click(self, x=None, y=None, clicks=1, interval=0.0, button='left', duration=0.0):
        self.wait_for_focus()
        pyautogui.click(x, y, clicks, interval, button,duration=duration)

    def pause_if_necessary(self):
        # This method will be called to check if any key was held down before pausing
        for key, state in self.keydown_state.items():
            if state:
                pyautogui.keyDown(key)

    def moveRel(self, xOffset, yOffset, duration=0.5, relative=True):
        """注意：此处使用pydirectinput"""
        self.wait_for_focus()
        pydirectinput.moveRel(xOffset, yOffset,duration=duration,relative=relative)

    def scroll(self, clicks, x, y):
        self.wait_for_focus()
        pyautogui.scroll(clicks=clicks, x=x, y=y)

    def mouseDown(self):
        self.wait_for_focus()
        pyautogui.mouseDown()

    def mouseUp(self):
        self.wait_for_focus()
        pyautogui.mouseUp()

    def drag(self, x, y, duration=0.5):
        self.wait_for_focus()
        pyautogui.drag(x, y, duration=duration)

GIautogui = GenshinAutoGUI()
# from utils.GIautogui import GIautogui as pyautogui

