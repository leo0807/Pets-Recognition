import os
from keras.models import load_model
from helper import No_Preprocessing
from keras.preprocessing import image
import dlib
import numpy as np
import helper


# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# face detector
pathDet = '../Emotion_Dog/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(pathDet)

# load model
model = load_model('../Emotion_Dog/Dog_classifier.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# helper class
helper = No_Preprocessing(img_width, img_height)

# load model
test_img = '../testImages/dog_neutral_1.jpg'
if os.path.exists(test_img):
    print("find test image: ", test_img)
else:
    print("not find test image")

test_img = image.load_img(test_img, target_size=(img_width, img_height), color_mode="grayscale")

# convert input image in input format that model accepts
test_img = image.img_to_array(test_img)
test_img = np.expand_dims(test_img, axis=0)

prediction = helper.predict_emotion(model, test_img)
print(prediction)

