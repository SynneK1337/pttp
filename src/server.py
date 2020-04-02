import socket
import sys
import threading
import os.path
import http


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
            threading._start_new_thread(Handler, (conn, addr))


class Handler():
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.is_alive = True
        self.handle()

    def __del__(self):
        self.conn.close()
        self.is_alive = False

    def handle(self):
        while self.is_alive:
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                print(f"[-] {self.addr} disconnected: Connection losed.")
                self.__del__()
            else:
                if data:
                    status = 200
                    try:
                        request = http.parse_request(data)
                    except http.MethodNotAllowed:
                        status = 405
                        path = "error_sites/405.html"
                    except Exception:
                        status = 400
                        path = "error_sites/400.html"
                    else:
                        if request.uri == '/':
                            request.uri = "/index.html"
                        path = os.path.join("htdocs/", request.uri[1:])
                    try:
                        f = open(path, "rb")
                    except FileNotFoundError:
                        status = 404
                        path = "error_sites/404.html"
                        f = open("error_sites/404.html", "rb")
                    _, ext = os.path.splitext(path)
                    print(f"[i] {self.addr} requested {request.uri}")
                    d = f.read()
                    f.close()
                    response = http.Response(d, content_type=http.mime_types[ext], status=status)
                    try:
                        self.conn.sendall(response.get_raw())
                    except OSError:
                        self.__del__()
                        print(f"[i] {self.addr} ended the connection.")


if __name__ == "__main__":
    s = Server()
    s.handle_connections()
