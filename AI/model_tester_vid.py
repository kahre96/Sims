import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import cv2
from mtcnn import MTCNN
from PIL import Image


cam = cv2.VideoCapture(0)
detector = MTCNN()

model = keras.models.load_model('test2.h5')
normalization_layer = tf.keras.layers.Rescaling(1./255)
labels = ['Andreas', 'Fredrik', 'Nordin', 'Peter']
while True:
    check, frame = cam.read()
    
    face = detector.detect_faces(frame)
    if len(face) != 0:
        x, y, width, height, = face[0]['box']
        cropped_img = frame[y:y+height,x:x+width]
        cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        image_predict = Image.fromarray(cropped_img, mode ="RGB")
        image_predict = image_predict.resize(size = (200,200))
        face_array = np.asarray(image_predict)
        face_array = normalization_layer(face_array)
        face_array = np.expand_dims(face_array, axis = 0)
        predictions = model.predict(face_array)
        score = tf.nn.softmax(predictions)
        print("pred", predictions)
        print(score)
        knas = str(labels[np.argmax(score)])
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(labels[np.argmax(score)], 100 * np.max(score)))

        cv2.rectangle(frame, 
                      (x, y), # start_point
                      (x+width, y+height), # end_point
                      (255, 0, 0),  # color in BGR
                      2) # thickness in px
        cv2.putText(frame, knas,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        

    
    
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
