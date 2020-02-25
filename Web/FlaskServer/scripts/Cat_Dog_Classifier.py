import os

import keras
from keras.models import load_model
from scripts.helper import No_Preprocessing
from keras.preprocessing import image
import dlib
from imutils import face_utils
import imutils
import numpy as np
from keras.backend import set_session
import tensorflow as tf
import time
from tensorflow.keras.applications.vgg19 import preprocess_input


# ---------------------------------------------------------
# load models
graph = tf.get_default_graph()
sess = tf.Session()
set_session(sess)

model = tf.keras.models.load_model('Cat_vs_Dog/Cat_Dog_model.h5')
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# image size for prediction
img_width = 200
img_height = 200
# scale factor for preprocessing
picSize = 400
rotation = True

# helper class
helper = No_Preprocessing(img_width, img_height)

def predict():

    with graph.as_default():
        set_session(sess)
        test_img = 'testImages/image.jpg'
        # if os.path.exists(test_img):
        #     print("find test image", test_img)
        # else:
        #     print("error, not find test image")

        test_img = image.load_img(test_img, target_size=(img_width, img_height))
        # convert input image in input format that model accepts
        test_img = image.img_to_array(test_img)
        test_img = np.expand_dims(test_img, axis=0)
        test_img = preprocess_input(test_img)

        start = time.time()
        prediction = model.predict(test_img)
        prediction_ = np.argmax(prediction)
        # print("time ", time.time() -start)
        if prediction_ == 0:
            print('Cat!!!')
            return "Cat"
        elif prediction_ == 1:
            print('Dog!!!')
            return "Dog"
        else:
            print("No cat or dog or Error here! ")



