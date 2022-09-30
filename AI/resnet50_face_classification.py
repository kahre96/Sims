import tensorflow as tf

#tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU


img_height, img_width = 224, 224  # size of images
num_classes = 6
epochs = 50
batch_size = 32
patience = 4
augmentation = False


if(augmentation == False):
    print("Training model without augmentation")
    normalization_layer = tf.keras.layers.Rescaling(1./255)

    #importing data
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
       "cropped_dataset",
       validation_split=0.2,
       label_mode="categorical",
       subset="training",
       seed=1,
       image_size=(img_height, img_width),
       batch_size=batch_size,


    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "cropped_dataset",
        validation_split=0.2,
        label_mode="categorical",
        subset="validation",
        seed=1,
        image_size=(img_height, img_width),
        batch_size=batch_size,


    )
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
else:
    print("Training with augmented dataset")
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1/255,  #normalizations
        #featurewise_center=True,
        #featurewise_std_normalization=True,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        brightness_range=(-0.2,0.2),
        horizontal_flip=True,
        validation_split=0.2)

    #datagen.fit(x_train?) # need to fit data if featurewise is used in datagen

    train_ds = datagen.flow_from_directory(
            "cropped_dataset",
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode='categorical')  #categorical data so categorical crossentropy can be used
    val_ds = datagen.flow_from_directory(
            "cropped_dataset",
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode='categorical')


base_model = tf.keras.applications.resnet50.ResNet50(
    include_top=False,
    weights='imagenet',
    input_shape=(img_height, img_width, 3),
)

#base_model.summary()

import keras

# Set layers to non-trainable
for layer in base_model.layers:
    layer.trainable = False

# Add custom layers on top of ResNet
global_avg_pooling = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(num_classes, activation='softmax')(global_avg_pooling)

face_classifier = keras.models.Model(inputs=base_model.input,
                                     outputs=output,
                                     name='ResNet50')


from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

# ModelCheckpoint to save model in case of
# interrupting the learning process
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

callbacks = [earlystop, checkpoint]
face_classifier.compile(loss='categorical_crossentropy',    #sparse_categorical_crossentropy
                        optimizer=Adam(learning_rate=0.01),
                        metrics=['accuracy'])


history = face_classifier.fit_generator(   #maybe fit_generator?
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    #steps_per_epoch=50,
    validation_data=val_ds,
    #validation_steps=50
    )

face_classifier.save("models/test.h5")

