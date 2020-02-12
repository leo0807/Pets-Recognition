import os
import time

import cv2
import dlib
import pandas as pd
from helper import No_Preprocessing

# image size for prediction
img_width = 200
img_height = 200
# scale factor for preprocessing
picSize = 400
rotation = True

# image input and output
path = '../Data for project'
testpath = '../Data for project/dog/dog_neutral/dog_neutral_0.jpg'
pathResult = '../results'

# face detector
pathDet = '../Emotion_dog/dogHeadDetector.dat'
pathCat = "haarcascade_frontalcatface.xml"
pathCatExt = 'haarcascade_frontalcatface_extended.xml'
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)
extface = cv2.CascadeClassifier(cv2.data.haarcascades + pathCatExt)
detector = dlib.cnn_face_detection_model_v1(pathDet)

# helper class
helper = No_Preprocessing(img_width, img_height)


def find_label(path):
    emotion = -1
    if 'angry' in path:
        emotion = 0
    elif 'fearful' in path:
        emotion = 1
    elif 'happy' in path:
        emotion = 2
    elif 'sadness' in path:
        emotion = 3
    elif 'neutral' in path:
        emotion = 4
    return str(emotion)


def checkPath(savePath):
    if os.path.exists(savePath):
        print("path found: " + savePath)
    else:
        os.mkdir(os.path.abspath(savePath))
        print("create path: " + savePath)


def write2csv(csvPath, images):
    if images is not None and images != []:  # found face on image
        images = pd.DataFrame(images)
        images.to_csv(csvPath, header=False, index=False)


def dog_preprocess(path, savePath):
    orig = cv2.imread(path)
    dirpath, filedir = os.path.split(path)
    filename, extend = os.path.splitext(filedir)
    folderName = dirpath.split(os.sep)[-1]

    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)
        # image = cv2.resize(orig, (img_width*2, img_height*2))
        # color gray
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect face(s)
        start = time.time()
        dets = detector(image, upsample_num_times=1)
        print('detection time:', time.time() - start)

        for i, d in enumerate(dets):
            # save coordinates
            x1 = max(int(d.rect.left() / ratio), 1)
            y1 = max(int(d.rect.top() / ratio), 1)
            x2 = min(int(d.rect.right() / ratio), width - 1)
            y2 = min(int(d.rect.bottom() / ratio), height - 1)
            print(x1, y1, x2, y2)
            try:
                little = cv2.resize(image[y1:y2, x1:x2], (img_width, img_height))
                # checkPath(savePath + os.sep + folderName)
                # cv2.imwrite(savePath + os.sep + folderName + os.sep + filename + '.jpg', little)
                cv2.imwrite(savePath + filename + '.jpg', little)
                print('saved:', savePath + filename + '.jpg')
                return little.flatten()
            except:
                pass
    return None


def cat_preprocess(path, savePath):
    orig = cv2.imread(path)
    dirpath, filedir = os.path.split(path)
    filename, extend = os.path.splitext(filedir)
    folderName = dirpath.split(os.sep)[-1]

    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        # wratio = picSize / width
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)

        # color gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print('gray shape:', gray.shape)
        # detect face(s)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(60, 60),
        )
        for (i, (x, y, w, h)) in enumerate(faces):
            print(x, y, w, h)
            rmo = cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
            # prepare for prediction
            little = cv2.resize(image[y:y + h, x:x + w], (img_width, img_height))
            # checkPath(savePath + os.sep + folderName)
            cv2.imwrite(savePath + os.sep + folderName + os.sep + filename + '.jpg', little)
            # cv2.imshow("little", little)
            # cv2.imshow('rmo', rmo)
            # cv2.waitKey(0)
            # print(little.flatten())
            return little.flatten()
    return None

# --------define dog or cat to classify--------
classify = 'cat'

images = []
images.append(['emotion', 'pixels'])
folderPath = '../../../../Data for project' + os.sep + classify
savePath = '../../../../Data for project/new/' + classify
# imagespath = '../Data for project/dog/dog_neutral'
imagespath = '../Data for project/test/'
# print(os.getcwd())
# print(os.path.exists(folderPath))

# testImage = '../../../../Data for project/dog/dog_neutral/dog_neutral_287.jpg'
testImage = '../../../../Data for project/cat/cat_happy/cat_happy_1050.jpg'
# dirpath, filedir = os.path.split(testImage)
# filename, extend = os.path.splitext(filedir)
# folderName = dirpath.split(os.sep)[-1]
# print(folderName)
# dog_preprocess(testImage, '../../../../Data for project/')


cat_preprocess(testImage, savePath)

# for folders in os.listdir(folderPath):
#     folder = folderPath + os.sep + folders
#     for image in os.listdir(folder):
#         print(image)
#         ipath = folder + os.sep + image
#         label = find_label(ipath)
#         pixel = None
#         if classify == 'dog':
#             pixels = dog_preprocess(ipath, savePath)
#         else:
#             pixels = cat_preprocess(ipath, savePath)
#         if label != -1 and pixels is not None:
#             pixel = pixels
#             images.append([label, pixel])
# csvPath = '../../csv/' + classify + '_old_data_RGB' + '_V1' + '.csv'
# write2csv(csvPath, images)
