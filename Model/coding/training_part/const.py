import tensorflow as tf
# size of images
IMG_WIDTH = 200
IMG_HEIGHT = 200
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH)
# load saved model
TRAINED_MODEL = '../../models/models/cat_VGG19_v3_connected1024.h5'
# path for results
MODEL_PATH = "../../models/models/"
CSV_PATH = "../../models/csv/"
PLOT_PATH = "../../models/plots/"
LOG_PATH = "../../models/logs/"
DOG_TRAIN_DATA = '../../../../Data for project/New_Data/dog/train'
DOG_VALID_DATA = '../../../../Data for project/New_Data/dog/test'
DOG_VALID_DATA_FACE = '../../../../Data for project/New_Data/dog/test_face'
CAT_TRAIN_DATA = '../../../../Data for project/New_Data/cat/train'
CAT_VALID_DATA = '../../../../Data for project/New_Data/cat/test'
CAT_VALID_DATA_FACE = '../../../../Data for project/New_Data/cat/test_face'
BATCH_SIZE = 32
DENSE = 1024
EPOCH = 25
MODEL_LOSS = 'categorical_crossentropy'
MODEL_OPTIMISER = tf.keras.optimizers.Adam()
METRICS = ['accuracy']

