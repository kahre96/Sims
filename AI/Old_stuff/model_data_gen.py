import os
import numpy as np
import random
import tensorflow as tf
import pandas as pd
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from PIL import Image
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
import albumentations as alb
import matplotlib.pyplot as plt
import pickle


class createDataset():
    
    def __init__(self, directory, cat = False):
        
        """
        This will return the paths to each image. 
        if cat = False it will return labels as integers(label encoding). Default = False 
        if cat = True it will return each label as one hot encoding
        
        !!IMPORTANT!!
        If cat = False: set model.compile as sparse categorical crossentropy.
        if cat = True:  set model.compile as categorical crossentropy
        
        """
        self.directory = directory
        self.cat = cat
        self.paths = []
        self.labels =[]
        self.class_names = sorted(os.listdir(self.directory))
    
    def setDataset(self):
        class_names = self.class_names # this will save the labels for the model
        f = open('../labels.pickle', "wb")
        f.write(pickle.dumps(class_names))
        f.close()        
        i = 0
        if self.cat == False:
            class_number = np.unique(self.class_names, return_inverse=True)[1] # label encoding
        else:
            class_number = np.array(pd.get_dummies(self.class_names).T) # one hot 
        for labels in self.class_names:   
            i+=1
            for img in os.listdir(os.path.join(self.directory,labels)):
                self.paths.append(os.path.join(self.directory,labels,img))
                self.labels.append(class_number[i-1])

        dataset = list(zip(self.paths,self.labels))
        data = random.sample(dataset, len(dataset))
        indexes = int(len(data) - 1)
        train_ds = data[:int(indexes * 0.7)]
        val_ds = data[len(train_ds):indexes]
        return train_ds, val_ds




# train and val split. Shuffles the list.

def train_val_split(data, trainsize):
    data = random.sample(data, len(data))
    indexes = int(len(data)-1)
    train_ds = data[:int(indexes*trainsize)]
    val_ds = data[len(train_ds):indexes]
    return train_ds, val_ds



# model class

class model():
    def __init__(self, num_classes, loss, base_model, learning_rate, neuron1, neuron2):
        self.num_classes = num_classes
        if loss == 'Cat':
            self.loss = tf.keras.losses.CategoricalCrossentropy()
        else:
            self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        self.base_model = base_model
        self.learning_rate = learning_rate
        self.neuron1 = neuron1
        self.neuron2 = neuron2
    
    def layers(self):
        for layer in self.base_model.layers:
            layer.trainable = False
        
    def model(self, Layers = True):
        if Layers == True:
            self.layers()
        add_model = self.base_model.output
        add_model = Flatten(name = "flatten")(add_model)
        add_model = Dense(self.neuron1, activation = "relu")(add_model)
        add_model = Dropout(0.2)(add_model)
        add_model = Dense(self.neuron2, activation = "relu")(add_model)
        add_model = Dropout(0.2)(add_model)
        add_model = Dense(self.num_classes, activation = "softmax")(add_model)
        
        newModel = Model(inputs=self.base_model.input, outputs=add_model)
        newModel.compile(loss=self.loss,optimizer=Adam(self.learning_rate),metrics=['accuracy'])
        print(newModel.summary())
        return newModel




# albumentation pipeline

transformer1 = alb.Compose([
    alb.RandomBrightnessContrast(brightness_limit=(-0.35, 0.35), contrast_limit=(-0.35, 0.35), p=0.3),
    # brightness and contrast in range (-0.3 and 0.7)
    alb.HorizontalFlip(p=0.3),  # flip picture vertical
    alb.geometric.rotate.Rotate(limit=[-5, 5], p=0.3),  # Rotate 10 degrees left or right
    alb.RandomGamma(p=0.3)
])




# Data generator


