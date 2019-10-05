
# 用于实现微信小程序一键开锁
from socket import *
import sys


def get_host_ip():
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
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
            sock1 = socket(AF_INET, SOCK_STREAM)
            id = (sys.argv[1], 16)
            sock1.connect(id)
            sock1.send('10'.encode("utf-8"))

if __name__ == "__main__":
    receive()
