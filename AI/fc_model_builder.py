import fc_model_builder_functions as fc_f
from keras.optimizers import Adam
from keras.models import Model


# tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU

img_height, img_width = 224, 224  # size of images
num_classes = 7  # amount of people
epochs = 3
batch_size = 32
patience = 5  # amount of epoch without improvement before early exit
augmentation = "noaug"  # 1.noaug  2."kaug" for keras augmentation
neurons = 128
dd_layer = True
ds_dir = "Images"  # location of the dataset
VggBase = True  # true to use base pretrained model, # false to transfer learn one of our models
tl_model = "VGG16_aug"  # enter name of model that will be used for transfer learning

name_add = ""
if dd_layer:
    name_add = f"x{neurons}"


fc_f.save_labels(ds_dir)

#modelname = f"{ds_dir}_a{augmentation}_wGlasses_N{neurons}{name_add}"  # name of the model when saved to disk as h5 file
modelname = "asdasd"

train_ds, val_ds = fc_f.import_data(augmentation,ds_dir, img_width, img_height, batch_size)


if VggBase:
    base_model = fc_f.create_basemodel(img_height, img_width)
else:
    base_model = fc_f.load_model(tl_model)


head = fc_f.topModel(base_model, num_classes, neurons, dd_layer)

face_classifier = Model(inputs=base_model.input, outputs=head, name='VGG16')

callbacks = fc_f.create_callbacks(patience)

face_classifier.summary()


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
fc_f.plot_epochs(history)



