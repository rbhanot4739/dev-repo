import socket
import select

import sys

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    serv.bind(('localhost', 44444))
    serv.listen(5)
except socket.error as msg:
    print(msg)
else:
    print('Server started on localhost:44444')

inputs = [serv]


def send_to_peers(serv, client, data=None):
    for s in inputs:
        if s is not serv and s is not client:
            if data:
                reply = '[{}:{}]:~ {}'.format(*client.getpeername(), data.upper())
            else:
                reply = '[{}] disconnected\n'.format(s.getpeername())
            s.send(bytes(reply, 'utf-8'))


try:
    while inputs:
        read, write, error = select.select(inputs, [], [])

        for sock in read:
            if sock is serv:
                connection, _ = sock.accept()
                print('[{}] connected'.format(connection.getpeername()))
                inputs.append(connection)
                connection.send(b' --- Hello from server ---\n')
            else:
                try:
                    data = sock.recv(1024).decode()
                    if data:
                        # print("received {} from {} ".format(data, sock.getpeername()))  # Can be put into a Queue
                        send_to_peers(serv, sock, data)
                    else:
                        print('[{}] disconnected'.format(sock.getpeername()))
                        send_to_peers(serv, sock)
                        sock.close()
                        inputs.remove(sock)

                except socket.error as msg:
                    print('[{}] disconnected\n {}'.format(sock.getpeername(), msg))
                    sock.close()
                    inputs.remove(sock)

except KeyboardInterrupt:
    serv.close()
    sys.exit('ctrl-c issue !!')
