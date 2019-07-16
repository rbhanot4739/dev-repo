import sys
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
import threading


class MyRequestHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline()
        self.curthread = threading.current_thread().getName()
        while self.data:
            print('Received data from {}'.format(self.client_address))
            self.wfile.write(('Received {} from {}'.format(self.data.upper(), self.curthread)).encode())
            self.data = self.rfile.readline()
        else:
            print('{} disconnected'.format(self.client_address))


class MyThreadedTcpServer(ThreadingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    try:
        server = MyThreadedTcpServer(('', 12345), MyRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
