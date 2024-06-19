import PyQt5
import matplotlib
import matplotlib.axes
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import threading
from processing.data_collection import DC

dc:DC = None


def velocity_plots(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes, o:matplotlib.axes.Axes, l:matplotlib.axes.Axes, v:matplotlib.axes.Axes):
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

        linear_x = [data[0] for data in dc.imu_filtered]
        linear_y = [data[1] for data in dc.imu_filtered]
        linear_z = [data[2] for data in dc.imu_filtered]

        velo_x = [data[0] for data in dc.velocity]
        velo_y = [data[1] for data in dc.velocity]

        a.cla()
        g.cla()
        o.cla()
        l.cla()
        v.cla()

        ax = a.plot(accel_x, label='x-accel')
        ay = a.plot(accel_y, label='y-accel')
        az = a.plot(accel_z, label='z-accel')

        gx = g.plot(gyro_x, label='x-gyro')
        gy = g.plot(gyro_y, label='y-gyro')
        gz = g.plot(gyro_z, label='z-gyro')
        
        ox = o.plot(ori_x, label= 'x-tilt-deg')
        oy = o.plot(ori_y, label= 'y-tilt-deg')
        #oz = o.plot(ori_z, label= 'z-deg')

        lx = l.plot(linear_x, label='x-linear-accel-filtered')
        ly = l.plot(linear_y, label='y-linear-accel-filtered')
        #lz = l.plot(linear_z, label='z-linear-accel')

        vx = v.plot(velo_x, label = 'x-velocity')
        vy = v.plot(velo_y, label = 'y-velocity')


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
        #plt.setp(lz, linewidth= lw)

        plt.setp(vx, linewidth = lw)
        plt.setp(vy, linewidth = lw)

        plt.autoscale(tight=False)
        #g.autoscale(tight=False)

        o.set_ylim(-90, 90)
        a.legend(loc='upper left')
        g.legend(loc="upper left")
        o.legend(loc="upper left")
        l.legend(loc="upper left")
        v.legend(loc='upper left')

def update_mouse_events(frame, a:matplotlib.axes.Axes, o:matplotlib.axes.Axes, l:matplotlib.axes.Axes, lf:matplotlib.axes.Axes):
    lw = 0.6
    with dc.imu_list_filtered_lock:
        accel_x = [data[0] for data in dc.imu_raw]
        accel_y = [data[1] for data in dc.imu_raw]
        accel_z = [data[2] for data in dc.imu_raw]

    with dc.orientation_lock:
        ori_x = [data[0] for data in dc.orientation]
        ori_y = [data[1] for data in dc.orientation]
        #ori_z = [data[2] for data in dc.orientation]
    with dc.linear_accel_lock:
        linear_x = [data[0] for data in dc.linear_accel]
        linear_y = [data[1] for data in dc.linear_accel]
    
    
    
    linear_x_f = [data[0] for data in dc.imu_filtered]
    linear_y_f = [data[1] for data in dc.imu_filtered]
    #accel_z_f = [data[2] for data in dc.imu_filtered]

    a.cla()
    lf.cla()
    o.cla()
    l.cla()

    ax = a.plot(accel_x, label='x-accel')
    ay = a.plot(accel_y, label='y-accel')
    az = a.plot(accel_z, label='z-accel')
    
    ox = o.plot(ori_x, label= 'x-tilt-deg')
    oy = o.plot(ori_y, label= 'y-tilt-deg')
    #oz = o.plot(ori_z, label= 'z-deg')

    lx = l.plot(linear_x, label='x-linear-accel')
    ly = l.plot(linear_y, label='y-linear-accel')

    lxf = lf.plot(linear_x_f, label='x-linear-accel-filtered')
    lyf = lf.plot(linear_y_f, label='y-linear-accel-filtered')

    plt.setp(ax, linewidth= lw)
    plt.setp(ay, linewidth= lw)
    plt.setp(az, linewidth= lw)
    plt.setp(ox, linewidth= lw)
    plt.setp(oy, linewidth= lw)
    plt.setp(lx, linewidth= lw)
    plt.setp(ly, linewidth= lw)
    plt.setp(lxf, linewidth= lw)
    plt.setp(lyf, linewidth= lw)

    plt.autoscale(tight=False)
    #g.autoscale(tight=False)

    o.set_ylim(-90, 90)
    a.legend(loc='upper left')
    lf.legend(loc="upper left")
    o.legend(loc="upper left")
    l.legend(loc="upper left")


