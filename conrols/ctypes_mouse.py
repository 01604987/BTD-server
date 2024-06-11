import ctypes
import time

# Load user32.dll for Windows API calls
user32 = ctypes.windll.user32

# Function to move the mouse to (x, y)
def move_mouse(x, y):
    user32.SetCursorPos(x, y)

def move_mouse_relative(dx, dy):
    ctypes.windll.user32.mouse_event(0x0001, ctypes.c_long(dx), ctypes.c_long(dy), 0, 0)
