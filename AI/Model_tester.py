import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import mtcnn
import os

## this file just works as a model tester to evaluate the accuracy per trained model.
## import the h5 file from the trained model

model = tf.keras.models.load_model("models/face_classifier.h5")

normalization_layer = tf.keras.layers.Rescaling(1./255)

dir = 'insert path here'
labels = []
for label in os.listdir(dir):
    labels.append(label)
labels.sort()


img = plt.imread('insert file path')
face_detector = mtcnn.MTCNN()
image_predict = face_detector.detect_faces(img)

x, y, width, height, = image_predict[0]['box']
cropped_img = img[y:y+height,x:x+width]

image_predict = Image.fromarray(cropped_img)
image_predict = image_predict.resize(size = (200,200))
face_array = np.asarray(image_predict)
face_array = normalization_layer(face_array)
face_array = np.expand_dims(face_array, axis = 0)

predictions = model.predict(face_array)

print(predictions)
score = tf.nn.softmax(predictions)
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(labels[np.argmax(score)], 100 * np.max(score))
)

