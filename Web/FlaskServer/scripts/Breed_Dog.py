import os
import sys
import urllib.request

import numpy as np
import pandas as pd
import tensorflow as tf

from Breed_Dog import consts
from Breed_Dog import dataset
from Breed_Dog import freeze
from Breed_Dog import paths
import time
from keras.backend import set_session


# start = time.time()

graph = tf.get_default_graph()
sess=tf.Session();
set_session(sess)
tensors = freeze.unfreeze_into_current_graph(
    os.path.join(paths.FROZEN_MODELS_DIR, consts.CURRENT_MODEL_NAME + '.pb'),
    tensor_names=[consts.INCEPTION_INPUT_TENSOR, consts.OUTPUT_TENSOR_NAME])

_, one_hot_decoder = dataset.one_hot_label_encoder()
# print("the time of load model ", time.time()-start)
def infer(img_raw):
    with graph.as_default():
        # tensors = freeze.unfreeze_into_current_graph(
        #     os.path.join(paths.FROZEN_MODELS_DIR, model_name + '.pb'),
        #     tensor_names=[consts.INCEPTION_INPUT_TENSOR, consts.OUTPUT_TENSOR_NAME])
        set_session(sess)

        # start = time.time()
        probs = sess.run(tensors[consts.OUTPUT_TENSOR_NAME],
                         feed_dict={tensors[consts.INCEPTION_INPUT_TENSOR]: img_raw})

        # print("time 1 ", time.time()-start)
        breeds = one_hot_decoder(np.identity(consts.CLASSES_COUNT)).reshape(-1)

        # print(breeds)
        # print("time 2 ", time.time()-start)
        df = pd.DataFrame(data={'prob': probs.reshape(-1), 'breed': breeds})


        return df.sort_values(['prob'], ascending=False)


def classify(resource_type, path):
    if resource_type == 'uri':
        response = urllib.request.urlopen(path)
        img_raw = response.read()
    else:
        with open(path, 'rb') as f:
            img_raw = f.read()

    return infer( img_raw)


def predict():
    # start = time.time()

    src = 'Breed_Dog/inference.py'
    path = 'testImages/image.jpg'  # dog image to classify
    probs = classify(src, path)
    print(probs.sort_values(['prob'], ascending=False).take(range(3)))

    # print("predict time ",time.time()-start)
    return probs.sort_values(['prob'], ascending=False).take(range(3))


