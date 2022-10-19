from keras.optimizers import Adam
from keras.models import Model
import numpy as np
import fnmatch
import os
import tensorflow as tf
import keras
from keras.layers import Dense, Dropout, Flatten
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
import pickle
from keras_vggface import VGGFace
from create_data_aug import CreateDataset
from custom_data_gen import CustomDataGen


class ModelBuilder:

    def __init__(self, path="images_ds", epochs=3000, patience=15, alb_aug=False):
        self.img_height, self.img_width = 224, 224
        self.ds_dir = path
        self.amount_of_classes = self.count_classes()
        self.patience = patience
        self.batch_size = 32
        self.epochs = epochs
        self.model_type = "vgg16"
        self.neurons = [256, 128]
        self.drop_rate = [0.75, 0.5]
        if alb_aug:
            self.train_ds, self.val_ds = self.create_generator()
        else:
            self.train_ds, self.val_ds = self.import_data()
        self.callbacks = self.generate_callback()
        self.model = self.generate_model()

        self.save_labels()
        #self.train_model()

    def count_classes(self):
        count = len(fnmatch.filter(os.listdir(self.ds_dir), '*'))
        print(count)
        return count

    def save_labels(self):
        class_names = sorted(os.listdir(self.ds_dir))
        f = open('labels.pickle', "wb")
        f.write(pickle.dumps(class_names))
        f.close()

    def import_data(self):
        normalization_layer = tf.keras.layers.Rescaling(1. / 255)

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.ds_dir,
            validation_split=0.2,
            labels='inferred',
            label_mode="categorical",
            subset="training",
            seed=1,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,

        )

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.ds_dir,
            labels='inferred',
            validation_split=0.2,
            label_mode="categorical",
            subset="validation",
            seed=1,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,

        )
        train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

        return train_ds,val_ds


    def create_generator(self):
        train_ds, val_ds = CreateDataset(self.ds_dir, cat=True).set_dataset()
        training = CustomDataGen(data=train_ds, batch_size=32, normalization='minmax')
        validation = CustomDataGen(data=val_ds, batch_size=32, normalization='minmax')
        return training,validation



    # creates a base model based on model_types archtitecture and adds toplayer
    # based on neurons,drop and amount of classes
    def generate_model(self):
        base_model = VGGFace(
            model=self.model_type,
            include_top=False,
            input_shape=(self.img_height, self.img_width, 3),
        )
        for layer in base_model.layers:
            layer.trainable = False

        top_model = base_model.output
        top_model = Flatten(name="flatten")(top_model)
        for i in range(len(self.neurons)):
            top_model = Dense(self.neurons[i], activation="relu")(top_model)
            top_model = Dropout(self.drop_rate[i])(top_model)
        top_model = Dense(self.amount_of_classes, activation="softmax")(top_model)

        return Model(inputs=base_model.input, outputs=top_model, name='VGG16')

    def generate_callback(self):
        checkpoint = ModelCheckpoint("models/face_classifier.h5",
                                     monitor="val_loss",
                                     mode="min",
                                     save_best_only=True,
                                     verbose=1)

        # EarlyStopping to find best model with a large number of epochs
        earlystop = EarlyStopping(monitor='val_loss',
                                  restore_best_weights=True,
                                  patience=self.patience,  # number of epochs with
                                  # no improvement after which
                                  # training will be stopped
                                  verbose=1)

        return [checkpoint, earlystop]

    def train_model(self):
        self.model.summary()
        self.model.compile(loss='categorical_crossentropy',  # sparse_categorical_crossentropy
                           optimizer=Adam(learning_rate=0.001),
                           metrics=['accuracy'])
        history = self.model.fit(
            self.train_ds,
            epochs=self.epochs,
            callbacks=self.callbacks,
            validation_data=self.val_ds,
        )
        self.model.save(f"models/classification_model.h5")

        # prints results of best epoch
        best_epochs = np.argmin(history.history['val_loss'])
        print("val_accuracy", history.history['val_accuracy'][best_epochs])
        print("val_loss", history.history['val_loss'][best_epochs])
        print("accuracy", history.history['accuracy'][best_epochs])
        print("loss", history.history['loss'][best_epochs])




