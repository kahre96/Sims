import tensorflow as tf
from tensorflow import keras
import numpy as np
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import pickle
import collections as col
import time

class multimedia():

    def __init__(self, labels, model,video_source):
        self.labels = pickle.loads(open(labels, "rb").read())
        self.model = keras.models.load_model(model)
        self.mtcnn = MTCNN()
        self.cam = cv2.VideoCapture(video_source)
        self.cam.set(3, 3840)
        self.cam.set(4, 2160)
        self.guess_array = col.deque(maxlen=20)
        self.guessed = []

    def video(self):
        while True:
            check, frame = self.cam.read()
            faces, _ = self.mtcnn.detect(frame)
            if not check:
                print("No frame, exiting...")
                break
           
            if faces is not None:
                for face in faces:
                    x = int(face[0])
                    y = int(face[1])
                    x2 = int(face[2])
                    y2 = int(face[3])

                    if x > 0 and y>0 and x2-x > 120 and y2-y > 120:
                        face_crop = frame[y:y2, x:x2]
                        image = self.img_hndlr(face_crop)
                        image_pred = self.predictions(image)
                    cv2.rectangle(frame,(x, y),(x2, y2), (0, 255, 0), 2) 
                    cv2.putText(frame, image_pred, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv2.namedWindow('video', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('video', 1280,720)
            cv2.imshow('video', frame)

            key = cv2.waitKey(1)
            if key == 27:
                break
    def img_hndlr(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        img_array = np.array(image)
        img_array = self.minmaxnorm(img_array)
        img_array = np.expand_dims(img_array, axis = 0)
        return img_array

    def quecheck(self, label):
        self.guess_array.append(label)
        self.check_logged_in_len()
        for elem in self.guess_array:
            if self.guess_array.count(elem) > 5:
                self.dbcaller(elem)
                
    def dbcaller(self,elem):
        if elem in self.guessed:
            pass
        else:
            if elem == 'Guest':
                print('Make db call guest')
                return
            else:
                self.guessed.append(elem)
                print(self.guessed)
                print('make db call')
                return
    def check_logged_in_len(self):
        if len(self.guessed) == 2 and self.get_time() == '18:58:00':
            print('EVERYTHING IS CLEARED')
            self.guess_array.clear()
            self.guessed.clear()
        else:
            pass
    def minmaxnorm(self,x):
        return((x-x.min())/(x.max()-x.min()))
    
    def get_time(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time

    def predictions(self,image):
        pred = self.model(image)
        score = tf.nn.softmax(pred)
        label_guess = str(self.labels[np.argmax(score)])
        self.quecheck(label_guess)
        return label_guess 

    

show = multimedia(labels = 'models/labels.pickle', model = 'models/128x64_GnG_BN.h5', video_source = 1).video()






