import socket
import sys
import threading
import os
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
        self.handle()

    def __del__(self):
        self.conn.close()

    def handle(self):
        while 1:
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                print("[-] {addr} disconnected: Connection losed.")
                self.__del__()
            if data:
                status = 200
                request = http.parse_request(data)
                path = os.path.join("htdocs/", request.uri)
                try:
                    f = open(path, "rb")
                except FileNotFoundError:
                    f = open("error_sites/404.html", "rb")
                    status = 404
                    ext = ".html"
                else:
                    _, ext = os.path.splitext(path)
                d = f.read()
                f.close()
                response = http.Response(d, content_type=http.mime_types[ext], status=status)
                self.conn.sendall(response.get_raw())


if __name__ == "__main__":
    s = Server()
    s.handle_connections()
