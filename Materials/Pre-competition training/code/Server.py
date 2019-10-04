#!/usr/bin/env python
# coding=utf-8
import socket
import datetime



#初始化Server_socket
def Server_init(local_host):
    server_socket = socket.socket()                                         #创建socket对象
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #当进程结束后立即释放端口占用
    server_socket.bind(tuple(local_host))                                   #绑定本机ip和端口
    server_socket.listen(100)
    print('server_socket starts to listening %s:%s'%(local_host[0],local_host[1]))
    return server_socket
#Server业务
def Server_run(server_socket,dst_host):
    while True:
        clientSocket,addr =  server_socket.accept()                         #监听到客户端通信请求
        data = clientSocket.recv(1024).decode('utf-8')                      #解析客户端通信内容 bytes
        print('[%s][Info from%s]:%s\n'%(str(datetime.datetime.now()),str(addr),data))

        #更新目标host
        if "update" in data:
            dst_host[0]=data.split("&")[-1]
            print("Update dst %s"%(dst_host))
            clientSocket.send(b"ok")        #响应请求端
        #接收开锁命令转发开发板
        elif "unlock" in data:
            print("send unlock to %s"%(dst_host[0]))
            clientSocket.send(b"ok")
            send_data(tuple(dst_host),"unlock")
        #获取采集数据
        elif "data" in data:
            #调用opencv 从rtsp://172.23.33.230:8554/live1.h264 读取视频流进行分析
            #get_rtsp()
            clientSocket.send(b"ok")

        #关闭socket对象
        clientSocket.close()
#host是包含ip和port的元组 content为utf8字符串
def send_data(host,content):
    content=bytes(content,encoding="utf8")
    with socket.socket() as client_socket:
        try:
            client_socket.connect(host)
            client_socket.send(content)
        except Exception:
            print("Connect to ",host," Fail!")


#后端地址
local_host=["172.16.252.137",8001]
#前端地址
dst_host=["0.0.0.0",8001]

#监听来自前端的请求
Server_run(Server_init(local_host),dst_host)