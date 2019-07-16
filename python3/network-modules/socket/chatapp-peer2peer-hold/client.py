import socket
import sys
import select


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 50000)
print('Connecting to {} on {}'.format(*server_address))
sock.connect(server_address)


def exiting(host=''):
    print('{} has exitted !!'.format(host))
    sys.exit()

inputs = [sock, sys.stdin]

while inputs:
    readable, _, _ = select.select(inputs, [], [])

    for s in readable:
        if s is sock:
            data = sock.recv(1024).decode()
            if data:
                if data.lower() != 'exit':
                    print('{}'.format(data))
                    sys.stdout.write('You: ')
                    sys.stdout.flush()
                else:
                    exiting('Server')
            else:
                exiting('Server')
        else:
            msg = sys.stdin.readline()
            sock.send(msg.encode())
            sys.stdout.write('You: ')
            sys.stdout.flush()
