import server
from plotting import plotter
import threading
from processing.data_collection import DC

def main():

    dc = DC(frames=3000)
    exit_flag = threading.Event()  # Event to signal thread to exit

    # Create and start the thread
    server_thread = threading.Thread(target=server.start, args=(exit_flag, dc))
    server_thread.start()
    
    # main loop starts here
    plotter.start(exit_flag, dc)


if __name__ == "__main__":
    main()
