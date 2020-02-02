import os
from keras.models import load_model
from helper import No_Preprocessing
from keras.preprocessing import image
import dlib
from imutils import face_utils
import imutils
import numpy as np

# ---------------------------------------------------------
# load models
model = load_model('../Cat_vs_Dog/Cat_Dog_model.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# image size for prediction
img_width = 64
img_height = 64
# scale factor for preprocessing
picSize = 128
rotation = True

# helper class
helper = No_Preprocessing(img_width, img_height)

# load model
test_img = 'testImages/'
if os.path.exists(test_img):
    print("find test image", test_img)
else:
    print("error, not find test image")

test_img = image.load_img(test_img, target_size=(img_width, img_height))
# convert input image in input format that model accepts
test_img = image.img_to_array(test_img)
test_img = np.expand_dims(test_img, axis=0)

prediction = model.predict(test_img)
# prediction_ = np.argmax(prediction)
if prediction[0][0] == 0:
    print('Cat')
else:
    print('Dog')
