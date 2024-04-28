import PyQt5
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import threading
from processing.data_collection import DC

dc:DC = None

def update(frame):
    with dc.accel_list_lock:
        
        data_x = [data[0] for data in dc.accel_raw]
        data_y = [data[1] for data in dc.accel_raw]
        data_z = [data[2] for data in dc.accel_raw]

    # clean plots
    plt.cla()

    plt.ylim(-3, 3)

    # plot all 3 axis values
    plt.plot(data_x, label='x-axis')
    plt.plot(data_y, label='y-axis')
    plt.plot(data_z, label='z-axis')

    plt.legend(loc='upper left')
    plt.tight_layout()


def start(exit:threading.Event, data_collection:DC):
    global dc
    dc = data_collection
    freq = 100
    interval = (1/freq) * 1000
    frame = 1000

    fig, ax = plt.subplots()

    print('Starting plotter')
    # frame probably currently not relevant. Plot updates based on interval
    ani = FuncAnimation(fig, update, frames = frame, interval=interval)
    try:
        # blocking function
        plt.show()
    except KeyboardInterrupt:
        # terminate plotter thread
        print("Bye")
        exit.set()
        close()

def close():
    plt.close()