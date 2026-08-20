# 1) create socket (AF_INET, SOCK_STREAM)
# 2) bind to (HOST, PORT) and listen
# 3) loop: accept a connection
# 4) recv bytes until you see b"\r\n\r\n" (end of HTTP headers)
# 5) parse the request line: method path HTTP_VERSION
# 6) if method != "GET": send 405 and close
# 7) if path == "/": set path = "/index.html"
# 8) map path to a file inside ./www (and prevent ../ traversal)
# 9) if file missing: send 404 and close
# 10) if file exists:
#       - send HTTP 200 headers (Content-Type + Content-Length, blank line)
#       - open file and stream bytes to the client
# 11) close connection
# 12) go back to accept next connection

import socket
from pathlib import Path

HOST = "0.0.0.0"

PORT = 8080

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print(f"Listening on ({HOST},{PORT})")
    while True:
        conn,addr = s.accept()
        with conn:
            print(f"Connection accepted from ({addr})")

            data=""
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(1024)

                if not chunk:
                    break

                data+=chunk
            
            end = data.find(b"\r\n\r\n")
            headers = data[:end+4]

            request_line = data.split(b"\r\n")[0].split(b" ")
            method = request_line[0].decode()
            path = request_line[1].decode()
            HTTP_VERSION = request_line[2].decode()

            if method!="GET":
                response = (
                    "HTTP/1.1 405 Method Not Allowed\r\n"
                    "Content-Length: 0\r\n"
                    "\r\n"
                )

                conn.sendall(response.encode())
                continue

            if path == "/":
                path = "/index.html"
            www = Path("./www").resolve()
            file_path = www / path.lstrip("/").resolve()

            if not file_path.is_relative_to(www):
                response = (
                    "HTTP/1.1 403 Forbidden\r\n"
                    "Content-Length: 0\r\n"
                    "\r\n"
                )

                conn.sendall(response.encode())
                continue

            if not file_path.is_file():
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    "Content-Length:22\r\n"
                    "\r\n"
                    "<h1>404.Page Not Found</h1>"
                )

                conn.sendall(response.encode())
                continue

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {file_path.stat().st_size}\r\n"
                "\r\n"
            )
            
            conn.sendall(response.encode())

            with open(file_path,"rb") as f:
                while True:
                    chunk = f.read(4096)

                    if not chunk:
                        break
                        
                    conn.sendall(chunk)






            


