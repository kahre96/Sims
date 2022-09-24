import tensorflow as tf
import keras

tf.config.set_visible_devices([], 'GPU')

img_height, img_width = 224, 224  # size of images
num_classes = 6


base_model = tf.keras.applications.xception(weights="imagenet",
                                            include_top=False,
                                            input_shape=(img_height,img_width, 3))


global_avg_pooling = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(num_classes, activation='sigmoid')(global_avg_pooling)

# Set layers to non-trainable
for layer in base_model.layers:
    layer.trainable = False


face_classifier = keras.models.Model(inputs=base_model.input,
                                     outputs=output,)

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
                          patience=3,  # number of epochs with
                                       # no improvement after which
                                       # training will be stopped
                          verbose=1)

callbacks = [earlystop, checkpoint]
face_classifier.compile(loss='categorical_crossentropy',    #sparse_categorical_crossentropy
                        optimizer=Adam(learning_rate=0.01),
                        metrics=['accuracy'])


epochs = 20

history = face_classifier.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds)


face_classifier.save("Xception_tbd")

