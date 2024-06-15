import csv
import threading
import queue
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration, filter, calculate_input
import os

data_folder = "./data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print("Initialized data directory")

dc:DC = None

raw_signal = "./data/raw_signal.csv"
processed_signal = "./data/processed_signal.csv"
orientation_data = "./data/processed_orientation.csv"
linear_data = "./data/linear.csv"

def store_imu(data, filtered = False):

    if not filtered:
        with dc.imu_list_lock:
            dc.imu_raw.append(data)
            dc.imu_raw.pop(0)
            to_csv(data, raw =1)

    else :
        with dc.imu_list_filtered_lock:
            dc.imu_filtered.append(data)
            dc.imu_filtered.pop(0)
            to_csv(data, filtered = 1)

def store_velo(data) :
    dc.velocity.append(data)
    dc.velocity.pop(0)

def store_orientation(data):
    with dc.orientation_lock:
        dc.orientation.append(data)
        dc.orientation.pop(0)


def store_linear_accel(data):
    with dc.linear_accel_lock:
        dc.linear_accel.append(data)
        dc.linear_accel.pop(0)
        to_csv(data, linear = 1)

# push data into in memory list and persist to csv
def store(data, raw = False):

    if raw:
        with dc.accel_list_lock:
            dc.accel_raw.append(data)
            dc.accel_raw.pop(0)
    else:
        with dc.accel_list_lock:
            dc.accel_processed.append(data)
            dc.accel_processed.pop(0)

    to_csv(data, raw = raw)

# persist to csv for alternative processing 
def to_csv(data, **kwargs):

    path = ""


    if kwargs.get('raw'):
        path = raw_signal
    
    if kwargs.get('filtered'):
        path = processed_signal
    
    if kwargs.get('orientation'):
        path = orientation_data
    if kwargs.get("linear"):
        path = linear_data


    with open(path, mode ='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def start_new(exit:threading.Event, data_collection:DC, mouse_event:threading.Event = None):
    global dc
    dc = data_collection

    while not exit.is_set():
        try:
            mouse_event.wait()
            raw = dc.data_q.get(block= True, timeout=5)
        #TODO! QUEUE MUST BE EMPTY when switching between mouse events
        except queue.Empty:
            if exit.is_set():
                print("queue empty and server shutting down, terminating thread")
                break
            if mouse_event.is_set():
                print("!!!! Queue empty during mouse events !!!!")
                continue

        store_imu(raw)
        orientation = complementary_filter.estimate_orientation([raw[0], raw[1], raw[2]], [raw[3], raw[4], raw[5]])
        store_orientation(orientation)
        linear_accel = linear_acceleration.free_linear_acceleration([raw[0], raw[1], raw[2]], orientation)
        store_linear_accel(linear_accel) 
        x = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 0 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames)
        y = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 1 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames)
        z = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 2 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames)
        filtered = (x, y, z, raw[3], raw[4], raw[5])
        store_imu(filtered, 1)

# fetch queue elements for processing and push to in memory/csv store
def start(exit:threading.Event, data_collection:DC,  events: dict[str, threading.Event]):
    global dc
    dc = data_collection

    while not exit.is_set():
        try:
            events.get("stream").wait()
            raw = dc.data_q.get(block= True, timeout=5)
        #TODO! QUEUE MUST BE EMPTY when switching between udp and tcp
        except queue.Empty:
            print("queue empty, terminating thread")
            break

        #proccessed = raw
        store_imu(raw)

        orientation = complementary_filter.estimate_orientation([raw[0], raw[1], raw[2]], [raw[3], raw[4], raw[5]])
        store_orientation(orientation)
        linear_accel = linear_acceleration.free_linear_acceleration([raw[0], raw[1], raw[2]], orientation)
        store_linear_accel(linear_accel)
        
        x = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 0 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames)
        y = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 1 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames)
        z = filter.bandpass_second_order(dc.imu_filtered, dc.linear_accel, axis = 2 , n_out = dc.in_memory_frames, n_in=dc.in_memory_frames) * 0

        filtered = (x, y, z, raw[3], raw[4], raw[5])
        store_imu(filtered, 1)
        vx = calculate_input.calc_velocity(filtered, dc.velocity, 0, dc.in_memory_frames)
        vy = calculate_input.calc_velocity(filtered, dc.velocity, 1, dc.in_memory_frames)
        velo = (vx, vy, 0, raw[3], raw[4], raw[5])
        store_velo(velo)

        if events.get("mouse").is_set():
            calculate_input.move(orientation)
        elif events.get("volume").is_set():
            calculate_input.ctrl_volume(orientation, dc.orientation[dc.in_memory_frames - 2])
        elif events.get("zoom").is_set():
            calculate_input.ctrl_zoom(orientation)
    
