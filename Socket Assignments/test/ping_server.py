import socket
import sys
from threading import Thread

PORT = 2000
BUFFERSIZE = 256
PREFIX = "PONG-"

def makePongMsg(data):
    if data[:5] == "PING-" and data[-1] == '!':
        return PREFIX+data[5:-1]+'!'

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('0.0.0.0', PORT))
    while True:
        # input()

        dataGram = serverSocket.recvfrom(BUFFERSIZE)
        data = dataGram[0].decode("utf-8")
        if data and makePongMsg(data):
            serverSocket.sendto(makePongMsg(data).encode(), dataGram[1])




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
