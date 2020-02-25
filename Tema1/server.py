import socket
import sys
from threading import Thread
import datetime
import time

IP = "127.0.0.1"
UDP_PORT = 5005
TCP_PORT = 5006
protocol = "udp" if len(sys.argv) == 1 else sys.argv[1]
ackMessage = "acknowledged"

def handleTcp(connection):
    bytesReceived = 0
    messagesReceived = 0
    try:
        totalBytes = 0
        while 1:
            data = connection.recv(65535)
            messagesReceived += 1
            bytesReceived += len(data)
            if not data: break
            connection.send(str.encode(ackMessage))
        connection.close()
    except:
        print("finished")
    print("Protocol Used: TCP")
    print("Messages Received : " + str(messagesReceived))
    print("Bytes Received : " + str(bytesReceived))

def handleUdp(clientsDict):
    while True:
        time.sleep(0.5)
        toBeRemoved = []
        for key,client in clientsDict.items():
            clientDate = client["lastAdded"] + datetime.timedelta(0,1)
            if clientDate < datetime.datetime.now():
                print("Protocol Used: UDP")
                print("Messages Received : " + str(client["messagesReceived"]))
                print("Bytes Received : " + str(client["bytesReceived"]))
                toBeRemoved.append(key)
        for client in toBeRemoved:
            clientsDict.pop(client)


if protocol == "udp":
    bytesReceived = 0
    messagesReceived = 0
    usedAddr = False
    clientsDict = {}
    thread = Thread(target = handleUdp, args = (clientsDict, ))
    thread.start()
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind((IP, UDP_PORT))
    while True:
        data, addr = socket.recvfrom(65535)
        if addr not in clientsDict:
            clientsDict[addr] = {
                "messagesReceived": 1,
                "bytesReceived": len(data),
                "lastAdded": datetime.datetime.now()
            }
        else:
            pastData = clientsDict[addr]
            clientsDict[addr] = {
                "messagesReceived": pastData["messagesReceived"] + 1,
                "bytesReceived": pastData["bytesReceived"] + len(data),
                "lastAdded": datetime.datetime.now()
            }
        socket.sendto(str.encode(ackMessage), addr)

if protocol == "tcp":
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((IP,TCP_PORT))
    socket.listen(1) 
    while 1:
        conn, addr = socket.accept()
        thread = Thread(target = handleTcp, args = (conn, ))
        thread.start()