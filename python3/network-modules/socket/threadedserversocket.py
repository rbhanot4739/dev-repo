import socket
import sys
import threading
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 12345))
sock.listen(2)
print('Listening on port 12345')


def threader(client):
    data = client.recv(1024)
    count = 0
    while data:
        count += 1
        data = client.recv(1024)
    else:
        print(count)
        client.send(b'no data')


try:
    while True:
        conn, _ = sock.accept()
        print(conn.getpeername())
        threading.Thread(target=threader, args=(conn,), daemon=True).start()
except KeyboardInterrupt:
    sock.close()
    sys.exit()
