# screenshot.py
import pyautogui
from time import strftime

def take_screenshot():
    timestamp = strftime("%Y-%m-%d_%H-%M-%S")
    path = f"logs/screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
