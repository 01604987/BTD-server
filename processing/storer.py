import csv
import threading
import queue
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration
import os

data_folder = "./data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print("Initialized data directory")

dc:DC = None

raw_signal = "./data/raw_signal.csv"
processed_signal = "./data/processed_signal.csv"
orientation_data = "./data/processed_orientation.csv"

def store_imu(data):
    with dc.accel_list_lock:
        dc.imu_raw.append(data)
        dc.imu_raw.pop(0)

def store_orientation(data):
    with dc.orientation_lock:
        dc.orientation.append(data)
        dc.orientation.pop(0)
    
    to_csv(data, orientation = True)

def store_linear_accel(data):
    with dc.linear_accel_lock:
        dc.linear_accel.append(data)
        dc.linear_accel.pop(0)

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

    path = raw_signal


    if kwargs.get('raw'):
        path = raw_signal
    
    if kwargs.get('filtered'):
        path = processed_signal
    
    if kwargs.get('orientation'):
        path = orientation_data


    with open(path, mode ='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

#deprecated do not use
def flush():
    for el in dc.accel_raw:
        to_csv(el, False)

    for el in dc.accel_processed:
        to_csv(el, True)


# fetch queue elements for processing and push to in memory/csv store
def start(exit:threading.Event, data_collection:DC):
    global dc
    dc = data_collection
    while not exit.is_set():
        try:
            raw = dc.data_q.get(block= True, timeout=5)
        except queue.Empty:
            print("queue empty, terminating thread")
            #store(raw, raw = True)
            #store(proccessed, raw = False)
            break

        #proccessed = raw
        store_imu(raw)
        orientation = complementary_filter.estimate_orientation([raw[0], raw[1], raw[2]], [raw[3], raw[4], raw[5]])
        store_orientation(orientation)
        linear_accel = linear_acceleration.free_linear_acceleration([raw[0], raw[1], raw[2]], orientation)
        store_linear_accel(linear_accel)
        #store(raw, True)

        # todo preprocess raw signal
        #store(proccessed, False)
    
