import ctypes
import time

# Load user32.dll for Windows API calls
user32 = ctypes.windll.user32

# Function to move the mouse to (x, y)
def move_mouse(x, y):
    user32.SetCursorPos(x, y)

def move_mouse_relative(dx, dy):
    ctypes.windll.user32.mouse_event(0x0001, ctypes.c_long(dx), ctypes.c_long(dy), 0, 0)

# Measure time to move the mouse
def measure_move_time(x, y):
    start_time = time.time()
    move_mouse_relative(x, y)
    end_time = time.time()
    return end_time - start_time

# Measure the time for a number of executions
num_iterations = 500
times = []

for _ in range(num_iterations):
    times.append(measure_move_time())

# Calculate average time
average_time = sum(times) / len(times)
print(f"Average execution time of move_mouse: {average_time:.6f} seconds")