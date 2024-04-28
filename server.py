import socket
import threading
import time
from processing import network_package as np, storer
from processing.data_collection import DC


SIZE = 64 # how many symbols (bytes) to read
PORT = 50 # port number to listen on
# need to adjust this function to get correct host address for hosts that have multiple adapters
SERVER = socket.gethostbyname_ex(socket.gethostname())[2][2] # this gets the current IP addr.
#SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


# TODO extend for accepting different kind of data / protocol
def handle_client_int(conn, addr, exit:threading.Event, dc:DC):
    print(f"[NEW CONNECTION] {addr} connected.")

    termination = 'end'.encode()
    st = time.time()
    a= 0
    connected = True
    while connected and not exit.is_set():
        # accel data = 3 float values. 4 byte each = 12 byte max for single message.
        data = conn.recv(12)  
        if not data:
            print("no message..")  # connection closed by client
            break
        elif termination in data:
            print("end of transmission..")
            # no need to take the last data captured before end because will always receive 12 bytes as chunk.
            #msg= msg + data.decode('utf-8')[:-3]
            break
        else:
            raw_data = np.ntohs_array(data)
            # push to queue for processing by another thread.
            dc.q.put(raw_data)
            a += 1
            #print("msg count: {}".format(a))

        # debug 
        # print('chunk:', htons)

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


def start(exit:threading.Event, dc:DC):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client_int, args=(conn, addr, exit, dc))
    thread.start()

    while dc.q.empty():
        if exit.is_set():
            return 0
        time.sleep(0.5)
    
    print("Starting Storer")
    storer_t = threading.Thread(target=storer.start, args=(exit, dc))
    storer_t.start()


    print(f"[ACTIVE THREADS] {threading.activeCount()}")