import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 12345))
sock.listen(2)
print('Listening on port 12345')

try:
    while True:
        conn, _ = sock.accept()
        print(conn.getpeername())
        data = conn.recv(1024)
        count = 0
        if data:
            while data:
                count += 1
                data = conn.recv(1024)
            else:
                print(count)

except KeyboardInterrupt:
    sock.close()
    sys.exit()
