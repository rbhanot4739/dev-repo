import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 50000)
print('Connecting to {} on {}'.format(*server_address))
sock.connect(server_address)


def exiting(host=''):
    print('{} has exitted !!'.format(host))
    sys.exit()


while True:
    serv_msg = sock.recv(1024).decode()
    if serv_msg.lower() != 'exit':
        print('{}'.format(serv_msg))
        client_reply = input('You: ')
        sock.send(bytes(client_reply, 'utf-8'))

        if client_reply.lower() == 'exit':
            exiting('Client')
    else:
        exiting('Server')
