import keras
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
import numpy as np


norm_layer = tf.keras.layers.Rescaling(1. / 255)

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
            "../Nya_dataset_croppade",
            labels='inferred',
            seed=1337,
            image_size=(224, 224),
            batch_size=32


        )

model = keras.models.load_model('../models/knowit_vgg16_Images_noaug_0.75x0.5d_N512x256.h5')

test_y = []
test_x = []
y_pred = []


for x, y in test_ds.take(9999):
    test_y.append(y)
    y_temp = model(norm_layer(x))
    y_pred.append(tf.argmax(y_temp, axis=1))


test_asonearray = np.concatenate(test_y, axis=0)
pred_asonearray = np.concatenate(y_pred, axis=0)

cf = confusion_matrix(test_asonearray, pred_asonearray)

conf_m = sns.heatmap(cf, annot=True, cmap='Blues')

conf_m.set_title('Seaborn Confusion Matrix with labels\n\n')
conf_m.set_xlabel('\nPredicted Values')
conf_m.set_ylabel('Actual Values ')
plt.show()

