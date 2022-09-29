import tensorflow as tf
from tensorflow import keras
import numpy as np
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt
import cv2
from PIL import Image

#tf.config.set_visible_devices([], 'GPU')
cam = cv2.VideoCapture(0)
detector = MTCNN()

model = keras.models.load_model('models/EffNV2M_aug.h5')
normalization_layer = tf.keras.layers.Rescaling(1./255)
labels = ['Andreas', 'Fredrik', 'Glenn', 'Ina', 'Nordin', 'Peter']
while True:
    check, frame = cam.read()

    if not check:
        print("Cant recive a frame from camera. exiting...")
        break

    #faces store one array for each face
    faces, probability = detector.detect(frame)

    #make sure a face is detected in the frame
    if faces is not None:

        for face in faces:

            #covert it into a list to access variables
            faceList = face.tolist()

            #cordinates for box around a face
            x, y, x2, y2 = faceList
            x = int(x)
            y = int(y)
            x2 = int(x2)
            y2 = int(y2)

            #crop the image for a prediction
            if(x>0 and y>0):
                cropped_img = frame[y:y2, x:x2]
                cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                image_predict = Image.fromarray(cropped_img, mode ="RGB")
                image_predict = image_predict.resize(size = (224,224))
                face_array = np.asarray(image_predict)
                face_array = normalization_layer(face_array)
                face_array = np.expand_dims(face_array, axis = 0)
                predictions = model.predict(face_array)
                score = tf.nn.softmax(predictions)
                print("pred", predictions)
                print(score)
                knas = str(labels[np.argmax(score)])
                print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(labels[np.argmax(score)], 100 * np.max(score)))

                #draw a rectangle around the face and write predicted name above
                cv2.rectangle(frame,
                              (x, y), # start_point
                              (x2, y2), # end_point
                              (255, 0, 0),  # color in BGR
                              2) # thickness in px
                cv2.putText(frame, knas,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)



    cv2.imshow('video', frame)


    #allows to exit the program by pressing ESC
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
