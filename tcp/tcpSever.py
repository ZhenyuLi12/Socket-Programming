# Learned how to implement the case of 404 from: https://stackoverflow.com/questions/41852380/how-to-abort-a-python-script-and-return-a-404-error

from socket import *

# Server name and port number
serverName = 'localhost'
serverPort = 12000

FLAG = False

# Creat a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)


# The server is constantly waiting for request
while True:
    print("Server 'localhost' is listening.")
    connectionSocket, addr = serverSocket.accept()

    try: 

        client_request = connectionSocket.recv(1024).decode()
        print (client_request)


        http_header = {
            "status_line" : "HTTP/1.1 200 OK\r\n",
            "Accept-Ranges":"bytes\r\n",
            "Content-Length": len(client_request)+"\r\n",
            "Connection": "Keep-Alive\r\n",
            "Content-Type": "text/html\r\n"

        }
        http_header = http_header + "\r\n"
        print (http_header)
        connectionSocket.send(http_header.encode())
        connectionSocket.close()

    except:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send("Content-Type: text/html\r\n\r\n")
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>')
        connectionSocket.send('<html><head></head><body><div>The requested URL was not found on this server</div></body></html>')
        connectionSocket.close()

serverSocket.close()