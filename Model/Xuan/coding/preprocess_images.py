from keras.models import load_model
from helper import No_Preprocessing
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import math
import os
import shutil

# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# image input and output
path = '../../Data for project'
pathResult = '../results'

# face detector
pathDet = '../faceDetectors/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(pathDet)

# landmarks detector
pathPred = '../faceDetectors/landmarkDetector.dat'
predictor = dlib.shape_predictor(pathPred)

# helper class
helper = No_Preprocessing(img_width, img_height)


def renameFile(path):
    print('come into path:' + path)
    fileList = os.listdir(path)
    for file in fileList:
        oldfilename = path + os.sep + file
        newfilename = path + os.sep + file[:-4] + '.jpg'
        os.rename(oldfilename, newfilename)
        print(oldfilename + ' -> ' + newfilename)
    print("done")


def preprocess(path):
    if os.path.exists(path):
        print("find path " + path)

    # read image from path
    orig = cv2.imread(path)

    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)

        # color gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect face(s)
        dets = detector(gray, upsample_num_times=1)

        imageList = []  # for return
        for i, d in enumerate(dets):
            # save coordinates
            x1 = max(int(d.rect.left() / ratio), 1)
            y1 = max(int(d.rect.top() / ratio), 1)
            x2 = min(int(d.rect.right() / ratio), width - 1)
            y2 = min(int(d.rect.bottom() / ratio), height - 1)

            # detect landmarks
            shape = face_utils.shape_to_np(predictor(gray, d.rect))
            points = []
            index = 0
            for (x, y) in shape:
                x = int(round(x / ratio))
                y = int(round(y / ratio))
                index = index + 1
                if index == 3 or index == 4 or index == 6:
                    points.append([x, y])
            points = np.array(points)  # right eye, nose, left eye

            # rotate
            if rotation == True:
                xLine = points[0][0] - points[2][0]
                if points[2][1] < points[0][1]:
                    yLine = points[0][1] - points[2][1]
                    angle = math.degrees(math.atan(yLine / xLine))
                else:
                    yLine = points[2][1] - points[0][1]
                    angle = 360 - math.degrees(math.atan(yLine / xLine))
                rotated = imutils.rotate(orig, angle)
                # detectFace(rotated, picSize)

            # highlight face and landmarks
            cv2.polylines(orig, [points], True, (0, 255, 0), 1)
            cv2.rectangle(orig, (x1, y1), (x2, y2), (255, 0, 0), 1)
            imageList.append(orig)

            # prepare for prediction
            little = cv2.resize((rotated[y1:y2, x1:x2]), (img_width, img_height))  # crop and resize
            pixel = cv2.cvtColor(little, cv2.COLOR_BGR2GRAY)
            x = np.expand_dims(pixel, axis=0)
            x = x.reshape((-1, 100, 100, 1))
            imageList.append(x)
            return imageList  # order: marked picture, input for classifier
    return None

# ----------------- rename files --------------------#
# for folders in os.listdir(path):
#     # print(folders)
#     folderPath = path + os.sep + folders
#     for folders in os.listdir(folderPath):
#         imagespath = folderPath + os.sep + folders
#         renameFile(imagespath)
# ---------------------------------------------------#



# renameFile(path)
# for filepath in os.listdir(path):
#     print(filepath)
#     print(preprocess(path + os.sep + filepath))
