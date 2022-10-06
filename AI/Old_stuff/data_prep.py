import os
import tensorflow as tf


print(tf.__version__)


trains_ds=tf.keras.preprocessing.image_dataset_from_directory(
    "Dataset",
    validation_split=0.2,
    subset="training",
    seed=1,
    image_size=(1280,720),
    batch_size=32,


)

val_ds=tf.keras.preprocessing.image_dataset_from_directory(
    "Dataset",
    validation_split=0.2,
    subset="validation",
    seed=1,
    image_size=(1280,720),
    batch_size=32,


)


import matplotlib.pyplot as plt

plt.figure(figsize=(10,10))
for images, labels in trains_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3,3, i+1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(int(labels[i]))

plt.show()