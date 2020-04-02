status_codes = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed"
}

methods = [
    "OPTIONS",
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "TRACE"
    "CONNECT"
]

mime_types = {
    ".html":    "text/html;charset=utf-8",
    ".json":    "application/json",
    ".jpg":     "image/jpeg",
    ".jpeg":    "image/jpeg",
    ".png":     "image/png"
}


class MethodNotAllowed(Exception):
    """405 Method Not Allowed"""
    pass


def parse_request(data):
    data = data.decode('utf-8')
    data = data.splitlines()

    # Parsing the Request-Line
    # Request-Line body: Method Request-URI HTTP-Version
    method, uri, version = data[0].split(' ')

    if method not in methods:
        raise MethodNotAllowed  # Return Error 405 to Client

    if ".." in uri:
        # TODO: Path Traversal Attempt Exception
        raise Exception

    if uri == '/':
        uri = "index.html"
    return Request(method, uri, version)


class Request():
    def __init__(self, method, uri, version):
        self.method = method
        self.uri = uri
        self.version = version


class Response():
    def __init__(self, data, content_type=mime_types[".html"], content_length=None,
                 status=200, status_msg=None, version="HTTP/1.1"):
        self.status = status
        self.status_msg = status_codes[self.status]
        self.version = version
        self.content_type = content_type
        self.data = data
        self.content_length = len(self.data)

    def get_raw(self):
        return f"""{self.version} {self.status} {self.status_msg}
Content-Type: {self.content_type}
Content-Length: {self.content_length}

{self.data.decode('utf-8')}
""".encode('utf-8')
