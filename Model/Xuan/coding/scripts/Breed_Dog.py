import os
import sys
import urllib.request

import numpy as np
import pandas as pd
import tensorflow as tf

from coding.Breed_Dog import consts
from coding.Breed_Dog import dataset
from coding.Breed_Dog import freeze
from coding.Breed_Dog import paths


def infer(model_name, img_raw):
    with tf.Graph().as_default(), tf.Session().as_default() as sess:
        tensors = freeze.unfreeze_into_current_graph(
            os.path.join(paths.FROZEN_MODELS_DIR, model_name + '.pb'),
            tensor_names=[consts.INCEPTION_INPUT_TENSOR, consts.OUTPUT_TENSOR_NAME])

        _, one_hot_decoder = dataset.one_hot_label_encoder()

        probs = sess.run(tensors[consts.OUTPUT_TENSOR_NAME],
                         feed_dict={tensors[consts.INCEPTION_INPUT_TENSOR]: img_raw})

        breeds = one_hot_decoder(np.identity(consts.CLASSES_COUNT)).reshape(-1)

        # print(breeds)

        df = pd.DataFrame(data={'prob': probs.reshape(-1), 'breed': breeds})


        return df.sort_values(['prob'], ascending=False)


def classify(resource_type, path):
    if resource_type == 'uri':
        response = urllib.request.urlopen(path)
        img_raw = response.read()
    else:
        with open(path, 'rb') as f:
            img_raw = f.read()

    return infer(consts.CURRENT_MODEL_NAME, img_raw)

src = '../Breed_Dog/inference.py'
path = '../testImages/dog_neutral_2.jpg'  # dog image to classify
probs = classify(src, path)

print(probs.sort_values(['prob'], ascending=False).take(range(3)))

