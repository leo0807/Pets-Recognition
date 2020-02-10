import os

JPEG_EXT = '.jpg'
DATA_ROOT = '../Breed_Dog/data/'
# TRAIN_DIR = os.path.join(DATA_ROOT, 'train')
# TEST_DIR = os.path.join(DATA_ROOT, 'test')
#TRAIN_TF_RECORDS = os.path.join(ROOT, 'dogs_train.tfrecords')
# TRAIN_TF_RECORDS = os.path.join(DATA_ROOT, 'stanford.tfrecords')
TEST_TF_RECORDS = os.path.join(DATA_ROOT, 'dogs_test.tfrecords')
# LABELS = os.path.join(DATA_ROOT, 'train', 'labels.csv')
BREEDS = os.path.join(DATA_ROOT, 'breeds.csv')
IMAGENET_GRAPH_DEF = '../Breed_dog/frozen/inception/classify_image_graph_def.pb'
# TEST_PREDICTIONS = 'predictions.csv'
METRICS_DIR = '../Breed_Dog/metrics'
TRAIN_CONFUSION = os.path.join(METRICS_DIR, 'training_confusion.csv')
FROZEN_MODELS_DIR = '../Breed_Dog/frozen'
CHECKPOINTS_DIR = '../Breed_Dog/checkpoints'
GRAPHS_DIR = '../Breed_Dog/graphs'
SUMMARY_DIR = '../Breed_Dog/summary'
# STANFORD_DS_DIR = os.path.join(DATA_ROOT, 'stanford_ds')
# STANFORD_DS_TF_RECORDS = os.path.join(DATA_ROOT, 'stanford.tfrecords')

