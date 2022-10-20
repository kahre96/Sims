import pickle
import os
import numpy as np
import pandas as pd
import random


class CreateDataset:

    def __init__(self, directory, cat=False):

        """
        This will return the paths to each image.
        if cat = False it will return labels as integers(label encoding). Default = False
        if cat = True it will return each label as one hot encoding

        !!IMPORTANT!!
        If cat = False: set model.compile as sparse categorical crossentropy.
        if cat = True:  set model.compile as categorical crossentropy

        """
        self.directory = directory
        self.cat = cat
        self.paths = []
        self.labels = []
        self.class_names = sorted(os.listdir(self.directory))

    def set_dataset(self):
        class_names = self.class_names  # this will save the labels for the model
        f = open('labels.pickle', "wb")
        f.write(pickle.dumps(class_names))
        f.close()
        i = 0
        if self.cat == False:
            class_number = np.unique(self.class_names, return_inverse=True)[1]  # label encoding
        else:
            class_number = np.array(pd.get_dummies(self.class_names).T)  # one hot
        for labels in self.class_names:
            i += 1
            for img in os.listdir(os.path.join(self.directory, labels)):
                self.paths.append(os.path.join(self.directory, labels, img))
                self.labels.append(class_number[i - 1])

        dataset = list(zip(self.paths, self.labels))
        data = random.sample(dataset, len(dataset))
        indexes = int(len(data) - 1)
        train_ds = data[:int(indexes * 0.7)]
        val_ds = data[len(train_ds):indexes]
        return train_ds, val_ds
