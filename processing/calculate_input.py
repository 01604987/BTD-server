import threading
import math
from controls import control_driver
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration, filter
import time

def move(current_orientation):
    x_null = 2
    y_null = 2

    x = 0
    y = 0
    o = current_orientation
    if abs(o[1]) > x_null:
        x = exponential_transfer(normalize_input(o[1]))
        x = round(normalize_output(x))
        # determine x axis mouse movement
        # non inverted
        if o[1] < 0:
            x = -x
    if abs(o[0]) > y_null:
        y = exponential_transfer(normalize_input(o[0]))
        y = round(normalize_output(y))
        # determine y axis mouse movement 
        # inverted
        if o[0] < 0:
            y = -y
    
    # calculate next x, y movement
    control_driver.move_mouse_relative(x, y)

def ctrl_volume(current_orientation, last_orientation):

    roll = current_orientation[1]

    if (abs(roll-last_orientation[1]) <= 1):
        return
    
    curr_vol = linear_transform(roll, -85, 85, 0, 1, True)

    control_driver.volume(curr_vol)
        
last_time = 0

def ctrl_zoom(current_orientation, last_orientation):
    global last_time

    current_time = time.time()
    if current_time - last_time >= 0.08:
        roll = current_orientation[0]
        last_roll = last_orientation[0]

        delta = round((roll - last_roll))
        delta = max(-1 , delta) if delta < 0 else min(1, delta) if delta > 0 else 0 

        control_driver.zoom(delta)   

        last_time = current_time

def calc_velocity(acceleration, velocity, axis, n = 3000, time_step = 1/100 ):
    velocity = velocity[n-1][axis] + acceleration[axis] * time_step
    return velocity

def linear_transform(input, in_min, in_max, out_min, out_max, clamp=True):

    y = ( (input - in_min) * (out_max - out_min) ) / (in_max - in_min) + out_min

    if clamp:
        y = out_max if y > out_max else out_min if y < out_min else y

    return y

def normalize_input(input, in_min= 10, in_max = 90):

    out = (abs(input) - in_min) / (in_max - in_min)

    return out

def normalize_output(input, in_min= 1, in_max =  math.e, out_min = 1, out_max = 10):
    out = out_min + (input - in_min) * ((out_max - out_min)/(in_max - in_min))
    return out

def exponential_transfer(x):
    return math.exp(x * 3)