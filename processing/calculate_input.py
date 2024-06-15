import threading
import math
from controls import ctypes_mouse
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration, filter

# 0 - 90
# += 10 is 0 
# scale factor 1.0
# 45 deg == normal 
def start(exit:threading.Event, dc:DC, mouse_events:threading.Event):
    x_null = 4
    y_null = 4
    while(not exit.is_set()):
        mouse_events.wait()

        x = 0
        y = 0

        with dc.orientation_lock:
            o = dc.orientation[dc.in_memory_frames - 1]
        if abs(o[0]) > x_null:
            x = exponential_transfer(normalize_input(o[0]))
            x = round(normalize_output(x))
            if o[0] < 0:
                x = -x
        if abs(o[1]) > y_null:
            y = exponential_transfer(normalize_input(o[1]))
            y = (normalize_output(y))
            if o[1] < 0:
                y = -y
        
        # calculate next x, y movement
        ctypes_mouse.move_mouse_relative(x, y)

def move(current_orientation):
    x_null = 4
    y_null = 4

    x = 0
    y = 0
    o = current_orientation
    if abs(o[1]) > x_null:
        x = exponential_transfer(normalize_input(o[1]))
        x = round(normalize_output(x))
        if o[1] < 0:
            x = -x
    if abs(o[0]) > y_null:
        y = exponential_transfer(normalize_input(o[0]))
        y = round(normalize_output(y))
        if o[0] < 0:
            y = -y
    
    # calculate next x, y movement
    ctypes_mouse.move_mouse_relative(x, y)

def ctrl_volume(current_orientation):
    print(current_orientation)
        
def ctrl_zoom(current_orientation):
    print(current_orientation)

def calc_velocity(acceleration, velocity, axis, n = 3000, time_step = 1/100 ):
    velocity = velocity[n-1][axis] + acceleration[axis] * time_step
    return velocity


def normalize_input(input, in_min= 10, in_max = 90):

    out = (abs(input) - in_min) / (in_max - in_min)

    return out

def normalize_output(input, in_min= 1, in_max =  math.e, out_min = 1, out_max = 15):
    out = out_min + (input - in_min) * ((out_max - out_min)/(in_max - in_min))
    return out

def exponential_transfer(x):
    return math.exp(x)