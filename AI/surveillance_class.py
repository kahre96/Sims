import tensorflow as tf
from tensorflow import keras
import numpy as np
from facenet_pytorch import MTCNN
import cv2
import pickle
import collections as col
import requests
import time


class surveillance():

    def __init__(self, labels, model, video_source):
        self.labels = pickle.loads(open(labels, "rb").read())
        self.model = keras.models.load_model(model)
        self.detector = MTCNN()
        self.cam = cv2.VideoCapture(video_source)
        self.cam.set(3, 3840)
        self.cam.set(4, 2160)
        self.guess_queue = col.deque(maxlen=20)
        self.already_detected = []
        self.norm_layer = tf.keras.layers.Rescaling(1./255)
        self.frame = None
        self.url = "http://localhost:5000/player/newEntry"
        self.color = (0, 255, 0)
        self.counter= 0
        self.surveillance()

    def surveillance(self):
        while True:
            check, self.frame = self.cam.read()
            if not check:
                print("Cant recive a frame from camera. exiting...")
                break

            faces, probability = self.detector.detect(self.frame)

            if faces is not None:

                for face in faces:
                    if any(cord < 0 for cord in face):
                        break

                    x, y, x2, y2 = face.astype(int)
                    if x2 - x < 180:
                        break
                    if y2 - y < 180:
                        break

                    face_array = self.image_processing(x,y,x2,y2)
                    label_guess = self.predict(face_array)
                    self.draw_face(x,y,x2,y2, label_guess)
                self.post_handler()

            self.check_time_for_reset()
            self.counter += 1
            if self.counter > 20:
                self.reset_guest_lock()
                self.counter = 0 

            cv2.namedWindow('video', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('video', 1280, 720)
            cv2.imshow('video', self.frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

    def image_processing(self, x, y, x2, y2):

        cropped_img = self.frame[y:y2, x:x2]
        reimage = cv2.resize(cropped_img, (224, 224))
        face_array = np.asarray(reimage)
        face_array = self.norm_layer(face_array)
        face_array = np.expand_dims(face_array, axis=0)
        return face_array

    def predict(self, face_array):
        predictions = self.model.predict(face_array)
        score = tf.nn.softmax(predictions)
        label_guess = self.labels[np.argmax(score)]  # the label with the highest score
        if label_guess in self.already_detected:
            pass
        self.guess_queue.append(label_guess)
        return label_guess

    def post_handler(self):
        unique_list = set(self.guess_queue)
        for elem in unique_list:
            if elem in self.already_detected:
                print("already detected")
                continue
            if self.guess_queue.count(elem) > 4:
                self.already_detected.append(elem)
                print(f"{elem} post")
                #request_parameters = {"emp_ID": elem}
                #requests.post(self.url, params=request_parameters)

    def draw_face(self,x,y,x2,y2, label_guess):
        cv2.rectangle(self.frame, (x, y), (x2, y2), self.color, 2)
        cv2.putText(self.frame, label_guess, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.color, 2)

    def check_time_for_reset(self):
        now = time.localtime()
        nowstr = time.strftime("%H:%M:%S", now)
        if nowstr == "23:00:00":
            self.guess_queue.clear()
            self.already_detected.clear()


    def reset_guest_lock(self):
        for elem in self.already_detected:
            if elem == "Guest":
                self.already_detected.remove(elem)
                self.guess_queue.clear()
                print('Cleared guess que unlocking guest')
                


surveillance(labels='models/labels.pickle', model='models/128x64_GnG_BN.h5', video_source=2)










