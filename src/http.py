status_codes = {
    # Informational
    100: "Continue",
    101: "Switching Protocols",

    # Successful
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",

    # Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",   # 306 is missing because it is unused since HTTP/1.1
    307: "Temporary Redirect",

    # Client Error
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",

    # Server Error
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
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
    ".css":     "text/css",
    ".xml":     "text/xml",
    ".csv":     "text/csv",
    ".txt":     "text/plain",
    ".json":    "application/json",
    ".js":      "application/javascript",
    ".zip":     "application/zip",
    ".pdf":     "application/pdf",
    ".sql":     "application/sql",
    ".doc":     "application/msword",
    ".docx":    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls":     "application/vnd.ms-excel",
    ".xlsx":    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt":     "application/vnd.ms-powerpoint",
    ".pptx":    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".odt":     "application/vnd.oasis.opendocument.text",
    ".zst":     "application/zstd",
    ".mp3":     "audio/mpeg",
    ".ogg":     "audio/ogg",
    ".jpg":     "image/jpeg",
    ".jpeg":    "image/jpeg",
    ".png":     "image/png",
    ".gif":     "image/gif"

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
