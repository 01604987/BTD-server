import queue
import threading

class DC:

    def __init__(self, frames) -> None:
        self.q = queue.Queue()
        self.accel_list_lock = threading.Lock()
        self.in_memory_frame = frames

        self.accel_raw = [[0, 0, 0] for _ in range(self.in_memory_frame)]
        self.accel_processed = [[0, 0, 0] for _ in range(self.in_memory_frame)]