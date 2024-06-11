import queue
import threading

class DC:

    def __init__(self, frames) -> None:
        # queue for pushing live data from sockets for processing by the processing thread (storer)
        self.data_q = queue.Queue()

        # deprecated
        # queue for pushing m5 stick commands for executing in controls
        self.msg_q = queue.Queue()

        #deprecated not used anymore
        # built in list is not thread safe. Add lock to prevent corruption
        self.accel_list_lock = threading.Lock()

        # the window size for plotter to plot values in x
        self.in_memory_frames = frames

        # deprecated
        # init raw and processed acceleration value lists with 0 padding and len = in_memory_frame
        self.accel_raw = [(0, 0, 0) for _ in range(self.in_memory_frames)]
        self.accel_processed = [(0, 0, 0) for _ in range(self.in_memory_frames)]

        self.imu_list_lock = threading.Lock()
        # init list for raw imu readings
        self.imu_raw = [(0, 0, 0, 0, 0, 0) for _ in range(self.in_memory_frames)]

        # init list for filtered imu readings
        self.imu_list_filtered_lock = threading.Lock()
        self.imu_filtered =  [(0, 0, 0, 0, 0, 0) for _ in range(self.in_memory_frames)]

        self.orientation_lock = threading.Lock()
        self.orientation = [(0, 0, 0) for _ in range(self.in_memory_frames)]


        self.linear_accel_lock = threading.Lock()
        self.linear_accel = [(0, 0, 0) for _ in range(self.in_memory_frames)]
        
        self.velocity = [(0, 0, 0) for _ in range(self.in_memory_frames)]

    def reset(self):
        #self.data_q = queue.Queue()
        self.imu_raw = [(0, 0, 0, 0, 0, 0) for _ in range(self.in_memory_frames)]
        self.imu_filtered =  [(0, 0, 0, 0, 0, 0) for _ in range(self.in_memory_frames)]
        self.orientation = [(0, 0, 0) for _ in range(self.in_memory_frames)]
        self.linear_accel = [(0, 0, 0) for _ in range(self.in_memory_frames)]
        self.velocity = [(0, 0, 0) for _ in range(self.in_memory_frames)]

class AccelGyroData:

    def __init__(self):

        self.last_angle_xyz = (0, 0, 0)
        self.last_gyro_angle_xyz =  (0, 0, 0)
    
    def update_last_values(self, current_angle:list, current_gyro_angle:list):
        self.last_angle_xyz = current_angle
        self.last_gyro_angle_xyz = current_gyro_angle

    