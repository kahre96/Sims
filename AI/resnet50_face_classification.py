import tensorflow as tf

tf.config.set_visible_devices([], 'GPU')

normalization_layer = tf.keras.layers.Rescaling(1./255)

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "content/images",
    validation_split=0.2,
    subset="training",
    seed=1,
    image_size=(200,200),
    batch_size=32,


)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "content/images",
    validation_split=0.2,
    subset="validation",
    seed=1,
    image_size=(200,200),
    batch_size=32,


)


train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

img_height, img_width = 200, 200  # size of images
num_classes = 4

base_model = tf.keras.applications.resnet50.ResNet50(
    include_top=False,
    weights='imagenet',
    input_shape=(img_height,img_width,3),
)

#base_model.summary()

import keras

# Set layers to non-trainable
for layer in base_model.layers:
    layer.trainable = False

# Add custom layers on top of ResNet
global_avg_pooling = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(num_classes, activation='sigmoid')(global_avg_pooling)

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
                          patience=3,  # number of epochs with
                                       # no improvement after which
                                       # training will be stopped
                          verbose=1)

callbacks = [earlystop, checkpoint]
face_classifier.compile(loss='sparse_categorical_crossentropy',    #sparse_categorical_crossentropy
                        optimizer=Adam(learning_rate=0.01),
                        metrics=['accuracy'])


epochs = 20

history = face_classifier.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds)

face_classifier.save("models/resnet50_face_classifier_10e_croppedimg.h5")

