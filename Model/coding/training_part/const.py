import tensorflow as tf
import util
# size of images
IMG_WIDTH = 200
IMG_HEIGHT = 200
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH)
# path for results
MODEL_PATH = "../../models/"
DOG_TRAIN_DATA = '../../../../Data for project/new/dog/train'
DOG_VALID_DATA = '../../../../Data for project/new/dog/test'
CAT_TRAIN_DATA = '../../../../Data for project/new/cat/train'
CAT_VALID_DATA = '../../../../Data for project/new/cat/test'
BATCH_SIZE = 64
MODEL_LOSS = 'categorical_crossentropy'
# MODEL_LOSS = 'kullback_leibler_divergence'
MODEL_OPTIMISER = tf.keras.optimizers.Adam()
EPOCH = 30
METRICS = ['mae', 'accuracy']
DENSE = 1024
TRAINED_MODEL = '../../models/cat_VGG19_v3_connected1024.h5'
