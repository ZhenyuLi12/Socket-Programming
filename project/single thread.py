#learn from
#https://docs.python.org/3/library/threading.html
#https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.25
#sagarsv
import socket
import os
import time
from os import path
import sys
import threading
from urllib.parse import urlparse

serverName="localhost"
serverPort=12000
TIMEOUT=10
isModified=False
mtime=""

def myParse(req):
    request_filename = req.split()[1]
    filename = ""
    for x in range(len(request_filename)-1):
        filename += request_filename[x+1]
        
    print ("This is requested filename: ", filename)
    return filename

def sendResponse(status,fname):
    dResponse=""
    if status==200:
        dResponse=dResponse+"HTTP/1.1 {0} {1}\r\n".format(status, "OK")
    elif status==404:
        dResponse=dResponse+"HTTP/1.1 {0} {1}\r\n".format(status, "Not Found")
    elif status==400:
        dResponse=dResponse+"HTTP/1.1 {0} {1}\r\n".format(status, "Bad Request")
    elif status==304:
        dResponse=dResponse+"HTTP/1.1 {0} {1}\r\n".format(status, "Not Modified")
    elif status==408:
        dResponse=dResponse+"HTTP/1.1 {0} {1}\r\n".format(status, "Request Timed Out")
    return dResponse

def receiveConnection(con,addr):
    global isModified, mtime
    request = con.recv(1024).decode()
    if request=="" or request.split()[0]!='GET':
        dResponse=sendResponse(400,'400.html')
        dResponse=dResponse.encode()
        con.sendall(dResponse)
        sendFile(con,'400.html')


    else:
        fname=myParse(request)
        if path.exists(fname)==1:
            if isModified==False:
                dResponse=sendResponse(200,fname)
                mtime=time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime(os.path.getmtime(fname)))
                dResponse=dResponse+"Last-Modified: {}\r\n".format(mtime)
                dResponse=dResponse.encode()
                con.sendall(dResponse)
                sendFile(con,fname)
                isModified=True
            else:
                dResponse=sendResponse(304,'304.html')
                dResponse=dResponse.encode()
                con.sendall(dResponse)
                sendFile(con,'304.html')
        else:
            dResponse=sendResponse(404,fname)
            dResponse=dResponse.encode()
            con.sendall(dResponse)
            sendFile(con,'404.html')
    con.close()
        
def sendFile(con,fname):
    content = open(fname, "rb")
    while True:
        content_data = content.read()
        if content_data==b"":
            break
        else:
            con.send(content_data)


def startServer(serverSocket):
    isRun=True
    while isRun:
        try:
            print("Server 'localhost' is listening.")
            connectionSocket, addr = serverSocket.accept()
            #if connectionSocket:
                #thread = threading.Thread(target=receiveConnection, args=(connectionSocket, addr))
                #thread.start()
            receiveConnection(connectionSocket, addr)
            print ("My IP address and port are: ",addr)
        except KeyboardInterrupt:
            print ('Interrupted')
            isRun = False
        except socket.timeout:
            print ('Timeout')
            isRun = False
        time.sleep(0.05)

def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.settimeout(TIMEOUT)
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(5)
    startServer(serverSocket)

if __name__ == '__main__':
	main()
    
