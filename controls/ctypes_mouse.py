import ctypes


# Load user32.dll for Windows API calls
user32 = ctypes.windll.user32


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# Function to move the mouse to (x, y)
def move_mouse(x, y):
    user32.SetCursorPos(x, y)

def move_mouse_relative(dx, dy):
    user32.mouse_event(0x0001, ctypes.c_long(dx), ctypes.c_long(dy), 0, 0)

def hold_lmb():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

# Function to release the left mouse button
def release_lmb():
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)