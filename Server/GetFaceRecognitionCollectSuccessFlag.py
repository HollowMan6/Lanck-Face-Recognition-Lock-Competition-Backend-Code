def get_FaceRecognitionCollectSuccess_flag(index) :
    import os
    ImagePath = r'./Query/' + str(index)
    s = ""
    for f in os.listdir(ImagePath):
            if f.endswith('txt'):
                file = open(ImagePath + '/' + f, encoding = 'gbk')
                s=file.read()
                print(s)
                break
    return s


if __name__ == '__main__':
    get_FaceRecognitionCollectSuccess_flag('xxxxxx')
