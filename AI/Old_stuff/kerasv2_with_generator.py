import os
import random
from PIL import Image
import albumentations as alb
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Convolution2D as Conv2D
from keras.layers import MaxPool2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.optimizers import Adam



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


"""
Image augmentation using albumentations. This will create a augmentation pipeline.
"""
transformer = alb.Compose([
    alb.RandomBrightnessContrast(brightness_limit=(-0.4,0.4), contrast_limit=(-0.4,0.4), p=0.3), ## brightness and contrast in range (-0.3 and 0.7)
    alb.HorizontalFlip(p=0.25), ## flip picture vertical
    alb.geometric.rotate.Rotate(limit = [-5,5], p = 0.3), ## Rotate 10 degrees left or right 
    alb.RandomGamma(p=0.2)
])


def img_aug(image,label):
    augmented_images = []
    augmented_labels = []
    for y,t in enumerate(image):
        for i in range(30):
            image = np.array(t)
            augment_img = transformer(image = image) ## image goes through augmentation pipeline. Returns a dict
            augmented_images.append(augment_img['image'])
            augmented_labels.append(label[y])
    return augmented_images,augmented_labels



class CustomDataGen(tf.keras.utils.Sequence):
    """
    This generator is created based on tf.keras.utils.Sequence. The condition from keras API is that
    __init__, on_epoch_end, __getitem__ and __len__ needs to be defined. 

    When we increase ppl in the dataset, we will go OOM on RAM. 
    This generator will therefore be optimal to use when we have large amount of pictures.

    """
    
    def __init__(self, X, y, batch_size, shuffle = True):
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.n = len(self.X)
        self.indices = list(range(0, len(self.X)))
        self.shuffle = shuffle
    def on_epoch_end(self):
        print("epoch done")
        self.index = np.arange(len(self.indices))
        if self.shuffle == True:
            np.random.shuffle(self.index)

    def __get_data(self, index):
        """
        This will generate image augmentations per batch.
        """
        data_gen = img_aug(self.X[index*self.batch_size:(index+1)*self.batch_size],self.y[index*self.batch_size:(index+1)*self.batch_size])
        X = list(self.X)
        y = list(self.y)
        X.extend(data_gen[0])
        y.extend(data_gen[1])
        X = np.array(X)
        y = np.array(y)
        return X,y

    def __getitem__(self, index): 
        """
        __getitem__ will get the X,y data from calling __get_data and then convert to tensors.
        This will then be forwarded to the model.
        """
        X,y = self.__get_data(index)
        X = tf.convert_to_tensor(X)
        y = tf.convert_to_tensor(y)
        return X,y
    def __len__(self):
        return self.n // self.batch_size



dir = '../content/images/'  ## define the directory where the pictures are stored.
class_names = os.listdir(dir) ## returns a list of the label names. This will be used later when creating the sequential model.


new_dataset = dataset(dir,train_size = 0.7, test_size = 0.1, val_size = 0.2) ## creating a new dataset. Set train, test and val size.
train,val,test = new_dataset.train_test_val() ## calling the method inside class dataset to get the train,val and test datasets.

"""
Unzipping the train val test into x-train, y-train and so on.
"""
x_train, y_train = zip(*train)
x_val, y_val = zip(*val)
x_test, y_test = zip(*test)


"""
Create training and validation datasets using the generator, choose batch_size. 
"""


training = CustomDataGen(X = x_train, y = y_train, batch_size = 32)
validation = CustomDataGen(X = x_val, y = y_val, batch_size = 32)



"""
Create the sequential model.

This mode will have 21.170.626 total params and trainable params.
This sequential is based of VGG.

We could be adding a dropout per Conv2D layer. 
"""


model = Sequential()
model.add(Conv2D(input_shape=(224,224,3),filters=64,kernel_size=(3,3),padding="same", activation="relu"))
model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
## hidden and output
model.add(Flatten())
model.add(Dense(units=256,activation="relu"))
model.add(Dense(units=128,activation="relu"))
model.add(Dense(units= len(class_names), activation="softmax"))



## checkpoint will be created based on accuracy.
from keras.callbacks import ModelCheckpoint
checkpoint = ModelCheckpoint("Re-created1_vgg16_1.h5", monitor='accuracy', verbose=1, save_best_only=True, save_weights_only=False, mode='auto')

"""
im not adding any earlystopping right now due to that
keras earlystopping only allows you to stop the model based on 1 metric.
im currently developing a custom callback for earlystopping that will take both
accuracy and val_accuracy into account before stopping the model.

"""

## start the training. Choose the epochs.
model.fit(training,
          validation_data=validation,
          epochs=50, callbacks = [checkpoint])
