import os
import pickle
from Model_builder import ModelBuilder

if len(os.listdir("Images")) != len(pickle.loads(open("labels.pickle", "rb").read())):
    ModelBuilder_obj = ModelBuilder(epochs=300, path='Images', alb_aug=True)
    ModelBuilder_obj.train_model()
