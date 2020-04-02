import socket
import sys
import threading
import os


class PathTraversalAttack(Exception):
    """Client attempted to exploit path traversal vulnerability"""


class Server():
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind((self.host, self.port))
        except Exception as err:
            sys.exit(err)
        print(f"[+] Server listening on {self.host}:{self.port}")
        self.sock.listen(0)

    def __del__(self):
        self.sock.close()

    def handle_connections(self):
        while 1:
            conn, addr = self.sock.accept()
            print(f"[+] New connection from {addr}")
            threading._start_new_thread(HTTPHandle, (conn, addr))


class Response():
    def __init__(self, data, version="HTTP/1.1", status=200, status_msg="OK"):
        self.version = version
        self.status = status
        self.status_msg = status_msg
        self.data = data.decode('utf-8')

    def get_raw(self):
        return f"{self.version} {self.status} {self.status_msg}\r\nContent-Type: text/html;charset=utf-8\r\nContent-Length: {len(self.data)}\r\n\r\n{self.data}\r\n\r\n".encode('utf-8')


class Request():
    def __init__(self, data):
        self.data = data
        # Parsing the request
        self.data = self.data.decode('utf-8')
        self.data = self.data.splitlines()

        # Parsing the Request-Line
        # Request-Line body: Method Request-URI HTTP-Version \r\n
        self.method, self.uri, self.version = self.data[0].split(' ')

        # Convert URI to path
        if self.uri == '/':
            self.uri = "index.html"

        elif ".." in self.uri:
            raise PathTraversalAttack
        # print("!!!!!!!", self.uri)
        self.requested_path = os.path.join("htdocs/", self.uri)


class HTTPHandle():
    def __init__(self, conn, addr):
        self.is_alive = True
        self.conn = conn
        self.addr = addr
        self.handle()

    def __del__(self):
        self.is_alive = False
        self.conn.close()

    def handle(self):
        while self.is_alive:
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                self.__del__()
            print(data.decode('utf-8'))
            request = Request(data)     # Request() parses the data itself
            with open(request.requested_path, 'rb') as f:
                d = f.read()
                response = Response(data=d)
            # print(response.get_raw())
            self.conn.sendall(response.get_raw())



if __name__ == "__main__":
    s = Server()
    s.handle_connections()