from Model_builder import ModelBuilder

# path to determine folder of dataset
# epochs to determine amount of epochs
# patience ot determine after how many epochs without improvement the program will stop
# alb_aug True to use albumentation augmentation, False for no augmentation
# img_h set image height, default 224
# img_w set image width, default 224
# batch_size set the batch size, default 32
# neurons input each layers neurons as array, default [256,128]
# drop_rate drop rate inbetween each layer as an array, default [0.75 0.5]
# modeltype string to determine model architecture, vgg16 or resnet50

ModelBuilder_obj = ModelBuilder(epochs=3000, path='Images', alb_aug=True)
ModelBuilder_obj.train_model()
