from socketserver import TCPServer, StreamRequestHandler, ForkingMixIn
import os, sys


class MyRequestHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline()
        self.pid = os.getpid()
        while self.data:
            print('{} received from {}'.format(self.data.decode(), self.client_address))
            msg = '{} received from pid - {}'.format(self.data.upper(), self.pid)
            self.wfile.write(msg.encode())
            self.data = self.rfile.readline()


class MyForkingTcpServer(ForkingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    try:
        server = MyForkingTcpServer(('', 12345), MyRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(1)
