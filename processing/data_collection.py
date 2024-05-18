import queue
import threading

class DC:

    def __init__(self, frames) -> None:
        # queue for pushing live data from sockets for processing by the processing thread (storer)
        self.data_q = queue.Queue()

        # queue for pushing m5 stick commands for executing in controls
        self.msg_q = queue.Queue()

        # built in list is not thread safe. Add lock to prevent corruption
        self.accel_list_lock = threading.Lock()

        # the window size for plotter to plot values in x
        self.in_memory_frames = frames
        # init raw and processed acceleration value lists with 0 padding and len = in_memory_frame
        self.accel_raw = [[0, 0, 0] for _ in range(self.in_memory_frames)]
        self.accel_processed = [[0, 0, 0] for _ in range(self.in_memory_frames)]
