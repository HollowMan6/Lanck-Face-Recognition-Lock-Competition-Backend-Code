# -*- coding=utf-8 -*-

#=====PART4 人脸识别=====
import cv2
import os
from PIL import Image

#传入index,FaceRecognitionCollectSuccess_flag，传出opendoor_flag
def face_recognition(index,FaceRecognitionCollectSuccess_flag):

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(r'./Train.xml')
    ImagePath = r'./Query/' + str(index)

    opendoor_flag = 0
    if not FaceRecognitionCollectSuccess_flag==1 :
        print('识别数据收集错误！')
    else :
        count = 0
        def getNames():
            DataPath = r'./Data'
            names = []
            cards=[]
            for f in os.listdir(DataPath):
                file = open(DataPath + '/' + f, encoding = 'gbk')
                s=file.read()
                text = s.split(' ')
                names.append(text[0])
                cards.append(text[-1])
                file.close()
            return names,cards

        names,cards=getNames()
        recognizer.read('face_trainer/trainer.yml')

        #筛选'jpg'文件并加入到paths列表中
        paths=[]
        for f in os.listdir(ImagePath):
            if f.endswith('jpg'):
                paths.append(os.path.join(ImagePath, f))

        for path in paths:
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # 转为灰度图片
            faces = detector.detectMultiScale(gray, 1.3, 5)   # 检测人脸
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
                count += 1
                cv2.imwrite(path, gray[y: y + h, x: x + w])   # 保存图像

            img_BGR = cv2.imread(path)
            img_GRAY = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)
            card,confidence = recognizer.predict(img_GRAY)
            def card_find_name(ID):
                i=-1
                names,cards=getNames()
                for card in cards:
                    i=i+1
                    if card==ID:
                        return names[i]
            card=str(card)
            for i in cards:
                temp = i[0]+i[3:5]+i[-5:-1]
                if card==temp:
                    card=i
                    break
            name = card_find_name(card)
            probability = str(100-confidence) + '%'
            print(card, name, probability)
            if confidence < 60:
                count += 1

        if count>=15 :
            opendoor_flag = 1
            print('开门成功！')
        else:
            opendoor_flag = 0
            print('开门失败！')

    return opendoor_flag

if __name__ == '__main__':
    face_recognition('xxxxxx',1)
