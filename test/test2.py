import ctypes_mouse

# Measure the time for a number of executions
num_iterations = 100
times = []

for _ in range(num_iterations):
    times.append(ctypes_mouse.measure_move_time())

# Calculate average time
average_time = sum(times) / len(times)
print(f"Average execution time of move_mouse: {average_time:.6f} seconds")