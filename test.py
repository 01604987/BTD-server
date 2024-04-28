
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import threading
from processing.storer import accel_raw, lock

def update(frame):
    with lock:
        
        data_x = [data[0] for data in accel_raw]
        data_y = [data[1] for data in accel_raw]
    
    plt.cla()

    plt.plot(data_x, label='x-axis')
    plt.plot(data_y, label='y-axis')

    plt.legend(loc='upper left')
    plt.tight_layout()



def test (exit_flag: threading.Event):
    counter = 0
    while not exit_flag.is_set():
        time.sleep(1)
        counter += 1
        print("sleeping {}".format(counter))
    print("Exiting plotter")

def start(exit: threading.Event):
    
    freq = 100
    interval = (1/freq) * 1000
    frame = 1000

    fig, ax = plt.subplots()

    print('Starting plotter')
    ani = FuncAnimation(fig, update, frames = frame, interval=interval)
    plt.show()

def close():
    plt.close()