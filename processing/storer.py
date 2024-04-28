import csv
import threading
import queue
from processing.data_collection import DC

dc:DC = None

raw_signal = "./data/raw_signal.csv"
processed_signal = "./data/processed_signal.csv"



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


def to_csv(data, raw = False):

    path = processed_signal

    if raw:
        path = raw_signal

    with open(path, mode ='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

#deprecated
def flush():
    for el in dc.accel_raw:
        to_csv(el, False)

    for el in dc.accel_processed:
        to_csv(el, True)

def start(exit:threading.Event, data_collection:DC):
    global dc
    dc = data_collection
    while not exit.is_set():
        try:
            raw = dc.q.get(block=5)
        except queue.Empty:
            store(raw, True)
            store(raw, False)
            break
        
        store(raw, True)
        store(raw, False)
    
