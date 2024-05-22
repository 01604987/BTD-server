import PyQt5
import matplotlib
import matplotlib.axes
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import threading
from processing.data_collection import DC

dc:DC = None

def update_linear_accel(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes, o:matplotlib.axes.Axes, l:matplotlib.axes.Axes):
    lw = 0.6
    with dc.accel_list_lock:
        accel_x = [data[0] for data in dc.imu_raw]
        accel_y = [data[1] for data in dc.imu_raw]
        accel_z = [data[2] for data in dc.imu_raw]
        gyro_x = [data[3] for data in dc.imu_raw]
        gyro_y = [data[4] for data in dc.imu_raw]
        gyro_z = [data[5] for data in dc.imu_raw]

        ori_x = [data[0] for data in dc.orientation]
        ori_y = [data[1] for data in dc.orientation]
        #ori_z = [data[2] for data in dc.orientation]

        linear_x = [data[0] for data in dc.linear_accel]
        linear_y = [data[1] for data in dc.linear_accel]
        linear_z = [data[2] for data in dc.linear_accel]

        a.cla()
        g.cla()
        o.cla()
        l.cla()

        ax = a.plot(accel_x, label='x-accel')
        ay = a.plot(accel_y, label='y-accel')
        az = a.plot(accel_z, label='z-accel')

        gx = g.plot(gyro_x, label='x-gyro')
        gy = g.plot(gyro_y, label='y-gyro')
        gz = g.plot(gyro_z, label='z-gyro')
        
        ox = o.plot(ori_x, label= 'x-tilt-deg')
        oy = o.plot(ori_y, label= 'y-tilt-deg')
        #oz = o.plot(ori_z, label= 'z-deg')

        lx = l.plot(linear_x, label='x-linear-accel')
        ly = l.plot(linear_y, label='y-linear-accel')
        lz = l.plot(linear_z, label='z-linear-accel')

        plt.setp(ax, linewidth= lw)
        plt.setp(ay, linewidth= lw)
        plt.setp(az, linewidth= lw)
        plt.setp(gx, linewidth= lw)
        plt.setp(gy, linewidth= lw)
        plt.setp(gz, linewidth= lw)
        plt.setp(ox, linewidth= lw)
        plt.setp(oy, linewidth= lw)
        #plt.setp(oz, linewidth= lw)
        plt.setp(lx, linewidth= lw)
        plt.setp(ly, linewidth= lw)
        plt.setp(lz, linewidth= lw)

        plt.autoscale(tight=False)
        #g.autoscale(tight=False)

        o.set_ylim(-90, 90)
        a.legend(loc='upper left')
        g.legend(loc="upper left")
        o.legend(loc="upper left")
        l.legend(loc="upper left")

def update_orientation(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes, o:matplotlib.axes.Axes):
    lw = 0.6
    with dc.accel_list_lock:
        accel_x = [data[0] for data in dc.imu_raw]
        accel_y = [data[1] for data in dc.imu_raw]
        accel_z = [data[2] for data in dc.imu_raw]
        gyro_x = [data[3] for data in dc.imu_raw]
        gyro_y = [data[4] for data in dc.imu_raw]
        gyro_z = [data[5] for data in dc.imu_raw]

        ori_x = [data[0] for data in dc.orientation]
        ori_y = [data[1] for data in dc.orientation]
        #ori_z = [data[2] for data in dc.orientation]

        a.cla()
        g.cla()
        o.cla()

        ax = a.plot(accel_x, label='x-accel')
        ay = a.plot(accel_y, label='y-accel')
        az = a.plot(accel_z, label='z-accel')

        gx = g.plot(gyro_x, label='x-gyro')
        gy = g.plot(gyro_y, label='y-gyro')
        gz = g.plot(gyro_z, label='z-gyro')
        
        ox = o.plot(ori_x, label= 'x-tilt-deg')
        oy = o.plot(ori_y, label= 'y-tilt-deg')
        #oz = o.plot(ori_z, label= 'z-deg')

        plt.setp(ax, linewidth= lw)
        plt.setp(ay, linewidth= lw)
        plt.setp(az, linewidth= lw)
        plt.setp(gx, linewidth= lw)
        plt.setp(gy, linewidth= lw)
        plt.setp(gz, linewidth= lw)
        plt.setp(ox, linewidth= lw)
        plt.setp(oy, linewidth= lw)
        #plt.setp(oz, linewidth= lw)

        plt.autoscale(tight=False)
        #g.autoscale(tight=False)

        o.set_ylim(-100, 100)
        a.legend(loc='upper left')
        g.legend(loc="upper left")
        o.legend(loc="upper left")


