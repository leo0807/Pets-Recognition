import os

import cv2
from keras.models import load_model
from helper import No_Preprocessing
from keras.preprocessing import image
import dlib
from imutils import face_utils
import imutils
import numpy as np

# ---------------------------------------------------------

# image size for prediction
img_width = 64
img_height = 64
# scale factor for preprocessing
picSize = 128
rotation = True

# cat face detector
pathCat = '../Emotion_Cat/'
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)

# helper class
helper = No_Preprocessing(img_width, img_height)

# load model
test_img = '../testImages/'
if os.path.exists(test_img):
    print("find test image")
else:
    print("not find test image")

test_img = image.load_img(test_img, target_size=(img_width, img_height))

# convert input image in input format that model accepts
test_img = image.img_to_array(test_img)
test_img = np.expand_dims(test_img, axis=0)

model = load_model('models/Cat_Dog_model.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

prediction = model.predict(test_img)
# prediction_ = np.argmax(prediction)
# predict 3 most likely results
top_k = 3
top_k_idx = prediction.argsort()[::-1][0:top_k]
print(prediction)
