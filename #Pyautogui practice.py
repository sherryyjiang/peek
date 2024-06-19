#Pyautogui practice

import pyautogui
import time

time.sleep(5)

# Ensure failsafe is enabled
pyautogui.FAILSAFE = True

pyautogui.moveTo(500, 500, duration=1)

pyautogui.click()

pyautogui.moveRel(100, 0, duration=1)  # Move 100 pixels to the right from the current position
