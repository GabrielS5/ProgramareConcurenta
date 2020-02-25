import socket
import sys
import time

startTime = time.time()
bytesSent = 0
messagesSent = 0

IP = "127.0.0.1"
UDP_PORT = 5005
TCP_PORT = 5006
messageSize = 10000 if len(sys.argv) < 5 else int(sys.argv[4])
totalSendSize = 100 if len(sys.argv) < 4 else int(sys.argv[3])
mechanism = "stop-and-wait" if len(sys.argv) < 3 else sys.argv[2]
protocol = "udp" if len(sys.argv) == 1 else sys.argv[1]

with open('data.txt', 'r') as file:
    data = file.read().replace('\n', '')

if protocol == "udp":
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(1)

    if mechanism == "streaming":
        for i in range(0,totalSendSize):
            chunks = [data[j:j+messageSize] for j in range(0, len(data), messageSize)]
            for chunk in chunks:
                sock.sendto(str.encode(str(chunk)), (IP, UDP_PORT))
                bytesSent += len(chunk)
                messagesSent += 1

    if mechanism == "stop-and-wait":
        for i in range(0,totalSendSize):
                chunks = [data[j:j+messageSize] for j in range(0, len(data), messageSize)]
                for chunk in chunks:
                    acknowledged = False
                    sock.sendto(str.encode(str(chunk)), (IP, UDP_PORT))
                    bytesSent += len(chunk)
                    messagesSent += 1
                    while not acknowledged:
                        try:
                            ackMessage, address = sock.recvfrom(1024)
                            acknowledged = True
                        except socket.timeout:
                            sock.sendto(str.encode(str(chunk)), (IP, UDP_PORT))
                            bytesSent += len(chunk)
                            messagesSent += 1

if protocol == "tcp":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect((IP, TCP_PORT))

    if mechanism == "streaming":
        for i in range(0,totalSendSize):
            chunks = [data[j:j+messageSize] for j in range(0, len(data), messageSize)]
            for chunk in chunks:
                sock.send(str.encode(str(chunk)))
                bytesSent += len(chunk)
                messagesSent += 1

    if mechanism == "stop-and-wait":
        for i in range(0,totalSendSize):
            chunks = [data[j:j+messageSize] for j in range(0, len(data), messageSize)]
            for chunk in chunks:
                acknowledged = False
                sock.send(str.encode(str(chunk)))
                bytesSent += len(chunk)
                messagesSent += 1
                while not acknowledged:
                    try:
                        ackMessage = sock.recv(65535)
                        acknowledged = True
                    except socket.timeout:
                        sock.send(str.encode(str(chunk)))
                        bytesSent += len(chunk)
                        messagesSent += 1

    sock.close()

elapsedTime = time.time() - startTime

print("Elapsed Time : " + str(elapsedTime))
print("Messages Sent : " + str(messagesSent))
print("Bytes Sent : " + str(bytesSent))
time.sleep(3)