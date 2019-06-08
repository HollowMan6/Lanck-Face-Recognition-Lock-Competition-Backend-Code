# coding: utf-8
# 前端测试是否眨眼，用于活体检测 Front-end test blinks for biopsy
from scipy.spatial import distance as dist
from imutils import face_utils
import time
import dlib
import cv2


def eye_aspect_ratio(eye):
    # 计算两只眼睛之间的垂直欧式距离
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # 计算两眼之间的水平欧式距离
    C = dist.euclidean(eye[0], eye[3])

    # 计算眼睛纵横比
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


def main():
    shape_predictor = "shape_predictor_68_face_landmarks.dat"
    EYE_AR_THRESH = 0.27  # 阈值
    EYE_AR_CONSEC_FRAMES = 33   # the number of consecutive frames the eye must be below the threshold

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    # grab the indexes of the facial landmarks for the left and right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    print("[INFO] print q to quit...")

    vs = cv2.VideoCapture(1)
    time.sleep(1.0)

    # loop over frames from the video stream
    while True:
        # grab the frame from the threaded video file stream, resize it, and convert it to grayscale channels)
        _, frame = vs.read()
        frame = cv2.resize(frame, (0, 0), fx=0.75,fy=0.75)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink threshold
            else:
                # if the eyes were closed for a sufficient number of then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    return 1
                    

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
     
