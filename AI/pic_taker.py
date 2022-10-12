import cv2
from facenet_pytorch import MTCNN
import sys
import os
import time
import tensorflow as tf

now = int(time.time())


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


counter_max = 750  # amount of pics before program quits
dir_loc = "testfolder"  # directory where folders will be saved
cam = cv2.VideoCapture(1)
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
            x = int(face[0])
            y = int(face[1])
            x2 = int(face[2])
            y2 = int(face[3])

            if x > 0 and y > 0 and y2 > 0 and x2 > 0 and x2-x > 140 and y2-y > 140:
                cropped_img = frame[y:y2, x:x2]

                reimage = cv2.resize(cropped_img, (224, 224))
                cv2.imwrite(f"{dir_loc}/{label}/{label}_{now}_{counter}.jpg", reimage)
                counter += 1
                print(counter)
                if counter > counter_max:
                    quit()

    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1280, 720)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()