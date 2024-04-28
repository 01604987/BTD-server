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

    plt.cla()

    plt.ylim(-3, 3)

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
    ani = FuncAnimation(fig, update, frames = frame, interval=5)
    try:
        plt.show()
    except KeyboardInterrupt:
        print("Bye")
        exit.set()
        close()

    
    # try:
    #     while not exit.is_set():
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Keyboard interrupt received. Exiting...")
    # finally:
    #     exit.set()  # Set the exit event flag to terminate other threads
    #     close()     # Close the plot
    
    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         print("Bye")
    #         exit.set()
    #         close()
    #         break

def close():
    plt.close()