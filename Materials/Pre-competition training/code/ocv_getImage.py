import cv2
def get_rtsp():
    cap = cv2.VideoCapture("rtsp://172.23.33.230:8554/live1.h264")
    print (cap.isOpened())
    while cap.isOpened():
        success,frame = cap.read()
        cv2.imshow("frame",frame)
        cv2.waitKey(1)
