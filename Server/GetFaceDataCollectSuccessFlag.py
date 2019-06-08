def get_FaceDataCollectSuccess_flag(card) :
    import os
    Path = r'./Facedata_flag/User.' + str(card) + '.flag.txt'
    s = 0
    File = open(Path)
    s=File.read()
    print(s)
    return int(s)
            

if __name__ == '__main__':
    get_FaceDataCollectSuccess_flag(123456789013)
