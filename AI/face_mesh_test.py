import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras

labels = ['Andreas', 'Fredrik', 'Lovisa', 'Mattias']
model = keras.models.load_model('AI/models/face_marks_test2_NN.h5')
cap = cv2.VideoCapture(2)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      ls_single_face=results.multi_face_landmarks[0].landmark
    #if ls_single_face is not None:
      array_x = []
      array_y = []
      array_z = []
      for landmark in ls_single_face:
            #array_mesh = np.concatenate((landmark.x,landmark.y,landmark.z))
          array_x.append(landmark.x)
          array_y.append(landmark.y)
          array_z.append(landmark.z)
        #model.predict([landmark.x,landmark.y,landmark.z])
      array_mesh = np.concatenate((array_x,array_y,array_z))
      array_mesh = np.expand_dims(array_mesh, axis = 0)
      predictions = model.predict(array_mesh)
      score = tf.nn.softmax(predictions)
      print("pred", predictions)
      print(score)
        #labelguess = str(labels[np.argmax(score)])
        #print(labelguess)
      print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(labels[np.argmax(score)], 100 * np.max(score)))


    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()