def update_linear_accel_filtered(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes, o:matplotlib.axes.Axes, l:matplotlib.axes.Axes):
    lw = 0.6
    with dc.imu_list_filtered_lock:
        accel_x = [data[0] for data in dc.imu_filtered]
        accel_y = [data[1] for data in dc.imu_filtered]
        accel_z = [data[2] for data in dc.imu_filtered]
        velo_x = [data[0] for data in dc.velocity]
        velo_y = [data[1] for data in dc.velocity]
        #gyro_z = [data[5] for data in dc.imu_filtered]
    with dc.orientation_lock:
        ori_x = [data[0] for data in dc.orientation]
        ori_y = [data[1] for data in dc.orientation]
        #ori_z = [data[2] for data in dc.orientation]
    with dc.linear_accel_lock:
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

    gx = g.plot(velo_x, label='x-gyro')
    gy = g.plot(velo_y, label='y-gyro')
    #gz = g.plot(gyro_z, label='z-gyro')
    
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
   # plt.setp(gz, linewidth= lw)
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
        
        ox = o.plot(ori_x, label= 'pitch deg')
        oy = o.plot(ori_y, label= 'roll deg')
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

ani1 = None
def start(exit:threading.Event, data_collection:DC):
    global dc
    global ani1
    dc = data_collection
    freq = 100
    interval = (1/freq) * 1000
    frame = 1000

    accel = None
    gyro = None
    orientation = None
    linear = None
    linear_filtered = None
    velocity = None
    what = None

    fig0, ((accel, gyro), (orientation, linear), (velocity,what)) = plt.subplots(3, 2)
    #fig0, ((accel, orientation), (linear, linear_filtered)) = plt.subplots(2, 2)
    accel:matplotlib.axes.Axes
    gyro:matplotlib.axes.Axes
    orientation:matplotlib.axes.Axes
    linear:matplotlib.axes.Axes
    linear_filtered: matplotlib.axes.Axes
    velocity: matplotlib.axes.Axes

    # Set up the first subplot for accelerometer and gyro data
    if accel:
        accel.set_title('Accelerometer')
        accel.set_ylabel('Acceleration')
        accel.set_xlabel('Time')
        accel.set_ylim(-5, 5)
        accel.grid(False)

    # Set up the second subplot for only accelerometer data
    if gyro:
        gyro.set_title('Gyrometer')
        gyro.set_ylabel('Rotational acceleration')
        gyro.set_xlabel('Time')
        gyro.set_ylim(-5000, 5000)
        gyro.grid(False)

    if orientation:
        orientation.set_title('Orientation')
        orientation.set_ylabel('Degrees')
        orientation.set_xlabel('Time')
        #orientation.set_ylim(-180, 180)
        orientation.grid(False)

    if linear:
        linear.set_title('Free Accelerometer')
        linear.set_ylabel('Linear Acceleration')
        linear.set_xlabel('Time')
        linear.set_ylim(-5, 5)
        linear.grid(False)

    if linear_filtered:
        linear_filtered.set_title('Filtered linear accel')
        linear_filtered.set_ylabel('Filtered Linear Acceleration')
        linear_filtered.set_xlabel('Time')
        linear_filtered.set_ylim(-5, 5)
        linear_filtered.grid(False)


    if velocity:
        velocity.set_title('Velocity')
        velocity.set_ylabel('Velocity')
        velocity.set_xlabel('Time')
        velocity.set_ylim(-5, 5)
        velocity.grid(False)
        
    print('Starting plotter')
    # frame probably currently not relevant. Plot updates based on interval
    #ani1 = FuncAnimation(fig0, update_mouse_events, frames=frame, interval=interval, fargs=(accel,orientation,linear, linear_filtered))
    #ani1 = FuncAnimation(fig0, linear_accel_filtered, frames=frame, interval=interval, fargs=(accel,gyro,orientation,linear,))
    ani1 = FuncAnimation(fig0, velocity_plots, frames=frame, interval=interval, fargs=(accel,gyro,orientation,linear, velocity,))
    fig0.canvas.mpl_connect('key_press_event', on_key)
   

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

paused = 0

def on_key(event):
    global ani1
    global paused
    if event.key == 'p':
        if paused:
            ani1.event_source.start()
            paused = 0
        else:
            ani1.event_source.stop()
            paused = 1