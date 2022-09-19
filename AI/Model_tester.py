import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model("models/face_classifier.h5")

pic = cv2.imread("Dataset/WIN_20220919_11_47_35_Pro.jpg")

pic = cv2.resize(pic,(720,1280));
pic = np.expand_dims(pic, axis=0)
print(pic.shape)
predictions = model.predict(pic)
print(predictions)
#score = tf.nn.softmax(predictions)
#print(score)
