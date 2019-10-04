# -*- coding=utf-8 -*-

# 导入库 Import Library
import socket
import threading
import sys
import os
import struct
import traceback
import FaceTraining
import FaceRecognition
import send
import GetFaceRecognitionCollectSuccessFlag
import GetFaceDataCollectSuccessFlag


# 查询本机ip地址 get host ip
def get_host_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            pass
    return ip


def socket_service():
    try:
        # socket参数配置 Parameter configuration
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((get_host_ip(), 8008))
        s.listen(10)
        ip, port = s.getsockname()
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    # The current server IP address is ... and the receiving service port number is:
    print('当前服务器ip地址为: {0}, 接收服务端口号为: {1}'.format(ip, port))
    print('等待连接中...')  # Waiting for the connection...

    while True:
        conn, addr = s.accept()

        # 多线程处理文件发送请求 Multithread Processing File Send Request
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    # Received a new connection request from
    print('\n收到了从 {0}:{1} 发来的一个新的连接请求'.format(addr[0], addr[1]))
    FaceDataCollectSuccess_flag=1
    while True:
        try:
            # 首先接收文件名和大小信息(这里不接收文件的其它属性)
            # Firstly receive the file name and size information(no other attributes of the file are received here)
            # 128si: 定义这些信息由128位长度字符串和int字符组成
            # 128si: Defines that this information consists of 128-bit length strings and int characters
            fileinfo_size = struct.calcsize('128si')
            buf = conn.recv(fileinfo_size)
            if buf:
                # 解包发送过来的文件信息 Unpack file information
                filename, filesize = struct.unpack('128si', buf)
                # 解码文件名称 Decode file name
                fn = filename.decode().strip('\00')

                recvd_size = 0
                # 定义已接收文件的大小 Define the size of the received file
                if fn[0:5]=="Asker" and fn[-3:]=="txt":
                    isExists = os.path.exists('./Query/'+fn[6:12])
                    if not isExists:
                        os.makedirs('./Query/'+fn[6:12])
                    fp = open("./Query/"+fn[6:12]+"/"+fn, 'wb')
                    print('开始接收...')  # Begin receiving
                    # 接收文件主体数据 Receiving file body data
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            data = conn.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = conn.recv(filesize - recvd_size)
                            recvd_size = filesize
                        fp.write(data)
                    fp.close()
                    if GetFaceRecognitionCollectSuccessFlag.get_FaceRecognitionCollectSuccess_flag(fn[6:12]) == "1":
                        send.socket_client(str(FaceRecognition.face_recognition(fn[6:12], FaceDataCollectSuccess_flag)))
                    else:
                        send.socket_client("0")
                elif fn[0:4] == "User" and fn[-3:] == "txt":
                    if fn[-8:-4]=='flag':
                        fp = open("./Facedata_flag/"+fn, 'wb')
                        print('开始接收...')  # Begin receiving
                        # 接收文件主体数据 Receiving file body data
                        while not recvd_size == filesize:
                            if filesize - recvd_size > 1024:
                                data = conn.recv(1024)
                                recvd_size += len(data)
                            else:
                                data = conn.recv(filesize - recvd_size)
                                recvd_size = filesize
                            fp.write(data)
                        fp.close()
                        if GetFaceDataCollectSuccessFlag.get_FaceDataCollectSuccess_flag(int(fn[5:-9])) == 0:
                            pass
                    else:
                        fp = open("./Data/"+fn, 'wb')
                        print('开始接收...')  # Begin receiving
                        # 接收文件主体数据 Receiving file body data
                        while not recvd_size == filesize:
                            if filesize - recvd_size > 1024:
                                data = conn.recv(1024)
                                recvd_size += len(data)
                            else:
                                data = conn.recv(filesize - recvd_size)
                                recvd_size = filesize
                            fp.write(data)
                        fp.close()
                elif fn[0:4] == "User" and fn[-3:]=="jpg":
                    fp = open("./Facedata/"+fn, 'wb')
                    print('开始接收...')  # Begin receiving
                    # 接收文件主体数据 Receiving file body data
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            data = conn.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = conn.recv(filesize - recvd_size)
                            recvd_size = filesize
                        fp.write(data)
                    fp.close()
                    if fn[-7:-4]=="200":
                        FaceTraining.face_training()
                elif fn[0:5] == "Asker" and fn[-3:] == "jpg":
                    isExists = os.path.exists('./Query/'+fn[6:12])
                    if not isExists:
                        os.makedirs('./Query/'+fn[6:12])
                    fp = open("./Query/"+fn[6:12]+'/'+fn, 'wb')
                    print('开始接收...')  # Begin receiving
                    # 接收文件主体数据 Receiving file body data
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            data = conn.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = conn.recv(filesize - recvd_size)
                            recvd_size = filesize
                        fp.write(data)
                    fp.close()
                else:
                    fp = open(fn, 'wb')
                    print('开始接收...')  # Begin receiving
                    # 接收文件主体数据 Receiving file body data
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            data = conn.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = conn.recv(filesize - recvd_size)
                            recvd_size = filesize
                        fp.write(data)
                    fp.close()
                print('接收结束！')  # Receiving finished
                # The received file name is ... and the file size is ... bytes.
                print('接收到的文件名为 {0}, 文件大小为 {1} 字节'.format(fn, filesize))
                f = open("addr.txt", 'w')
                f.write(addr[0])
                f.close()
                print('\n等待连接中...')  # Waiting for the connection...
            conn.close()
        except Exception:
            traceback.print_exc()
            print(buf)
            print("请求操作失败！")  # The request operation failed!
            conn.close()
            print('\n等待连接中...')  # Waiting for the connection...
        break


if __name__ == '__main__':
    socket_service()
