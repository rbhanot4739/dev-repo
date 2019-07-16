import socketserver
import sys


class MyTCPRequesthandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        while self.data:
            print('Received {} from {}'.format(self.data.decode().strip(), self.client_address))
            self.request.send(self.data.upper())
            self.data = self.request.recv(1024)


class MyTcpServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, address, request_handler_class):
        self.address = address
        self.request_handler_class = request_handler_class
        super().__init__(self.address, self.request_handler_class)


if __name__ == '__main__':
    try:
        server = MyTcpServer(('', 12345), MyTCPRequesthandler)
        ip, port = server.server_address
        print(server.allow_reuse_address)
        print('Server listening on port {}'.format(port))
        # server.handle_request()
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
