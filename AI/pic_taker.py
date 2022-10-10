import cv2
from facenet_pytorch import MTCNN
import sys
import os

dir_loc = "testfolder"  # directory where folders will be saved
cam = cv2.VideoCapture(0)
cam.set(3, 3840)  # set width
cam.set(4, 2160)  # set height

detector = MTCNN()
label = sys.argv[1]
path = f"{dir_loc}/{label}"
if os.path.exists(path):
    print("folder already exists")
    quit()

os.mkdir(path)
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

            if x > 0 and y > 0 and y2 > 0 and x2 > 0 and x2-x > 120 and y2-y > 120:
                cropped_img = frame[y:y2, x:x2]

                cv2.imwrite(f"{dir_loc}/{label}/{label}_{counter}.jpg", cropped_img)
                counter += 1
                print(counter)
                if counter > 750:
                    quit()

    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1280, 720)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()