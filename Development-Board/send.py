# -*- coding=utf-8 -*-

# 导入库 Import Library
import socket
import os
import sys
import struct
import cv2
import numpy as np

def socket_client(filepath):
    try:
        # socket参数配置 Parameter configuration
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 在这里填入正确的ip 和端口号 fill in correct ip and port number here
        s.connect(('127.0.0.1', 8008))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while True:
        if os.path.isfile(filepath):
            # 发送文件名和大小信息(这里废弃文件的其它属性) Send file name and size information (other properties of  files are discarded here)
            # 128si: 定义这些信息由128位长度字符串和int数字组成 128si: Defines that this information consists of 128-bit length strings and interger
            # 打包数据 Pack data
            fhead = struct.pack('128si', os.path.basename(
                filepath).encode('utf-8'), os.stat(filepath).st_size)
            s.send(fhead)
            print("正在将路径为 {0} 的文件发送到服务器......".format(filepath))

            fp = open(filepath, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    print('文件 {0} 发送完毕...'.format(os.path.basename(filepath)))
                    break
                s.send(data)
        s.close()
        break


if __name__ == '__main__':
    filepath = "./Facedata/User.xxxxxxxxxxxx.1.jpg"
    socket_client(filepath)
