import tensorflow as tf
import keras
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
import numpy as np


# creates top layers to add on top of the vgg base model
def topModel(prev_model, num_classes, neurons, ddlayer):

    top_model = prev_model.output
    top_model = Flatten(name="flatten")(top_model)
    top_model = Dense(neurons, activation="relu")(top_model)
    top_model = Dropout(0.1)(top_model)
    if ddlayer:
        top_model = Dense(neurons, activation="relu")(top_model)
        top_model = Dropout(0.1)(top_model)
    top_model = Dense(num_classes, activation="softmax")(top_model)

    return top_model


# imports the data used to train the model
def import_data(aug, ds_dir, img_height, img_width, batch_size):
    train_ds = val_ds = None
    if aug == "noaug":
        print("Training model without augmentation")
        normalization_layer = tf.keras.layers.Rescaling(1. / 255)

        # importing data
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            ds_dir,
            validation_split=0.2,
            labels='inferred',
            label_mode="categorical",
            subset="training",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size,

        )

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            ds_dir,
            labels='inferred',
            validation_split=0.2,
            label_mode="categorical",
            subset="validation",
            seed=1,
            image_size=(img_height, img_width),
            batch_size=batch_size,

        )

        # test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        #     ds_dir + "/test",
        #     #validation_split=0.2,
        #     label_mode="categorical",
        #     #subset="testing",
        #     seed=1,
        #     image_size=(img_height, img_width),
        #     batch_size=batch_size,
        #
        # )
        train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
        # test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))

    elif aug == 'kaug':
        print("Training with augmented dataset")
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1 / 255,  # normalizations
            #featurewise_center=True,
            #featurewise_std_normalization=True,
            rotation_range=5,
            width_shift_range=0.1,
            height_shift_range=0.1,
            brightness_range=(-0.2, 0.2),
            horizontal_flip=True,
            validation_split=0.2)

        train_ds = datagen.flow_from_directory(
            ds_dir,
            seed=1,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            subset="training",
            class_mode='categorical')  # categorical data so categorical crossentropy can be used
        val_ds = datagen.flow_from_directory(
            ds_dir,
            seed=1,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            subset="validation",
            class_mode='categorical')

    else:
        print("incorrect augmentaiton input")
    return train_ds, val_ds


# creates a model using the pretrained base VGG16
def create_basemodel(img_height, img_width):

    base_model = tf.keras.applications.vgg16.VGG16(
        include_top=False,
        weights='imagenet',
        input_shape=(img_height, img_width, 3),
    )
    # Set layers to non-trainable
    for layer in base_model.layers:
        layer.trainable = False

    return base_model


# loads a model saved in a h5 file
def load_model(tl_model):
    print(f"Transfer learning on {tl_model}")
    return keras.models.load_model(f"models/{tl_model}.h5")


# creates save checkpoints and rules for early stop of the model
def create_callbacks(patience):

    checkpoint = ModelCheckpoint("models/face_classifier.h5",
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

    return [checkpoint, earlystop]


# fit the model
def fit_model(model, t_ds, v_ds, epochs, callbacks, modelname):
    model.fit(
        t_ds,
        epochs=epochs,
        callbacks=callbacks,
        # steps_per_epoch=len(train_ds)/train_ds.batch_size,
        validation_data=v_ds,
        # validation_steps=len(val_ds)/val_ds.batch_size
    )
    model.save(f"models/{modelname}.h5")
