#!/usr/bin/env python
# coding=utf-8
import socket
import datetime
import time
import os


#初始化Server_socket
def Server_init(local_host):
    server_socket = socket.socket()                                         #创建socket对象
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #当进程结束后立即释放端口占用
    server_socket.bind(tuple(local_host))                                   #绑定本机ip和端口
    server_socket.listen(100)
    print('server_socket starts to listening %s:%s'%(local_host[0],local_host[1]))
    return server_socket
#Server业务
def Server_run(server_socket):    
    #如果有客户端进行连接、则接受客户端的连接
    while True:
        #返回客户端socket通信对象和客户端的ip
        clientSocket,addr =  server_socket.accept()
        #客户端与服务端进行通信
        data = clientSocket.recv(1024).decode('utf-8')
        print('[%s][Info from%s]:%s\n'%(str(datetime.datetime.now()),str(addr),data))
        #服务端给客户端回消息
        clientSocket.send(b'ok')
        #判断来者的ip地址 根据包内容判断是否开锁
        if addr[0]==dst_host[0]:
            if data=="unlock":
                unlock()
        #关闭socket对象
        clientSocket.close()    #客户端对象

#开锁
def unlock():
    print("unlock!")
    os.system("echo 'fa'  | sudo -S sh lock.sh low")
    time.sleep(10)
    os.system("echo 'fa' | sudo -S sh lock.sh high")

#获取本机IP地址
# 与谷歌的公共DNS服务器 8.8.8.8:80建立socket连接 再返回本地socket地址
def get_host():
    host="0.0.0.0"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host = s.getsockname()[0]
    finally:
        s.close()
    return host

#host是包含ip和port的元组 content为utf8字符串
def send_data(host,content):
    content=bytes(content,encoding="utf8")
    client_socket=socket.socket()
    try:
        client_socket.connect(host)
        client_socket.send(content)
    except:
        print("Connect to ",host," Fail!")
    client_socket.close()

#后端地址
dst_host=["172.16.252.137",8001]
#前端地址
local_host=[get_host(),8001]

#通知后端更新 前端的ip地址
send_data(tuple(dst_host),"update&"+local_host[0])
#监听来自后端的请求
Server_run(Server_init(local_host))
##通知后端 采集数据进行分析
#send_data(tuple(dst_host),"datas&"+"Go on!")










