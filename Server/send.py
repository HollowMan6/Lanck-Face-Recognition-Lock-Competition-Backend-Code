# -*- coding=utf-8 -*-

# 导入库 Import Library
import socket
import sys

def socket_client(string):
    try:
        # socket参数配置 Parameter configuration
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f=open("addr.txt",'r')
        ip=f.readline().replace("\n",'')
        # 在这里填入正确的ip 和端口号 fill in correct ip and port number here
        s.connect((ip, 8018))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    s.send(bytes(string, encoding="UTF-8"))

if __name__ == '__main__':
    string = "Hello World!"
    socket_client(string)