class CustomDataGen(tf.keras.utils.Sequence):
    """

    When we increase ppl in the dataset, we will go OOM on RAM. 
    This generator will therefore be optimal to use when we have large amount of pictures.

    """
    
    def __init__(self, normalization,data, batch_size, shuffle = True, transformer=transformer1):
        self.data = random.sample(data, len(data)) # shuffles the list again
        self.batch_size = batch_size
        self.n = int(len(self.data))
        self.indices = list(range(0, len(self.data)))
        self.shuffle = shuffle
        self.transformer = transformer
        self.normalization = normalization
        if self.normalization == 'minmax':
            print('Using min-max-normalization')
        else:
            print('Using mean std normalization')
        self.on_epoch_end()
    def on_epoch_end(self):
        self.index = np.arange(len(self.indices))
        if self.shuffle == True:
            np.random.shuffle(self.index)
    def __get_data(self, start_index,end_index):
        """
        This will generate image augmentations per batch.
        """
        data = self.data[start_index:end_index]
        data_x,data_y = list(zip(*data))
        X = []
        for item in data_x:
            image = Image.open(item)
            image = np.array(image)
            image = self.img_aug(image)
            if self.normalization == 'minmax':
                image = self.minmaxnorm(image) # min-max-normalization
            else:
                image = self.znorm(image) # mean std normalization
            X.append(image)
        return X,data_y
    
    def minmaxnorm(self,x):
        return((x-x.min())/(x.max()-x.min()))
    
    def znorm(self,x):
        return(x - x.mean(axis=(0,1,2), keepdims=True)) / x.std(axis=(0,1,2), keepdims=True)
    
    def img_aug(self,x):
        augment_img = self.transformer(image=x)
        return augment_img['image']
    
    def __getitem__(self, index): 
        """
        __getitem__ will get the X,y data from calling __get_data and then convert to tensors.
        This will then be forwarded to the model.
        """
        start_index = int(index*self.batch_size)
        end_index = int((index+1)*self.batch_size)
        X,y = self.__get_data(start_index,end_index)
        X = tf.convert_to_tensor(np.array(X))
        y = tf.convert_to_tensor(np.array(y), dtype = tf.uint8)
        return X,y
    def __len__(self):
        return self.n // self.batch_size



# get base model(VGG16)
base_model= tf.keras.applications.VGG16(include_top=False,weights='imagenet',input_shape=(224, 224, 3))

# create the new model. Calls the model class. Set learning rate, loss function ('Sparse' if using label encoding, 'Cat' if using one hot)
# the model is created with two dense layers. Define the number of neurons(neuron1 and neuron2)
newModel = model(num_classes = 6, loss = 'Sparse', base_model = base_model, learning_rate = 0.001, neuron1 = 32, neuron2 = 32).model()

# create the dataset
# set the directory for images
# set cat = False for label encoding, set cat = True for one hot. Remember to change loss accordingly to the created dataset.
directory = 'PATH HERE'
dataset = createDataset(directory, cat = False).setDataset()

# get the train and val dataset
# set the train size
train,val= train_val_split(dataset, 0.7)


# create the generators for training and validation data
# set normalization to 'znorm' for mean std normalization.
# set normalization to 'minmax' for min max normalization
# each normalization is done per image and not per batch.
training = CustomDataGen(data = train, batch_size =32,normalization = 'minmax',transformer = transformer1)
validation = CustomDataGen(data = val, batch_size =32,normalization = 'minmax',transformer = transformer1)


# model.fit
# set epochs and patience for the callbacks
epochs = 200
patience = 20
# callbacks from keras
checkpoint = ModelCheckpoint("/notebooks/test/face_classifier_1006_test.h5",
                             monitor="val_loss",
                             mode="min",
                             save_best_only=True,
                             verbose=1)

# EarlyStopping to find best model with a large number of epochs
earlystop = EarlyStopping(monitor='val_loss',
                          restore_best_weights=True,
                          patience=patience,  # number of epochs with
                          # no improvement after which
                          # training will be stopped
                          verbose=1)

callbacks = [earlystop, checkpoint]

history = newModel.fit(training,epochs=epochs,callbacks=callbacks,validation_data=validation)





### PLOTTS.
# this will plot the accuracy and val_accuracy in one plot and loss and val_loss in another (this can be good for the report)


fig, axs = plt.subplots(2, 1,figsize=(30,20))
t1 = history.history['accuracy']
t2 = history.history['val_accuracy']
s1 = history.history['loss']
s2 = history.history['val_loss']

axs[0].plot(t1)
axs[0].plot(t2)
axs[0].set_xlabel('epochs')
axs[0].set_ylabel('accuracy and val_accuracy')
axs[0].grid(True)
axs[1].plot(s1)
axs[1].plot(s2)
axs[1].set_xlabel('epochs')
axs[1].set_ylabel('loss and val_loss')
axs[1].grid(True)
plt.show()