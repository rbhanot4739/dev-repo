import socket
import select
import queue
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind(('localhost', 44444))
    server.setblocking(0)
except socket.error as msg:
    print(msg)
else:
    server.listen(5)
    print('Listening on port 44444')

''
# Create the list of input/output/errored sockts
inputs = [server]
outputs = []
errorred = []
messages = {}

while inputs:
    readable, writable, exceptioned = select.select(inputs, outputs, errorred)

    for s in readable:
        if s is server:
            conn, _ = s.accept()
            print('Received connection from {!r}'.format(conn.getpeername()))
            inputs.append(conn)
            conn.setblocking(0)
            messages[conn] = queue.Queue()
            conn.send(b'Welcome to the server\n')
        else:  # If this is an existing connection
            data = s.recv(1024)
            if data:
                print('{} received from {!r}'.format(data, s.getpeername()))
                messages[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:  # client has exit the connection
                print('No data received. Closing {!r}'.format(s.getpeername()))
                inputs.remove(s)
                s.close()
                del messages[s]

    for s in writable:
        if not messages[s].empty():
            msg = messages[s].get().upper()
            s.send(msg)
        else:
            outputs.remove(s)
