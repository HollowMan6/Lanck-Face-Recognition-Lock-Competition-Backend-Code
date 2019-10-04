# -*- coding=utf-8 -*-
#导入模块
import cv2
import os
import numpy as np
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(r'./Train.xml')
path = './Facedata'   # 人脸数据路径,服务器中需要把所有图片放在这一个文件夹中


#创建目录
def face_trainer_mkdir():
    path=r"./face_trainer"
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        print(path+' 目录已存在')
        return False

    
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    cards = []
    for imagePath in imagePaths:
        img = cv2.imread(imagePath)
        gray = cv2.imread(imagePath,0)
        faces = detector.detectMultiScale(gray, 1.3, 5)   # 检测人脸
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
            cv2.imwrite(imagePath, gray[y: y + h, x: x + w])   # 保存图像
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        face_card = os.path.split(imagePath)[-1].split(".")[1]
        face_card = face_card[0]+face_card[3:5]+face_card[-5:-1]
        card = int(face_card)
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            cards.append(card)
    return faceSamples, cards


def face_training():
    print('正在训练. 请等待 ...')
    faces, cards = getImagesAndLabels(path)
    recognizer.train(faces, np.array(cards))
    recognizer.write(r'./face_trainer/trainer.yml')
    print("{0} 个人脸数据已训练成功！".format(len(np.unique(cards))))

if __name__ == '__main__':
    face_trainer_mkdir()
    face_training()

