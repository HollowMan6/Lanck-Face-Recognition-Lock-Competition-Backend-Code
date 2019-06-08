# -*- coding=utf-8 -*-

#=====PART1 人脸录入=====

#导入模块
import cv2
import os
import time
import send
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(r'./Train.xml')
FaceDataCollectSuccess_flag = 0

#创建目录
def card_mkdir(card):
    path=r"./users/" + str(card)
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        print(path+' 目录已存在')
        return False


#保存姓名、校园卡号到该目录下的TXT文件并上传
def data_save(name,card):
    path = r'./users/' + str(card) +'/User.' + str(card) + '.txt'
    file = open(path,'w')             
    file.write(name)
    file.write(' ')
    file.write(str(card))
    file.close()
    send.socket_client(path)

def flag_save(card,flag):
    path = r'./users/' + str(card) + '/User.' + str(card) + '.flag.txt'
    file = open(path,'w')             
    file.write(str(flag))
    file.close()
    send.socket_client(path)


#输入姓名、校园卡号
#保存图像到该目录下并上传
def face_save():

    face_name = input('\n 请输入你的姓名:')   #外接小程序
    face_card = input('\n 请输入你的校园卡号:')   #外接小程序
    while len(face_card)!=12:
        face_card = input('\n 校园卡号必须为12位,请重新输入:')
    card_mkdir(face_card)
    data_save(face_name, face_card)
    
    cap = cv2.VideoCapture(0)   # 调用摄像头
    print('\n 请看向摄像头并等待一会儿...')
    
    count = 0
    start = time.time()
    
    while True:
        
        end = time.time()
        
        sucess, img = cap.read()   # 从摄像头读取图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # 转为灰度图片
        faces = detector.detectMultiScale(gray, 1.3, 5)   # 检测人脸
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
            count += 1
            path = r"./users/" + str(face_card) + '/User.' + str(face_card)+ '.' + str(count) + '.jpg'
            cv2.imwrite(path, gray[y: y + h, x: x + w])   # 保存图像
            send.socket_client(path)   #上传图像
            cv2.imshow('image', img)
            
        k = cv2.waitKey(1)   # 保持画面的持续
        
        if k == 27:   # 通过esc键退出摄像
            FaceDataCollectSuccess_flag = 0
            print('您已按下ESC键退出录入！')
            break
        elif (end - start) > 30:   # 超过30s退出摄像
            FaceDataCollectSuccess_flag = 0
            print('录入超时！请检查您当前光线是否良好后重新录入。')
            break
        elif count >= 200:   # 得到200个样本后退出摄像
            FaceDataCollectSuccess_flag = 1
            print('录入成功！')
            break
        
    cap.release()   # 关闭摄像头
    cv2.destroyAllWindows()

    flag_save(face_card,FaceDataCollectSuccess_flag)   #录入数据是否异常


if __name__ == '__main__':
    FaceDataCollect_flag = 1   #人脸录入请求
    if FaceDataCollect_flag==1 :
        face_save()
