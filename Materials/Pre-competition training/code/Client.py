#!/usr/bin/env python
# coding=utf-8
import socket

#host是包含ip和port的元组 content为utf8字符串
def Client_send(host,content):
    content=bytes(content,encoding="utf8")
    client_socket=socket.socket()
    client_socket.connect(host)
    client_socket.send(content)
    data=client_socket.recv(1024).decode("utf-8")
    print(data)
    client_socket.close()
    if data == "ok":
        return True
    else:
        return False





##采集数据 发往服务端
Client_send(("172.16.252.137",8001),"unlock")

#Client_send(("172.23.198.235",8001),"unlock")









