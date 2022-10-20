import os
from facenet_pytorch import MTCNN
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


detector = MTCNN()

dirs = "D:/dokument/skolskit/SIMS/Code/Sims/AI/images_ds/12"
save_dir = "D:/dokument/skolskit/SIMS/Code/Sims/AI/Images/12"

for picture in os.listdir(dirs):
    img = cv2.imread(f"{dirs}/{picture}", cv2.IMREAD_UNCHANGED)

    faces, probability = detector.detect(img)

    if faces is not None:
        for face in faces:
            x, y, x2, y2 = face.astype(int)
            cropped_img = img[y:y2, x:x2]

            reimage = cv2.resize(cropped_img, (224, 224))
            #image = Image.fromarray(cropped_img)
            #image2 = image.resize(size=(224, 224))
            #face_array = np.asarray(image2)
            cv2.imwrite(f"{save_dir}/{picture}", reimage)
