import os

import cv2
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import load_model
from scripts.helper import No_Preprocessing
from keras.preprocessing import image
import dlib
from imutils import face_utils
import imutils
import numpy as np
from keras.backend import set_session

# ---------------------------------------------------------

# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# cat face detector
pathCat = 'Emotion_Cat/'
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)

# load model
graph = tf.get_default_graph()
sess = tf.Session()
set_session(sess)
model = tf.keras.models.load_model('Emotion_Cat/Cat_classifier_v2.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# helper class
helper = No_Preprocessing(img_width, img_height)

def predict():
    with graph.as_default():
        set_session(sess)
        test_img = 'testImages/image.jpg'

        test_img = image.load_img(test_img, target_size=(img_width, img_height), color_mode="grayscale")

        # convert input image in input format that model accepts
        test_img = image.img_to_array(test_img)
        test_img = np.expand_dims(test_img, axis=0)

        prediction = helper.predict_emotion(model, test_img)
        # prediction = model.predict(test_img)
        # prediction = np.argmax(prediction)
        # predict 3 most likely results
        # top_k = 3
        # top_k_idx = prediction.argsort()[::-1][0:top_k]
        print(prediction)
        return prediction


