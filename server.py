import socket
import threading
import time
from processing import network_package as np, storer
from processing.data_collection import DC


SIZE = 64 # how many symbols (bytes) to read
PORT = 5000 # port number to listen on
# need to adjust this function to get correct host address for hosts that have multiple adapters
#SERVER = socket.gethostbyname_ex(socket.gethostname())[2][2] # this gets the current IP addr.
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(3)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(3)
udp_socket.bind((SERVER, PORT))

def listen_udp_sock(exit:threading.Event, dc:DC):
    print(f"Listen to udp sock under {SERVER}:{PORT}")
    connected = True
    while connected and not exit.is_set():
        try:
            # TODO recv 24 bytes to include xyz gyro data
            data, addr = udp_socket.recvfrom(24)
            if not data:
                print("no message..")  # connection closed by client
                break
            else:
                #raw_data = np.ntohs_array(data)
                raw_data = np.ntohs_array_imu_float(data)
                # push to queue for processing by another thread.
                dc.data_q.put(raw_data)
        except socket.timeout:
            print("Udp timeout")
        except ConnectionResetError:
            print("Connection reset by peer.")
        except ConnectionAbortedError:
            print("Connection aborted.")
        except OSError as e:
            print(f"Socket error occurred: {e}")




# TODO rewrite TCP to accept string or numeric commands
def handle_client_int(conn, addr, exit:threading.Event, dc:DC):
    print(f"[NEW CONNECTION] {addr} connected.")

    termination = 'end'.encode()
    st = time.time()
    a= 0
    connected = True
    while connected and not exit.is_set():
        try:
            # accel data = 3 float values. 4 byte each = 12 byte max for single message.
            data = conn.recv(12)  
            if not data:
                print("no message..")  # connection closed by client
                break
            elif termination in data:
                print("end of transmission..")
                connected = False
                # no need to take the last data captured before end because will always receive 12 bytes as chunk.
                #msg= msg + data.decode('utf-8')[:-3]
                break
            else:
                raw_data = np.ntohs_array(data)
                # push to queue for processing by another thread.
                dc.msg_q.put(raw_data)
                a += 1
        except ConnectionAbortedError:
            print("Connection aborted")
            return


    # get the end time          
    et = time.time() 
    print('Done')
    # get the execution time
    elapsed = et - st
    perMessage = elapsed/a
    print (a, 'messages in approx.',elapsed,'s')
    freq = 1/perMessage
    print(freq)

    conn.send("Bye!".encode('utf-8'))
    conn.close()
    udp_socket.close()


def closer(exit:threading.Event, conn:socket):
    while (not exit.is_set()):
        time.sleep(1)
    
    conn.close()
    udp_socket.close()

def start(exit:threading.Event, dc:DC):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")


    conn = None

    # server.accept is blocking, preventing graceful shutdown
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
    

    tcp = threading.Thread(target=handle_client_int, args=(conn, addr, exit, dc))
    tcp.start()

    udp = threading.Thread(target=listen_udp_sock, args=(exit, dc))
    udp.start()

    # TODO need to remove this in order to start storer with empty queue
    while dc.data_q.empty():
        if exit.is_set():
            return 0
        time.sleep(0.5)
    
    print("Starting Storer")
    storer_t = threading.Thread(target=storer.start, args=(exit, dc))
    storer_t.start()

    terminator = threading.Thread(target=closer, args=(exit, conn))
    terminator.start()

    print(f"[ACTIVE THREADS] {threading.activeCount()}")



