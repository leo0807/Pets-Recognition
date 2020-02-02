from keras.models import load_model
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import math
import os
import shutil


import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as k
from keras.models import Sequential
# from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask, render_template
import tensorflow as tf
from keras.backend import set_session
from scripts import Emotion_Dog
from scripts import Emotion_Cat
# from scripts import Breed_Cat
from scripts import Breed_Dog

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("predict.html")

@app.route("/predict", methods= ["POST"])
def predict():
    message = request.get_json(force = True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))

    image.save("testImages/image.jpg")

    # dogEmotion = Emotion_Dog.predict()
    # catEmotion  = Emotion_Cat.predict()
    dogBreed = Breed_Dog.predict()

    response = {
        'prediction':{
            # 'emotion': catEmotion.to_string(index=False, header=False)
            'emotion' : dogBreed.to_string(index=False, header=False)
        }
    }


    os.remove("testImages/image.jpg")


    return jsonify(response)

#
# # image size for prediction
# img_width = 100
# img_height = 100
# # scale factor for preprocessing
# picSize = 200
# rotation = True
#
# # image input and output
# path ='testImages'
# pathResult = 'results'
#
# # face detector
# pathDet = 'faceDetectors/dogHeadDetector.dat'
# detector = dlib.cnn_face_detection_model_v1(pathDet)
#
# # landmarks detector
# pathPred = 'faceDetectors/landmarkDetector.dat'
# predictor = dlib.shape_predictor(pathPred)
#
# # helper class
# helper = No_Preprocessing(img_width, img_height)
#
# global graph,sess
# graph = tf.get_default_graph()
# sess = tf.Session()
# set_session(sess)
#
# # load model
# with graph.as_default():
#     model = load_model('models/classifierRotatedOn100Ratio90.h5')
#
#
#
#
# def preprocess(path):
#   # read image from path
#   orig = cv2.imread(path)
#
#   if orig.any() == True:
#     # resize
#     height, width, channels = orig.shape  # read size
#     ratio = picSize / height
#     image = cv2.resize(orig, None, fx=ratio, fy=ratio)
#
#     # color gray
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # detect face(s)
#     dets = detector(gray, upsample_num_times=1)
#
#     imageList = []  # for return
#     for i, d in enumerate(dets):
#       # save coordinates
#       x1 = max(int(d.rect.left() / ratio), 1)
#       y1 = max(int(d.rect.top() / ratio), 1)
#       x2 = min(int(d.rect.right() / ratio), width - 1)
#       y2 = min(int(d.rect.bottom() / ratio), height - 1)
#
#       # detect landmarks
#       shape = face_utils.shape_to_np(predictor(gray, d.rect))
#       points = []
#       index = 0
#       for (x, y) in shape:
#         x = int(round(x / ratio))
#         y = int(round(y / ratio))
#         index = index + 1
#         if index == 3 or index == 4 or index == 6:
#           points.append([x, y])
#       points = np.array(points) # right eye, nose, left eye
#
#       # rotate
#       if rotation == True:
#         xLine = points[0][0] - points[2][0]
#         if points[2][1] < points[0][1]:
#           yLine = points[0][1] - points[2][1]
#           angle = math.degrees(math.atan(yLine / xLine))
#         else:
#           yLine = points[2][1] - points[0][1]
#           angle = 360 - math.degrees(math.atan(yLine / xLine))
#         rotated = imutils.rotate(orig, angle)
#         # detectFace(rotated, picSize)
#
#       # highlight face and landmarks
#       cv2.polylines(orig, [points], True, (0, 255, 0), 1)
#       cv2.rectangle(orig, (x1, y1), (x2, y2), (255, 0, 0), 1)
#       imageList.append(orig)
#
#       # prepare for prediction
#       little = cv2.resize((rotated[y1:y2, x1:x2]), (img_width, img_height))  # crop and resize
#       pixel = cv2.cvtColor(little, cv2.COLOR_BGR2GRAY)
#       x = np.expand_dims(pixel, axis=0)
#       x = x.reshape((-1, 100, 100, 1))
#       imageList.append(x)
#       return imageList  # order: marked picture, input for classifier
#   return None
#
# # -------------------------------------------------------------------------------
#
# def result():
#     with graph.as_default():
#         set_session(sess)
#         # delete old results
#         if os.path.isdir(pathResult) == True:
#             shutil.rmtree(pathResult)
#             print('Result folder has been emptied.')
#         os.mkdir(pathResult)
#
#         # -------------------------------------------------------------------------------
#
#         counter = 0
#
#         # loop over all images
#         for filename in sorted(os.listdir(path)):
#             if filename != ".DS_Store":
#                 print('---------------------------------------------------')
#                 counter = counter + 1
#                 pathImage = path + "/" + filename
#                 fileType = (filename.split('.'))[-1]
#
#                 # read and preprocess image
#                 images = preprocess(pathImage)
#                 if images != None:  # found face on image
#                     x = images[1]
#                     marked = images[0]
#
#                     # model = load_model('models/classifierRotatedOn100Ratio90.h5')
#
#                     global df
#                     df = helper.predict_emotion(model, x)
#
#                     # sort and extract most probable emotion
#                     df = df.sort_values(by='prob', ascending=False)
#                     emotion = df['emotion'].values[0]
#                     prob = str(round((df['prob'].values[0]) * 100, 2))
#
#                     newPath = pathResult + '/' + str("{:03d}".format(counter)) + emotion + '.' + fileType
#
#                     height, width, channels = marked.shape  # read size
#                     overlay = marked.copy()  # save orig
#                     # draw semi-transparent layer
#                     cv2.rectangle(marked, (0, 0), (width, 45), (0, 0, 0), -1)
#                     marked = cv2.addWeighted(marked, 0.5, overlay, 0.5, 0)
#
#                     # marked = np.concatenate((img, marked), axis=0)
#                     text = emotion + ': ' + prob + '%'
#
#                     # Write some Text
#                     cv2.putText(marked,  # image
#                                 text,
#                                 (10, 30),  # text position
#                                 cv2.FONT_HERSHEY_SIMPLEX,  # font
#                                 0.6,  # fontScale
#                                 (255, 255, 255),  # font color
#                                 1,  # line type
#                                 cv2.LINE_AA)
#
#                     cv2.imwrite(newPath, marked)  # save
#                     print(pathImage + " --> " + newPath)
#                     print(df)
#
#





