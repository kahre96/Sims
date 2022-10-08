import fc_model_builder_functions as fc_f
from keras.optimizers import Adam
from keras.models import Model
import matplotlib.pyplot as plt

# tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU

img_height, img_width = 224, 224  # size of images
num_classes = 7  # amount of people
epochs = 3000
batch_size = 32
patience = 5  # amount of epoch without improvement before early exit
augmentation = "kaug"  # 1.noaug  2."kaug" for keras augmentation
neurons = 128
dd_layer = True
ds_dir = "Images"  # location of the dataset
VggBase = True  # true to use base pretrained model, # false to transfer learn one of our models
tl_model = "VGG16_aug"  # enter name of model that will be used for transfer learning

name_add = ""
if dd_layer:
    name_add = f"x{neurons}"

modelname = f"{ds_dir}_a{augmentation}_wGuest_N{neurons}{name_add}"  # name of the model when saved to disk as h5 file


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


history = fc_f.fit_model(face_classifier, train_ds, val_ds, epochs, callbacks, modelname)

fig, axs = plt.subplots(2, 1, figsize=(30, 20))
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
