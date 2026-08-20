# 1) create socket (AF_INET, SOCK_STREAM)
# 2) bind to (HOST, PORT) and listen
# 3) loop: accept a connection
# 4) recv bytes until you see b"\r\n\r\n" (end of HTTP headers)
# 5) parse the request line: METHOD PATH HTTP_VERSION
# 6) if METHOD != "GET": send 405 and close
# 7) if PATH == "/": set PATH = "/index.html"
# 8) map PATH to a file inside ./www (and prevent ../ traversal)
# 9) if file missing: send 404 and close
# 10) if file exists:
#       - send HTTP 200 headers (Content-Type + Content-Length, blank line)
#       - open file and stream bytes to the client
# 11) close connection
# 12) go back to accept next connection

import socket

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

            while True:
                data = conn.recv(1024)
                if data:
                    print(f"Recieved : {data.decode()}")
                    conn.sendall(b"Greetings from the server!")
                if not data:
                    break

