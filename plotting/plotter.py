import PyQt5
import matplotlib
import matplotlib.axes
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from processing.data_collection import DC

dc:DC = None



def velocity_plots(frame, a:matplotlib.axes.Axes, g:matplotlib.axes.Axes, o:matplotlib.axes.Axes, l:matplotlib.axes.Axes, v:matplotlib.axes.Axes, events):
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
        #linear_z = [data[2] for data in dc.imu_filtered]

        velo_x = [data[0] for data in dc.velocity]
        velo_y = [data[1] for data in dc.velocity]


    if events[0].is_set():
        a.cla()
        ax = a.plot(accel_x, label='x-accel')
        ay = a.plot(accel_y, label='y-accel')
        az = a.plot(accel_z, label='z-accel')
        plt.setp(ax, linewidth= lw)
        plt.setp(ay, linewidth= lw)
        plt.setp(az, linewidth= lw)
        a.legend(loc='upper left')

    if events[1].is_set():
        g.cla()
        gx = g.plot(gyro_x, label='x-gyro')
        gy = g.plot(gyro_y, label='y-gyro')
        gz = g.plot(gyro_z, label='z-gyro')
        plt.setp(gx, linewidth= lw)
        plt.setp(gy, linewidth= lw)
        plt.setp(gz, linewidth= lw)
        g.legend(loc="upper left")


    if events[2].is_set():        
        o.cla()
        ox = o.plot(ori_x, label= 'x-tilt-deg')
        oy = o.plot(ori_y, label= 'y-tilt-deg')
        #oz = o.plot(ori_z, label= 'z-deg')
        plt.setp(ox, linewidth= lw)
        plt.setp(oy, linewidth= lw)
        #plt.setp(oz, linewidth= lw)
        o.set_ylim(-90, 90)
        o.legend(loc="upper left")

    if events[3].is_set():   
        l.cla()
        lx = l.plot(linear_x, label='x-linear-accel-filtered')
        ly = l.plot(linear_y, label='y-linear-accel-filtered')
        #lz = l.plot(linear_z, label='z-linear-accel')
        plt.setp(lx, linewidth= lw)
        plt.setp(ly, linewidth= lw)
        #plt.setp(lz, linewidth= lw)
        l.legend(loc="upper left")

    if events[4].is_set():   
        v.cla()
        vx = v.plot(velo_x, label = 'x-velocity')
        vy = v.plot(velo_y, label = 'y-velocity')
        plt.setp(vx, linewidth = lw)
        plt.setp(vy, linewidth = lw)
        v.legend(loc='upper left')


    
    plt.autoscale(tight=False)

ani1 = None
a_paused = threading.Event()
a_paused.set()
g_paused = threading.Event()
g_paused.set()
o_paused = threading.Event()
o_paused.set()
l_paused = threading.Event()
l_paused.set()
v_paused = threading.Event()
v_paused.set()


events = [a_paused, g_paused, o_paused, l_paused, v_paused]

def start(exit:threading.Event, data_collection:DC):
    global dc
    global ani1
    global events
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

    fig0, ((accel, gyro), (orientation, linear), (velocity,_)) = plt.subplots(3, 2)
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
    ani1 = FuncAnimation(fig0, velocity_plots, frames=frame, interval=interval, fargs=(accel,gyro,orientation,linear, velocity, events, ))
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
    global events
    if event.key == 'p':
        if paused:
            ani1.event_source.start()
            paused = 0
        else:
            ani1.event_source.stop()
            paused = 1

    if event.key == 'a':
        if events[0].is_set():
            events[0].clear()
        else:
            events[0].set()
    if event.key == 'g':
        if events[1].is_set():
            events[1].clear()
        else:
            events[1].set()
    if event.key == 'o':
        if events[2].is_set():
            events[2].clear()
        else:
            events[2].set()
    if event.key == 'l':
        if events[3].is_set():
            events[3].clear()
        else:
            events[3].set()
    if event.key == 'v':
        if events[4].is_set():
            events[4].clear()
        else:
            events[4].set()