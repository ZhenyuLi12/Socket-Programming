from socket import *
import sys

serverName = 'localhost'
serverPort = 12000
fileName = "test.html"

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    
    http_header = {
        "request_line": "GET /%s HTTP/1.1\r\n" %(fileName),
        "Accept": "text/html,application/xhtml+xml\r\n",
        "Accept-Language": "en-us,en;q=0.5\r\n",
        "Keep-Alive": "115\r\n",
        "Connection": "keep-alive\r\n"
    }
    http_header = http_header + "\r\n"
    print (http_header)
    clientSocket.send(http_header.encode())

except:
    sys.exit()

response = clientSocket.recv(1024).decode()
clientSocket.close()
print (response)