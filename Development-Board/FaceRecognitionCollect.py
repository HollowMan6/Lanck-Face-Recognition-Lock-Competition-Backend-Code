# -*- coding=utf-8 -*-

#=====PART3 人脸识别录入=====

import send
import cv2
import os
import time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import random

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(r'./Train.xml')
FaceRecognitionCollectSuccess_flag = 0


'''
'''
#创建目录
def askers_mkdir():
    path=r"./askers"
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        print(path+' 目录已存在')
        return False

def flag_save(index,flag):
    path = r'./askers/Asker.' + str(index) + '.txt'
    file = open(path,'w')             
    file.write(str(flag))
    file.close()
    send.socket_client(path)

def FaceRecognitionCollect():
    cam = cv2.VideoCapture(0)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    count = 0
    index = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',6))   #生成6位索引码
    print('请按ESC键退出')
    
    #start = time.perf_counter()
    
    while True:
        #end = time.perf_counter()
        
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            count += 1
            path = r"./askers/Asker." + str(index) + '.' + str(count) + '.jpg'
            cv2.imwrite(path, gray[y: y + h, x: x + w])   # 保存图像
            send.socket_client(path)   #上传图像
            cv2.imshow('image', img)

        k = cv2.waitKey(1)   # 保持画面的持续
        
        if k == 27:   # 通过esc键退出摄像
            FaceRecognitionCollectSuccess_flag = 0
            print('您已按下ESC键退出录入！')
            break
        #elif (end - start) > 15:   # 超过15s退出摄像
            #FaceRecognitionCollectSuccess_flag = 0
            #print('识别超时！请检查您当前光线是否良好后重新录入。')
            #break
        elif count >= 20:   # 得到20个样本后退出摄像
            FaceRecognitionCollectSuccess_flag = 1
            print('数据已上传，正在识别 ...')
            break
        
    cam.release()   # 关闭摄像头
    cv2.destroyAllWindows()
    
    flag_save(index,FaceRecognitionCollectSuccess_flag)   #识别数据是否异常


if __name__ == '__main__':
    askers_mkdir()
    FaceReognitionCollect_flag = 1   #人脸识别录入请求
    if FaceReognitionCollect_flag==1 :
        FaceRecognitionCollect()
