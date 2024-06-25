import socket
import threading
import time
from processing import network_package as np, storer
from processing.data_collection import DC
from controls.actions import *
from controls.control_driver import *
import s_cmd


SIZE = 64 # how many symbols (bytes) to read
PORT = 5500 # port number to listen on
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(3)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(3)
udp_socket.bind((SERVER, PORT+1))

def listen_udp_sock(exit:threading.Event, dc:DC, events:dict[str, threading.Event]):
    print(f"Listen to udp sock under {SERVER}:{PORT}")
    connected = True
    while connected and not exit.is_set():
        # blocks until event has been set
        events.get("stream").wait()
        try:
            # TODO recv 24 bytes to include xyz gyro data
            data, addr = udp_socket.recvfrom(24)
            if not data:
                print("no message.. upd")  # connection closed by client
                #break
        except socket.timeout:
            print("Udp timeout")
        except ConnectionResetError:
            print("Connection reset by peer.")
        except ConnectionAbortedError:
            print("Connection aborted.")
        except OSError as e:
            print(f"Socket error occurred: {e}")
            break
        


        raw_data = np.ntohs_array_imu_float(data)
        # push to queue for processing by another thread.
        dc.data_q.put(raw_data)


def calc_freq(st:time.time, imu_raw):
    # get the end time          
    et = time.time() 
    print('Done')
    # get the execution time
    elapsed = et - st
    count = 0
    for zero in imu_raw:
        if zero == [0,0,0,0,0,0]:
            count += 1
        else:
            break
    perMessage = elapsed/ (len(imu_raw) - count)
    print ((len(imu_raw) - count), 'messages in approx.',elapsed,'s')
    freq = 1/perMessage
    print(freq)



def handle_client_new(conn, addr, exit:threading.Event, dc:DC, events: dict[str, threading.Event]):
    print(f"[NEW CONNECTION] {addr} connected.")
    

    st = time.time()

    while not exit.is_set():
        try:
            # all commands are string based. Currently max of 20 bytes string
            data = conn.recv(20) 
        except ConnectionAbortedError:
            print("Connection aborted")
            return
        except socket.timeout:
            print("Socket timed out. No data received within the timeout period.")
            return 
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

        if not data:
            print("no message.. tcp")  # connection closed by client maybe ?
            break

        elif s_cmd.termination in data:
            print("end of transmission..")
            break

        elif s_cmd.left_swipe in data:
            print("Left Swipe Command recieved!")
            previous_slide()

        elif s_cmd.right_swipe in data:
            print("Right Swipe Command recieved!")
            next_slide()

        elif s_cmd.mouse_begin in data:
            print("mouse begin")
            if not events.get("stream").is_set():
                dc.reset()
                events.get("stream").set()
                events.get("mouse").set()

        elif s_cmd.mouse_end in data:
            print("mouse end")
            if events.get("stream").is_set():
                events.get("stream").clear()
                events.get("mouse").clear()
                release_lmb()
                dc.flush_queue()


        elif s_cmd.mouse_hold in data:
            print("holding lmb")
            hold_lmb()

        elif s_cmd.index_tapped in data:
            print("tap index")
            hold_lmb()
            release_lmb()
            
        elif s_cmd.middle_tapped in data:
            print("tap middle")
            hold_rmb()
            release_rmb()


        elif s_cmd.middle_double_tapped in data:
            print("tap 2x middle")
            # pdf slides specific functions for entering & exiting full screen
            hold_ctrl()
            press_L()
            release_ctrl()

        elif s_cmd.vol_begin in data:
            print("hold middle")
            if not events.get("stream").is_set():
                dc.reset()
                events.get("stream").set()
                events.get("volume").set()

        elif s_cmd.vol_end in data:
            if events.get("stream").is_set():
                events.get("stream").clear()
                events.get("volume").clear()
                dc.flush_queue()

        elif s_cmd.zoom_begin in data:
            if not events.get("stream").is_set():
                dc.reset()
                events.get("stream").set()
                events.get("zoom").set()

        elif s_cmd.zoom_end in data:
            if events.get("stream").is_set():
                release_ctrl()
                events.get("stream").clear()
                events.get("zoom").clear()
                dc.flush_queue()

    
    conn.send("Bye!".encode('utf-8'))
    conn.close()
    udp_socket.close()

    calc_freq(st, dc.imu_raw)
    return


def closer(exit:threading.Event, conn:socket):
    while (not exit.is_set()):
        time.sleep(1)
    
    print("closing conn, sending Bye!")
    conn.send("Bye!".encode('utf-8'))
    conn.close()
    udp_socket.close()

def start(exit:threading.Event, dc:DC):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")


    conn = None

    # use exit.is_set()
    while not conn:
        try:
            conn, addr = server.accept()
        except socket.timeout:
            if exit.is_set():
                print("Shutting down Server")
                return 0
            else:
                print("Accept connections Timeout. Retry in {} seconds".format(server.gettimeout()))
    
    # Event to signal mouse event proccessing

    stream_events = threading.Event()
    mouse_events = threading.Event()
    vol_events = threading.Event()
    zoom_events = threading.Event()
    events = {
        "stream": stream_events,
        "mouse" : mouse_events,
        "volume": vol_events,
        "zoom" : zoom_events
    }
    

    tcp = threading.Thread(target=handle_client_new, args=(conn, addr, exit, dc, events))
    tcp.start()

    udp = threading.Thread(target=listen_udp_sock, args=(exit, dc, events))
    udp.start()

    while dc.data_q.empty():
        if exit.is_set():
            return 0
        time.sleep(0.5)
    
    print("Starting Storer")

    storer_t = threading.Thread(target=storer.start, args=(exit, dc, events))
    storer_t.start()
    
    terminator = threading.Thread(target=closer, args=(exit, conn))
    terminator.start()

    print(f"[ACTIVE THREADS] {threading.activeCount()}")



