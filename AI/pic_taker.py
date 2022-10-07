import cv2
from facenet_pytorch import MTCNN
import sys
import os

dir="testfolder" # directory where folders will be saved
cam = cv2.VideoCapture(0)
cam.set(3, 3840)  # set width
cam.set(4, 2160)  # set height

detector = MTCNN()
label = sys.argv[1]
os.mkdir(f"{dir}/{label}")
counter = 0
while True:
    check, frame = cam.read()
    if not check:
        print("Cant recive a frame from camera. exiting...")
        break

    faces, probability = detector.detect(frame)

    if faces is not None:
        for face in faces:
            # covert it into a list to access variables
            faceList = face.tolist()

            # cordinates for box around a face
            x, y, x2, y2 = faceList
            x = int(x)
            y = int(y)
            x2 = int(x2)
            y2 = int(y2)

            cropped_img = frame[y:y2, x:x2]

            cv2.imwrite(f"{dir}/{label}/{label}_{counter}.jpg", cv2.cvtColor(cropped_img, cv2.COLOR_2RGB))
            counter += 1

    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1280, 720)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()