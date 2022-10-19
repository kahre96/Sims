import tensorflow as tf
import random
import numpy as np
from PIL import Image
import albumentations as alb

transformer1 = alb.Compose([alb.HorizontalFlip(p=0.3),  ## flip picture vertical
    alb.geometric.rotate.Rotate(limit=[-5, 5], p=0.3),
    alb.OneOf([ alb.RandomBrightnessContrast(brightness_limit=(-0.35, 0.35), contrast_limit=(-0.35, 0.35)),
               alb.GaussNoise((0,255.0)),
               alb.GaussianBlur((17,29),0),
               alb.MotionBlur(17),alb.RandomGamma()], p = 0.7)
])


class CustomDataGen(tf.keras.utils.Sequence):
    """

    When we increase ppl in the dataset, we will go OOM on RAM.
    This generator will therefore be optimal to use when we have large amount of pictures.

    """

    def __init__(self, normalization, data, batch_size, shuffle=True, transformer=transformer1):
        self.data = random.sample(data, len(data))  # shuffles the list again
        self.batch_size = batch_size
        self.n = int(len(self.data))
        self.indices = list(range(0, len(self.data)))
        self.shuffle = shuffle
        self.index = None
        self.transformer = transformer
        self.normalization = normalization
        if self.normalization == 'minmax':
            print('Using min-max-normalization')
        else:
            print('Using mean std normalization')
        self.on_epoch_end()

    def on_epoch_end(self):
        self.index = np.arange(len(self.indices))
        if self.shuffle:
            np.random.shuffle(self.index)

    def __get_data(self, start_index, end_index):
        """
        This will generate image augmentations per batch.
        """
        data = self.data[start_index:end_index]
        data_x, data_y = list(zip(*data))
        X = []
        for item in data_x:
            image = Image.open(item)
            image = np.array(image)
            image = self.img_aug(image)
            if self.normalization == 'minmax':
                image = self.minmaxnorm(image)  # min-max-normalization
            else:
                image = self.znorm(image)  # mean std normalization
            X.append(image)
        return X, data_y

    def minmaxnorm(self, x):
        return ((x - x.min()) / (x.max() - x.min()))

    def znorm(self, x):
        return (x - x.mean(axis=(0, 1, 2), keepdims=True)) / x.std(axis=(0, 1, 2), keepdims=True)

    def img_aug(self, x):
        augment_img = self.transformer(image=x)
        return augment_img['image']

    def __getitem__(self, index):
        """
        __getitem__ will get the X,y data from calling __get_data and then convert to tensors.
        This will then be forwarded to the model.
        """
        start_index = int(index * self.batch_size)
        end_index = int((index + 1) * self.batch_size)
        X, y = self.__get_data(start_index, end_index)
        X = tf.convert_to_tensor(np.array(X))
        y = tf.convert_to_tensor(np.array(y), dtype=tf.uint8)
        return X, y

    def __len__(self):
        return self.n // self.batch_size
