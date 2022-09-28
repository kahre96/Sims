import os
import random
from PIL import Image
import albumentations as alb
import matplotlib.pyplot as plt
import os
import numpy as np
import tensorflow as tf


class dataset():

    def __init__(self,directory, train_size, test_size,val_size):
        self.directory = directory
        self.train = train_size
        self.test = test_size
        self.val = val_size

    def dataset_shuffle(self):
        labels = os.listdir(self.directory)
        print(labels)
        imagelist = []
        for label in labels:
            for item in os.listdir(os.path.join(self.directory,label)):
                imagelist.append([os.path.join(self.directory,label,item), labels.index(label)])
    
        imagelist = random.sample(imagelist, len(imagelist))  ## shufflar listan
        return imagelist

    def dataset_created(self):
        dataset_tp = self.dataset_shuffle()
        image, label = zip(*dataset_tp)
        dataset_ds = list(map(self.img_open,image,label))
        return dataset_ds
      
    def img_open(self,image,label):
        imag = Image.open(image) ## open image with PIL library
        imag = np.array(imag, dtype = np.float32)/255 ## array -> /255.
        return imag,label


    def train_test_val(self):
        array_list = self.dataset_created()

        train_length = int(len(array_list)*self.train)
        test_length = int(len(array_list)*self.test)
        val_length = int(len(array_list)*self.val)
        train_data = array_list[0:train_length]
        val_data = array_list[train_length:(train_length + val_length)]
        test_data = array_list[(train_length + val_length):]

        return train_data, val_data,test_data


transformer = alb.Compose([
    alb.RandomBrightnessContrast(brightness_limit=(-0.4,0.4), contrast_limit=(-0.4,0.4), p=0.4), ## brightness and contrast in range (-0.3 and 0.7)
    alb.HorizontalFlip(p=0.4), ## flip picture vertical
    alb.geometric.rotate.Rotate(limit = [-5,5], p = 0.4), ## Rotate 10 degrees left or right
    alb.RandomGamma(p=0.2)
])


def img_aug(image,label):
  #imag = Image.open(image) ## open image with PIL library
  #imag = np.array(imag) ## we need to make it to an array
    augmented_images = []
    augmented_labels = []
    for y,t in enumerate(image):
        for i in range(2):
            image = np.array(t)
            augment_img = transformer(image = image) ## image goes through augmentation pipeline. Returns a dict
            augmented_images.append(augment_img['image'])
            augmented_labels.append(label[y])
    return augmented_images,augmented_labels


def kv2(bs):

    ## directory where files is located
    dir = 'cropped_dataset'

    temp_dataset = dataset(dir,train_size = 0.7, test_size = 0.1, val_size = 0.2)
    created_dataset = temp_dataset.train_test_val()

    train,val,test = created_dataset

    x_train, y_train = zip(*train)
    x_val, y_val = zip(*val)
    x_test, y_test = zip(*test)

    x_train = list(x_train)
    x_val = list(x_val)
    x_test = list(x_test)
    y_train = list(y_train)
    y_val = list(y_val)
    y_test = list(y_test)



    aug_train = img_aug(x_train,y_train)
    print(aug_train)
    aug_val = img_aug(x_val,y_val)
    print(aug_val)
    aug_test = img_aug(x_test,y_test)
    print(aug_test)
    ## extend training, val and test dataset with the augmentated images
    ## train
    x_train.extend(aug_train[0])
    y_train.extend(aug_train[1])
    ## val
    x_val.extend(aug_val[0])
    y_val.extend(aug_val[1])
    ## test
    x_test.extend(aug_test[0])
    y_test.extend(aug_test[1])


    ## create the tensor dataset #keras V2 ;)
    ## training
    x_train = tf.convert_to_tensor(x_train)
    y_train = tf.convert_to_tensor(y_train)

    ##val
    x_val = tf.convert_to_tensor(x_val)
    y_val = tf.convert_to_tensor(y_val)

    ##test
    x_test = tf.convert_to_tensor(x_test)
    y_test = tf.convert_to_tensor(y_test)

    ## Make tensor slices. This step is done to create batches.

    #train
    x_train_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(x_train)
    y_train_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(y_train)

    #val
    x_val_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(x_val)
    y_val_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(y_val)

    #test
    x_test_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(x_test)
    y_test_to_tensor_dataset = tf.data.Dataset.from_tensor_slices(y_test)

    ## create the final tensor dataset

    train_ds = tf.data.Dataset.zip((x_train_to_tensor_dataset, y_train_to_tensor_dataset))
    val_ds = tf.data.Dataset.zip((x_val_to_tensor_dataset, y_val_to_tensor_dataset))
    test_ds = tf.data.Dataset.zip((x_test_to_tensor_dataset, y_test_to_tensor_dataset))


    ## create batches

    train_ds_batch = train_ds.batch(bs)
    val_ds_batch = val_ds.batch(bs)
    test_ds_batch = test_ds.batch(bs)

    return train_ds_batch,val_ds_batch,test_ds_batch













