import socketserver
import sys


class MyTcpHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline()
        while self.data:
            print('Received {} from {}'.format(self.data.decode().strip(), self.client_address))
            self.wfile.write(self.data.upper())
            self.data = self.rfile.readline()


class MyTcpServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, address, request_handler_class):
        self.address = address
        self.request_handler_class = request_handler_class
        super().__init__(self.address, self.request_handler_class)


if __name__ == '__main__':
    try:
        server = MyTcpServer(('', 12345), MyTcpHandler)
        server.allow_reuse_address = True
        ip, port = server.address
        print('Listening on port ', port)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
