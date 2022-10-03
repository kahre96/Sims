import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import pandas as pd
import numpy as np

rv_x = []
rv_y = []
rv_z = []
label = []

user_name = input('What is your name?\n') 


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
    ls_single_face=results.multi_face_landmarks[0].landmark

    for frame in image:
        internal_x = []
        internal_y = []
        internal_z = []
    for landmark in ls_single_face:
        internal_x.append(landmark.x)
        internal_y.append(landmark.y)
        internal_z.append(landmark.z)
    
    label.append(user_name) ##appends label
    ## appends each face landmark x,y,z
    rv_x.append(internal_x) 
    rv_y.append(internal_y)
    rv_z.append(internal_z)


    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      temp_df = pd.DataFrame(label) ## creates a dataframe with only labels
      df_x = pd.DataFrame(rv_x, columns=[f"lm_x_{count}" for count in range(478)]) ## creates a dataframe for each landmark per image
      df_y = pd.DataFrame(rv_y, columns=[f"lm_y_{count}" for count in range(478)])
      df_z = pd.DataFrame(rv_z, columns=[f"lm_z_{count}" for count in range(478)])
      new_df = pd.concat([temp_df,df_x,df_y,df_z],axis = 1) ## concat the labels and landmarks to one dataframe
      new_df.to_csv(f'{user_name}_data.csv', index=False, sep = ";") ## save dataframe
      break
cap.release()