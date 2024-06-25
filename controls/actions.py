import pyautogui
import time

def next_slide():
    pyautogui.press('right')

def previous_slide():
    pyautogui.press('left')

# DEPRECATED beyond this point

def double_click():
    # Double click
    pyautogui.doubleClick()

def click():
    pyautogui.click()

def move_mouse_right(x, y):
    pyautogui.move(x, y)
    
def move_mouse_smoothly(start_point, end_point, duration=1):
    # Calculate the distance to move in each axis
    delta_x = end_point[0] - start_point[0]
    delta_y = end_point[1] - start_point[1]
    
    # Calculate the number of steps based on duration and screen refresh rate
    steps = int(duration * pyautogui.MINIMUM_DURATION / pyautogui.MINIMUM_SLEEP)
    #steps = int(duration * 100)

    # Calculate the step increments for x and y
    step_x = delta_x / steps
    step_y = delta_y / steps

    # Move the mouse smoothly
    for i in range(steps):
        x = start_point[0] + step_x * i
        y = start_point[1] + step_y * i
        pyautogui.moveTo(x, y, duration=pyautogui.MINIMUM_DURATION)

    # Measure time to move the mouse
def measure_move_time(x, y):
    start_time = time.time()
    move_mouse_right(x, y)
    end_time = time.time()
    return end_time - start_time

def drag_and_drop(start_x, start_y, drop_x, drop_y):
    # Move to starting position
    pyautogui.moveTo(start_x, start_y)

    # Press the mouse button
    pyautogui.mouseDown()

    # Move to the drop destination
    pyautogui.moveTo(drop_x, drop_y)

    # Release the mouse button
    pyautogui.mouseUp()