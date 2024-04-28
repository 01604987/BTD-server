import csv
import threading
import queue
from processing.data_collection import DC
import os

data_folder = "./data"

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print("Initialized data directory")

dc:DC = None

raw_signal = "./data/raw_signal.csv"
processed_signal = "./data/processed_signal.csv"


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

    to_csv(data, raw)

# persist to csv for alternative processing 
def to_csv(data, raw = False):

    path = processed_signal

    if raw:
        path = raw_signal

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
            raw = dc.q.get(block=5)
        except queue.Empty:
            print("queue empty, terminating thread")
            store(raw, raw = True)
            store(proccessed, raw = False)
            break

        proccessed = raw
        store(raw, True)
        # todo preprocess raw signal
        store(proccessed, False)
    
