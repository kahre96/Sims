import fc_model_builder_functions as fc_f
from keras.optimizers import Adam
from keras.models import Model
import numpy as np
import visualkeras
from PIL import ImageFont

# tf.config.set_visible_devices([], 'GPU') #uncomment to force CPU

img_height, img_width = 224, 224  # size of images
num_classes = 11  # amount of people
epochs = 3000
batch_size = 32
patience = 10  # amount of epoch without improvement before early exit
augmentation = "kaug"  # 1.noaug  2."kaug" for keras augmentation
neurons = 256
neurons2 = 128
drop_rate = 0.75
drop_rate2 = 0.5
dd_layer = True     #enable 2 layers
ds_dir = "../Images"  # location of the dataset
model_name = 'vgg16'  #name of pretrained model in VGGFace to be used, options are 'vgg16', 'resnet50', 'senet50'
tl_model = "VGG16_aug"  # enter name of model that will be used for transfer learning

name_add = ""
if dd_layer:
    name_add = f"x{neurons2}"

d_name = ""
if drop_rate2 is not None:
    d_name = f"x{drop_rate2}"


fc_f.save_labels(ds_dir)

modelname = f"knowit_{model_name}_{ds_dir}_{augmentation}_{drop_rate}{d_name}d_N{neurons}{name_add}"  # name of the model when saved to disk as h5 file


train_ds, val_ds = fc_f.import_data(augmentation,ds_dir, img_width, img_height, batch_size)


base_model = fc_f.create_basemodel(img_height, img_width, model_name)


head = fc_f.topModel(base_model, num_classes, neurons, dd_layer, neurons2, drop_rate, drop_rate2)

face_classifier = Model(inputs=base_model.input, outputs=head, name='VGG16')

#font = ImageFont.truetype("C:\Windows\Fonts\Pala.ttf", 30)

#visualkeras.layered_view(face_classifier, legend=True, font=font, to_file='vgg_viz.png')



callbacks = fc_f.create_callbacks(patience)

face_classifier.summary()


face_classifier.compile(loss='categorical_crossentropy',  # sparse_categorical_crossentropy
                        optimizer=Adam(learning_rate=0.001),
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
best_epochs = np.argmin(history.history['val_loss'])
print("val_accuracy", history.history['val_accuracy'][best_epochs])
print("val_loss", history.history['val_loss'][best_epochs])
print("accuracy", history.history['accuracy'][best_epochs])
print("loss", history.history['loss'][best_epochs])
fc_f.plot_epochs(history)



