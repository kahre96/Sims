import os
import mtcnn
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


detector = mtcnn.MTCNN()

dirs = "D:/dokument/skolskit/SIMS/faces-spring-2020/"
save_dir = "D:/dokument/skolskit/SIMS/glasses_ds"

for picture in os.listdir(dirs):
    img = cv2.imread(f"{dirs}{picture}", cv2.IMREAD_UNCHANGED)
    face = detector.detect_faces(img)
    if face:
        x, y, width, height, = face[0]['box']
        cropped_img = img[y:y + height, x:x + width]
        reimage = cv2.resize(cropped_img, (224,224))
        #image = Image.fromarray(cropped_img)
        #image2 = image.resize(size=(224, 224))
        #face_array = np.asarray(image2)
        cv2.imwrite(f"{save_dir}/{picture}.jpg", reimage)
