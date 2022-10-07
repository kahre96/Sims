import fc_model_builder_functions as fc_f
from keras.optimizers import Adam
from keras.models import Model
# tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU

img_height, img_width = 224, 224  # size of images
num_classes = 6  # amount of people
epochs = 3000
batch_size = 32
patience = 5  # amount of epoch without improvement before early exit
augmentation = 1  # 1.NO  2. keras augmentation 3. kerasv2 albumentation
neurons = 4096
dd_layer = False
ds_dir = "Images"  # location of the dataset
modelname = "noaug_N4096x4096"  # name of the model when saved to disk as h5 file
VggBase = True  # true to use base pretrained model, # false to transfer learn one of our models
tl_model = "VGG16_aug"  # enter name of model that will be used for transfer learning


train_ds, val_ds = fc_f.import_data(augmentation, ds_dir, img_width, img_height, batch_size)


if VggBase:
    base_model = fc_f.create_basemodel(img_height, img_width)
else:
    base_model = fc_f.load_model(tl_model)


head = fc_f.TopModel(base_model, num_classes, neurons, dd_layer)

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



