
## Image augmentation with library albumentations. 
## Adds augmentation of pictures to folder.

from PIL import Image
import albumentations as alb
import matplotlib.pyplot as plt
import os
import numpy as np

## augmentation pipeline. All Changes have a probability of 0.2 (p = 0.2)
transformer = alb.Compose([
    alb.RandomBrightnessContrast(brightness_limit=(-0.3, 0.7), contrast_limit=(-0.3, 0.7), p=0.2), ## brightness and contrast in range (-0.3 and 0.7)
    alb.HorizontalFlip(p=0.2), ## flip picture vertical
    alb.geometric.rotate.Rotate(limit = [-10,10], p = 0.2), ## Rotate 10 degrees left or right
    alb.RandomCrop(height = 50, width = 200, p =0.2), # random crop of face 
    alb.RandomGamma(p=0.2),
    alb.RGBShift(p=0.2), # shifts the RBG

])

def image_auger(directory, number_of_augpics):
  labels = os.listdir(directory)
  for label in labels:
    for image in os.listdir(os.path.join(directory, label)):
      path = os.path.join(directory, label,image)
      file_name = os.path.join(directory, label,image).split('/')[-1]
      i = 0
      for x in range(number_of_augpics):
        image = Image.open(path) ## open image with PIL library
        image = np.array(image) ## we need to make it to an array
        augment_img = transformer(image = image) ## image goes through augmentation pipeline. Returns a dict
        os.chdir(os.path.join(directory,label)) ## Go to the folder
        plt.imsave(f'augmented_{file_name}_{i}.jpg', augment_img['image']) ## Save img using matplotlib.pyplot lib.
        i += 1


directory = 'insert your filepath here'
number_of_augpics = 30
image_auger(directory, number_of_augpics)