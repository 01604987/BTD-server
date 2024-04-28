import socket
import threading
import time
from preprocessing import preprocess
from preprocessing import storer


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



def handle_client_int(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    termination = 'end'.encode()
    st = time.time()
    a= 0
    connected = True
    while connected:
        data = conn.recv(12)  # receive up to 1024 bytes of data
        if not data:
            print("no message..")  # connection closed by client
            break
        elif termination in data:
            print("end of transmission..")
            # no need to take the last data captured before end because will always receive 12 bytes as chunk.
            #msg= msg + data.decode('utf-8')[:-3]
            break
        else:
            raw_data = preprocess.ntohs_array(data)
            # append raw data to raw_signal csv.
            storer.store(raw_data, raw=True)
            a += 1
            print("msg count: {}".format(a))

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


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client_int, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")