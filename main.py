import server
from plotting import plotter
import threading

def main():
    exit_flag = threading.Event()  # Event to signal thread to exit

    # Create and start the thread
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    plotter.start(exit_flag)
    #plot_thread = threading.Thread(target=plotter.start, args=(exit_flag,))
    #plot_thread.start()

if __name__ == "__main__":
    main()