import csv
import threading
import queue
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration, filter
import os

data_folder = "./data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print("Initialized data directory")

dc:DC = None

raw_signal = "./data/raw_signal.csv"
processed_signal = "./data/processed_signal.csv"
orientation_data = "./data/processed_orientation.csv"

def store_imu(data, filtered = False):

    if not filtered:
        with dc.imu_list_lock:
            dc.imu_raw.append(data)
            dc.imu_raw.pop(0)
            to_csv(data, raw = 'raw')

    else :
        with dc.imu_list_filtered_lock:
            dc.imu_filtered.append(data)
            dc.imu_filtered.pop(0)
    

def store_orientation(data):
    with dc.orientation_lock:
        dc.orientation.append(data)
        dc.orientation.pop(0)


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

    path = ""


    if kwargs.get('raw'):
        path = raw_signal
    
    if kwargs.get('filtered'):
        path = processed_signal
    
    if kwargs.get('orientation'):
        path = orientation_data


    with open(path, mode ='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)



# fetch queue elements for processing and push to in memory/csv store
def start(exit:threading.Event, data_collection:DC):
    global dc
    dc = data_collection

    input_coeff = [0.08613, 0.08613]
    output_coeff = [0.82773]

    x_prev = 0
    y_prev = 0
    z_prev = 0
    while not exit.is_set():
        try:
            raw = dc.data_q.get(block= True, timeout=5)
        except queue.Empty:
            print("queue empty, terminating thread")
            #store(raw, raw = True)
            #store(proccessed, raw = False)
            break

#TODO think about new thread for filtering 
        #proccessed = raw
        store_imu(raw)
        
        x_acc = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][0], raw[0], dc.imu_raw[dc.in_memory_frames - 1][0], input_coeff, output_coeff)


        # prev_output is currently last entry of imu_filtered
        # current_input is current raw reading
        # prev_input is currently second last entry of imu_filtered because new raw has been stored already
        x_acc_hpf = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][0], raw[0], dc.imu_raw[dc.in_memory_frames - 2][0], hpf=True)
        #x_acc_bandpass = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][0], x_acc_hpf, x_prev_in, hpf=False)
        x_acc_bandpass = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][0], x_acc, x_prev, hpf=False)

        y_acc = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][1], raw[1], dc.imu_raw[dc.in_memory_frames - 1][1], input_coeff, output_coeff)
        
        y_acc_hpf = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][1], raw[1], dc.imu_raw[dc.in_memory_frames - 2][1], hpf=True)
        y_acc_bandpass = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][1], y_acc, y_prev, hpf=False)

        z_acc = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][2], raw[2], dc.imu_raw[dc.in_memory_frames - 1][2], input_coeff, output_coeff)

        z_acc_hpf = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][2], raw[2], dc.imu_raw[dc.in_memory_frames - 2][2], hpf=True)
        z_acc_bandpass = filter.applyFilter_x(dc.imu_filtered[dc.in_memory_frames - 1][2], z_acc, z_prev, hpf=False)

        
        x_gyr = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][3], raw[3], dc.imu_raw[dc.in_memory_frames - 1][3], input_coeff, output_coeff)
        y_gyr = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][4], raw[4], dc.imu_raw[dc.in_memory_frames - 1][4], input_coeff, output_coeff)
        z_gyr = filter.applyFilter(dc.imu_filtered[dc.in_memory_frames - 1][5], raw[5], dc.imu_raw[dc.in_memory_frames - 1][5], input_coeff, output_coeff)


        x_prev = x_acc_hpf
        y_prev = y_acc_hpf
        z_prev = z_acc_hpf

        filtered = (x_acc_bandpass, y_acc_bandpass, z_acc_bandpass, x_gyr, y_gyr, z_gyr)
        store_imu(filtered, 1)

        orientation = complementary_filter.estimate_orientation([raw[0], raw[1], raw[2]], [raw[3], raw[4], raw[5]])
        #orientation = complementary_filter.estimate_orientation([x_acc, y_acc, z_acc], [x_gyr, y_gyr, z_gyr])
        store_orientation(orientation)
        linear_accel = linear_acceleration.free_linear_acceleration([raw[0], raw[1], raw[2]], orientation)
        #linear_accel = linear_acceleration.free_linear_acceleration([x_acc_bandpass, y_acc_bandpass, z_acc_bandpass], orientation)
        store_linear_accel(linear_accel)
        #store(raw, True)

        # todo preprocess raw signal
        #store(proccessed, False)
    
