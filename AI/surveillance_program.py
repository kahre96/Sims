import tensorflow as tf
from tensorflow import keras
import numpy as np
from facenet_pytorch import MTCNN
import cv2
import pickle
import collections as col
import requests

color = (0, 255, 0)
namecolor = (36, 255, 12)
guess_queue = col.deque(maxlen=20)
url= "http://localhost:5000/player/newEntry"

cam = cv2.VideoCapture(0)
cam.set(3, 3840)
cam.set(4, 2160)

labels = pickle.loads(open('labels.pickle', "rb").read())  # load the pickle file with labels
model = keras.models.load_model('models/Images_anoaug_wGlasses_N128x128.h5')

normalization_layer = tf.keras.layers.Rescaling(1./255)
detector = MTCNN()


while True:
    check, frame = cam.read()
    if not check:
        print("Cant recive a frame from camera. exiting...")
        break

    # faces store one array for each face
    faces, probability = detector.detect(frame)

    if faces is not None:
        for face in faces:
            x = int(face[0])
            y = int(face[1])
            x2 = int(face[2])
            y2 = int(face[3])

            if x > 0 and y > 0 and x2 - x > 140 and y2 - y > 140:
                cropped_img = frame[y:y2, x:x2]

                reimage = cv2.resize(cropped_img, (224, 224))
                face_array = np.asarray(reimage)
                face_array = normalization_layer(face_array)
                face_array = np.expand_dims(face_array, axis=0)
                predictions = model.predict(face_array)
                score = tf.nn.softmax(predictions)
                label_guess = labels[np.argmax(score)]  # the label with the highest score
                guess_queue.append(label_guess)
        unique_list = set(guess_queue)
        for elem in unique_list:
            print(guess_queue.count(elem))
            if guess_queue.count(elem) > 4:
                request_parameters = {"emp_ID": elem}
                requests.post(url, params=request_parameters)

    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1280, 720)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()