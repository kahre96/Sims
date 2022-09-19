import os
import mtcnn
import numpy  as np
import cv2
import matplotlib.pyplot as plt


## get images and labels from a directory.
def path_process(dir):
  images = []
  labels = []
  for label in os.listdir(dir):
    for image in os.listdir(os.path.join(dir,label)):
      path = os.path.join(dir,label,image)
      label = path.split('/')[-2]
      images.append(path)
      labels.append(label)
  return images, labels


## Call model

face_detector = mtcnn.MTCNN()

## crop images
def cropped_img(image, labels):
    img = cv2.imread(image)
    faces = face_detector.detect_faces(img)
    x, y, width, height, = faces[0]['box']
    cropped_img = img[y:y+height,x:x+width]
    return cropped_img,labels

## save images to new folder.
def save_images(data):
  i = 0 ## counter
  for image, label in data:
    dir = (f'/DatasetCrop/{label}')
    os.chdir(dir)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'img{i}_{label}.jpg',image)
    i += 1
  

## calls 

images, labels = path_process('/Dataset/')
cropped = list(map(cropped_img, images, labels))
save_images(cropped)