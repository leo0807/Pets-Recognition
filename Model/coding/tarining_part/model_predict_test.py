import os

import dlib
import numpy as np
from helper import No_Preprocessing
from keras.models import load_model
from keras.preprocessing import image

# ---------------------------------------------------------

# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# face detector
pathDet = '../faceDetectors/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(pathDet)

# landmarks detector
pathPred = '../faceDetectors/landmarkDetector.dat'
predictor = dlib.shape_predictor(pathPred)

# helper class
helper = No_Preprocessing(img_width, img_height)

# load model
# model = load_model('models/classifierRotatedOn100Ratio90.h5')
test_img = 'Data for project/test/cat_fearful_1.jpg'
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
if prediction[0][0] == 0:
    print('Cat')
else:
    print('Dog')
