
# 用于实现微信小程序一键开锁
from socket import *
import sys


def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def receive():
    sock = socket(AF_INET, SOCK_STREAM)
#    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((get_host_ip(), 8018))
#    print(get_host_ip())
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.listen(5)
    while True:
        newServerSocket, destAddr = sock.accept()
        recvData = newServerSocket.recv(1024)
        if recvData:
            print("receive a post.")
            print(recvData)

if __name__ == "__main__":
    receive()
