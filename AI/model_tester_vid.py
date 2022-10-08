import tensorflow as tf
from tensorflow import keras
import numpy as np
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import pickle

#tf.config.set_visible_devices([], 'GPU')
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

# setting up the camera input
cam = cv2.VideoCapture(0)
cam.set(3, 3840)
cam.set(4, 2160)

takepics = False  # decide if you want to take pics or not
correct_label = "Fredrik"
color = (0, 255, 0)
namecolor = (36, 255, 12)
labels = pickle.loads(open('labels.pickle', "rb").read()) ## load the pickle file with labels
model = keras.models.load_model('models/noaug_N256x256.h5')

model.summary()

detector = MTCNN() #model to detect faces
if takepics:
    counter = 0  # counter for saving images with diffrent names,

normalization_layer = tf.keras.layers.Rescaling(1./255)
while True:
    check, frame = cam.read()
    if not check:
        print("Cant recive a frame from camera. exiting...")
        break

    # faces store one array for each face
    faces, probability = detector.detect(frame)

    # make sure a face is detected in the frame
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

            # crop the image for a prediction
            if x > 0 and y > 0 and x2-x > 80 and y2-y > 80:
                cropped_img = frame[y:y2, x:x2]
                print("cropped img", cropped_img.shape)
                cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                image_predict = Image.fromarray(cropped_img, mode="RGB")
                image_predict = image_predict.resize(size=(224, 224))
                face_array1 = np.asarray(image_predict)
                face_array = normalization_layer(face_array1)
                face_array = np.expand_dims(face_array, axis=0)
                predictions = model.predict(face_array)
                score = tf.nn.softmax(predictions)
                print("pred", predictions)
                print(score)
                labelguess = str(labels[np.argmax(score)]) #the label with the highest score
                print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(labels[np.argmax(score)], 100 * np.max(score)))

                #draw a rectangle around the face and write predicted name above
                cv2.rectangle(frame,
                              (x, y),  # start_point
                              (x2, y2),  # end_point
                              color,  # color in BGR
                              2)  # thickness in px
                cv2.putText(frame, labelguess,(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, namecolor, 2)
                if takepics == True and correct_label != labelguess:
                    plt.imssave(f"wrong_class_img/{correct_label}/{labelguess}_{counter}.jpg", face_array1)
                    counter += 1


    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1280,720)
    cv2.imshow('video', frame)



    #allows to exit the program by pressing ESC
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
