import tensorflow as tf
from kerasv2 import kv2
import keras
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

# tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU

img_height, img_width = 224, 224  # size of images
num_classes = 6  # amount of people
epochs = 3000
batch_size = 32
patience = 5  # amount of epoch without improvement before early exit
augmentation = 1  # 1.NO  2. keras augmentation 3. kerasv2 albumentation
ds_dir = "Images"  # location of the dataset
modelname = "VGG19_aug_itt2"  # name of the model when saved to disk as h5 file
VggBase = False  #true to use base pretrained model, # false to transfer learn one of our models
tlmodel = "VGG19_aug"  # enter name of model that will be used for transfer learning
test = False  # Enable if testds is available

if (augmentation == 1):
    print("Training model without augmentation")
    normalization_layer = tf.keras.layers.Rescaling(1. / 255)

    # importing data
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        ds_dir,
        validation_split=0.2,
        label_mode="categorical",
        subset="training",
        seed=1,
        image_size=(img_height, img_width),
        batch_size=batch_size,

    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        ds_dir,
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
    #test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))

elif (augmentation == 2):
    print("Training with augmented dataset")
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1 / 255,  # normalizations
        # featurewise_center=True,
        # featurewise_std_normalization=True,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        brightness_range=(-0.2, 0.2),
        horizontal_flip=True,
        validation_split=0.2)

    # datagen.fit(x_train?) # need to fit data if featurewise is used in datagen

    train_ds = datagen.flow_from_directory(
        ds_dir+"/train",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')  # categorical data so categorical crossentropy can be used
    val_ds = datagen.flow_from_directory(
        ds_dir+"/val",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

elif (augmentation == 3):
    train_ds, val_ds, test_ds = kv2(batch_size, ds_dir)
else:
    print("incorrect augmentation option")
    quit()

#decide if base Vgg is gona be used or if our pretrained models will be used
if VggBase:
    base_model = tf.keras.applications.vgg16.VGG16(
        include_top=False,
        weights='imagenet',
        input_shape=(img_height, img_width, 3),
    )
    # Set layers to non-trainable
    for layer in base_model.layers:
        layer.trainable = False

    # Add custom layers on top of the model

    global_avg_pooling = keras.layers.GlobalAveragePooling2D()(base_model.output)
    output = keras.layers.Dense(num_classes, activation='softmax')(global_avg_pooling)
else:
    print(f"Transfer learning on {tlmodel}")
    base_model = keras.models.load_model(f"models/{tlmodel}.h5")

    # Set layers to non-trainable
    #for layer in base_model.layers:
    #    layer.trainable = False

    # Add custom layers on top of the model

    output = base_model.output


face_classifier = keras.models.Model(inputs=base_model.input,
                                     outputs=output,
                                     name='VGG16')

#face_classifier.summary()

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
face_classifier.compile(loss='categorical_crossentropy',  # sparse_categorical_crossentropy
                        optimizer=Adam(learning_rate=0.01),
                        metrics=['accuracy'])

history = face_classifier.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    # steps_per_epoch=len(train_ds)/train_ds.batch_size,
    validation_data=val_ds,
    # validation_steps=len(val_ds)/val_ds.batch_size
)

face_classifier.save(f"models/{modelname}.h5")


# evaluate the model with test dataset
if (test == True):
    result = face_classifier.evaluate(test_ds)
    print(result)
