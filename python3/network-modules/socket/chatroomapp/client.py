import socket

import sys

import select

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('localhost', 44444))
except socket.error as msg:
    print('Failed to connect to server !!')
    sys.exit(1)

inputs = [client, sys.stdin]

while inputs:
    readable, writable, error = select.select(inputs, [], [])

    for sock in readable:
        if sock is client:
            data = sock.recv(1024).decode()
            sys.stdout.write('\n' + data)
            sys.stdout.flush()
        else:
            msg = sys.stdin.readline()
            client.send(bytes(msg, 'utf-8'))
            sys.stdout.write('[Me]: ')
            sys.stdout.flush()