def update_new(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes):
    lw = 0.6
    with dc.accel_list_lock:
        accel_x = [data[0] for data in dc.imu_raw]
        accel_y = [data[1] for data in dc.imu_raw]
        accel_z = [data[2] for data in dc.imu_raw]
        gyro_x = [data[3] for data in dc.imu_raw]
        gyro_y = [data[4] for data in dc.imu_raw]
        gyro_z = [data[5] for data in dc.imu_raw]

        a.cla()
        g.cla()

        ax = a.plot(accel_x, label='x-accel')
        ay = a.plot(accel_y, label='y-accel')
        az = a.plot(accel_z, label='z-accel')

        gx = g.plot(gyro_x, label='x-gyro')
        gy = g.plot(gyro_y, label='y-gyro')
        gz = g.plot(gyro_z, label='z-gyro')
        

        plt.setp(ax, linewidth= lw)
        plt.setp(ay, linewidth= lw)
        plt.setp(az, linewidth= lw)
        plt.setp(gx, linewidth= lw)
        plt.setp(gy, linewidth= lw)
        plt.setp(gz, linewidth= lw)

        plt.autoscale(tight=False)
        #g.autoscale(tight=False)

        
        a.legend(loc='upper left')
        g.legend(loc="upper left")


def update(frame):
    with dc.accel_list_lock:
        
        data_x = [data[0] for data in dc.accel_raw]
        data_y = [data[1] for data in dc.accel_raw]
        data_z = [data[2] for data in dc.accel_raw]

    # clean plots
    plt.cla()

    

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

    fig0, ((accel, gyro), (orientation, linear)) = plt.subplots(2, 2)
    accel:matplotlib.axes.Axes
    gyro:matplotlib.axes.Axes
    orientation:matplotlib.axes.Axes
    linear:matplotlib.axes.Axes

    # Set up the first subplot for accelerometer and gyro data
    accel.set_title('Accelerometer')
    accel.set_ylabel('Acceleration')
    accel.set_xlabel('Time')
    accel.set_ylim(-5, 5)
    accel.grid(False)

    # Set up the second subplot for only accelerometer data
    gyro.set_title('Gyrometer')
    gyro.set_ylabel('Rotational acceleration')
    gyro.set_xlabel('Time')
    gyro.set_ylim(-5000, 5000)
    gyro.grid(False)

    orientation.set_title('Orientation')
    orientation.set_ylabel('Degrees')
    orientation.set_xlabel('Time')
    #orientation.set_ylim(-180, 180)
    orientation.grid(False)

    linear.set_title('Free Accelerometer')
    linear.set_ylabel('Linear Acceleration')
    linear.set_xlabel('Time')
    linear.set_ylim(-5, 5)
    linear.grid(False)

    print('Starting plotter')
    # frame probably currently not relevant. Plot updates based on interval
    #ani1 = FuncAnimation(fig0, update_orientation, frames=frame, interval=interval, fargs=(accel,gyro,orientation,))
    ani1 = FuncAnimation(fig0, update_linear_accel, frames=frame, interval=interval, fargs=(accel,gyro,orientation,linear,))

    try:
        # blocking function
        plt.show()
    except KeyboardInterrupt:
        # terminate plotter thread
        print("Closing Plotter")
        exit.set()
        close()

def close():
    plt.close()