import os
import mtcnn
import numpy  as np
import matplotlib.pyplot as plt
from PIL import Image


## get images and labels from a directory.
def path_process(dir):
  images = []
  labels = []
  for label in os.listdir(dir):
    for image in os.listdir(os.path.join(dir,label)):
      path = os.path.join(dir,label,image)
      label = path.split('\\')[-2]
      images.append(path)
      labels.append(label)
  return images, labels


## Call model
face_detector = mtcnn.MTCNN()

## crop images
def cropped_img(image,labels):
  # using plt instead
  img = plt.imread(image)
  faces = face_detector.detect_faces(img)
  ## this checks if the len of faces is > 0 and then make the calculation of where the face is. Returns the array of face and label.
  if len(faces) != 0:
    x, y, width, height, = faces[0]['box']
    cropped_img = img[y:y+height,x:x+width]
    image = Image.fromarray(cropped_img)
    ## We could add a size argument to the function instead. 
    image = image.resize(size = (224,224))
    face_array = np.asarray(image)
    return face_array, labels
  ## if the len of faces is 0. The MTCNN has not detected a face and therefore we return None. 
  else:
    return None




## save images to new folder.
## because we return None, we need to skip that when adding to new data. 
def save_images(data,directory):
   i = 0 ## counter
   for item in data:
      if item is not None:
        dir = (f'{directory}\{item[1]}')
        os.chdir(dir)

        plt.imsave(f'img{i}_{item[1]}.jpg',item[0])
        i += 1
      else:
        pass
  

## calls 

images, labels = path_process('Dataset')  # chose directory to get images
directory = "D:\dokument\skolskit\SIMS\Code\Sims\AI\content\images" # chose directory to save images
cropped = list(map(cropped_img, images, labels))
save_images(cropped, directory)

