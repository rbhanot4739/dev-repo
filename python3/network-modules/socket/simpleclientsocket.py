import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
print('Connecting to {} on {}'.format(*server_address))
sock.connect(server_address)

msg = 'data\n' * 90 * 1024 * 1024
sock.sendall(bytes(msg, 'utf-8'))
