import os

import cv2
import tensorflow as tf

from scripts.helper import No_Preprocessing
from keras.preprocessing import image
import dlib
from imutils import face_utils
import imutils
import numpy as np
from keras.backend import set_session
from tensorflow.keras.applications.xception import preprocess_input

# ---------------------------------------------------------

# image size for prediction
img_width = 200
img_height =200
# scale factor for preprocessing
picSize = 400
rotation = True

# cat face detector
pathCat = 'Emotion_Cat/haarcascade_frontalcatface.xml'
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)

# load model
graph = tf.get_default_graph()
sess = tf.Session()
set_session(sess)
model = tf.keras.models.load_model('Emotion_Cat/Cat_classifier.h5')
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# helper class
helper = No_Preprocessing(img_width, img_height)

def predict():
    with graph.as_default():
        set_session(sess)

        test_img = 'testImages/image.jpg'

        test_img = image.load_img(test_img, target_size=(img_width, img_height), color_mode="rgb")
        # convert input image in input format that model accepts
        test_img = image.img_to_array(test_img)
        test_img = np.expand_dims(test_img, axis=0)
        test_img = preprocess_input(test_img)

        prediction = helper.predict_emotion(model, test_img)
        print(prediction)

        return prediction[:3]
