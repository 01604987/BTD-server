import csv
import threading


raw_signal = "./raw_signal.csv"
processed_signal = "./processed_signal.csv"

in_memory_frame = 5000

accel_raw = [[0, 0, 0] for _ in range(in_memory_frame)]
accel_processed = [[0, 0, 0] for _ in range(in_memory_frame)]

lock = threading.Lock()


def store(data, raw = False):

    if raw:
        with lock:
            accel_raw.append(data)
            accel_raw.pop(0)
    else:
        with lock:
            accel_processed.append(data)
            accel_processed.pop(0)

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
    for el in accel_raw:
        to_csv(el, False)

    for el in accel_processed:
        to_csv(el, True)