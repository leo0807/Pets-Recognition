import tensorflow as tf
"""
this file stores most parameters and paths used in training.
"""
# size of images
IMG_WIDTH = 200
IMG_HEIGHT = 200
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH)
# load saved model
TRAINED_MODEL = '../../../Web/FlaskServer/Cat_vs_Dog/Cat_Dog_model.h5'
# path for results
MODEL_PATH = "../../models/models/"
CSV_PATH = "../../models/csv/"
PLOT_PATH = "../../models/plots/"
LOG_PATH = "../../models/logs/"
# Data path
DOG_TRAIN_DATA = '../../../../Data for project/New_Data/dog/train'
DOG_VALID_DATA = '../../../../Data for project/New_Data/dog/test'
DOG_VALID_DATA_FACE = '../../../../Data for project/New_Data/dog/test_face'
CAT_TRAIN_DATA = '../../../../Data for project/New_Data/cat/train'
CAT_VALID_DATA = '../../../../Data for project/New_Data/cat/test'
CAT_VALID_DATA_FACE = '../../../../Data for project/New_Data/cat/test_face'

# hyper parameters for models
BATCH_SIZE = 32
DENSE = 1024
EPOCH = 25
MODEL_LOSS = 'categorical_crossentropy'
MODEL_OPTIMISER = tf.keras.optimizers.Adam()
METRICS = ['accuracy']

