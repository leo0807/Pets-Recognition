import csv
import datetime
from keras.models import load_model
from helper import No_Preprocessing
import dlib
import cv2
from imutils import face_utils
import imutils
import numpy as np
import math
import os
from PIL import Image
import tensorflow as tf
import pandas as pd
import shutil

# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# image input and output
path = '../Data for project'
testpath = '../Data for project/dog/dog_neutral/dog_neutral_0.jpg'
pathResult = '../results'

# face detector
pathDet = '../faceDetectors/dogHeadDetector.dat'
pathCat = "haarcascade_frontalcatface.xml"

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)
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


# ---------------------------------------
def getSingleFilePixels(image_path):
    pixels = ""
    image = Image.open(image_path)
    matrix = np.asarray(image)
    for row in matrix:
        for pixel in row:
            pixels += str(pixel) + " "
    return pixels


def getAllFiles(path):
    all_file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                all_file_paths.append(root + os.sep + file)
    return all_file_paths


def writeImage2csv(folderPath, csvPath):
    with open(csvPath, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["emotion", "pixels"])
        all_file_paths = getAllFiles(folderPath)
        for path in all_file_paths:
            (filepath, tempfilename) = os.path.split(path)
            (shotname, extension) = os.path.splitext(tempfilename)
            emotion = shotname.split("_")[1].split('_')[0]
            # print(emotion)
            # usage = shotname.split("_")[1]
            pixels = getSingleFilePixels(path)
            writer.writerow([emotion, pixels])

        csvfile.close()


# ---------------------------------------

# ------------ find the label ------------
def find_label(path):
    label = -1
    if 'angry' in path:
        label = 0
    elif 'fear' in path:
        label = 1
    elif 'happy' in path:
        label = 2
    elif 'sadness' in path:
        label = 3
    elif 'neutral' in path:
        label = 4
    return str(label)


# ----------------------------------------

def dog_preprocess(path):
    # if os.path.exists(path):
    #     print("find path " + path)

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
            to_csv_data = ' '.join(map(str, pixel.flatten()))
            x = np.expand_dims(pixel, axis=0)
            x = x.reshape((-1, 100, 100, 1))
            imageList.append(x)
            return imageList, to_csv_data  # order: marked picture, input for classifier
    return None


def cat_preprocess(path):
    orig = cv2.imread(path)
    dirpath, filedir = os.path.split(path)
    print(filedir)
    filename, extend = os.path.splitext(filedir)

    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)

        # color gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect face(s)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.02,
            minNeighbors=3,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        imageList = []  # for return
        # t = datetime.datetime.now()
        for (i, (x, y, w, h)) in enumerate(faces):
            print(x,y,w,h)
            # 在猫脸区域画出方框
            # cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
            # 使用ROI获取猫脸区域图像
            roiImg = gray[int(y*0.8):y + int(h*1.2), int(x*0.8):x + int(w*1.2)]
            # roiImg = gray[y-int(h*0.8):y + int(h*1.3), x-int(h*0.8):x + int(w*1.3)]
            # 将猫脸区域图像保存成文件
            cv2.imwrite('../Data for project/test/test_save' + os.sep + filename + '.jpg', roiImg)
            # for i, d in enumerate(faces):
            #     # save coordinates
            #     x1 = max(int(d.rect.left() / ratio), 1)
            #     y1 = max(int(d.rect.top() / ratio), 1)
            #     x2 = min(int(d.rect.right() / ratio), width - 1)
            #     y2 = min(int(d.rect.bottom() / ratio), height - 1)
            #
            #     # detect landmarks
            #     shape = face_utils.shape_to_np(predictor(gray, d.rect))
            #     points = []
            #     index = 0
            #     for (x, y) in shape:
            #         x = int(round(x / ratio))
            #         y = int(round(y / ratio))
            #         index = index + 1
            #         if index == 3 or index == 4 or index == 6:
            #             points.append([x, y])
            #     points = np.array(points)  # right eye, nose, left eye

            # rotate
            # if rotation == True:
            #     xLine = points[0][0] - points[2][0]
            #     if points[2][1] < points[0][1]:
            #         yLine = points[0][1] - points[2][1]
            #         angle = math.degrees(math.atan(yLine / xLine))
            #     else:
            #         yLine = points[2][1] - points[0][1]
            #         angle = 360 - math.degrees(math.atan(yLine / xLine))
            #     rotated = imutils.rotate(orig, angle)
            #     # detectFace(rotated, picSize)

            # highlight face and landmarks
            # cv2.polylines(orig, [points], True, (0, 255, 0), 1)
            # cv2.rectangle(orig, (x1, y1), (x2, y2), (255, 0, 0), 1)
            # imageList.append(orig)

            # prepare for prediction
            # little = cv2.resize((rotated[y1:y2, x1:x2]), (img_width, img_height))  # crop and resize
            little = cv2.resize((image[y:y + h, x:x + w]), (img_width, img_height))
            pi = cv2.cvtColor(little, cv2.COLOR_BGR2GRAY)
            to_csv_data = ' '.join(map(str, pi.flatten()))
            # x = np.expand_dims(pixel, axis=0)
            # x = x.reshape((-1, 100, 100, 1))
            # imageList.append(x)
            return to_csv_data  # order: marked picture, input for classifier
    return None


# writeImage2csv("..\\Data for project\\cat\\cat_angry", "..\\test.csv")


# ----------------- rename files --------------------#
# for folders in os.listdir(path):
#     # print(folders)
#     folderPath = path + os.sep + folders
#     for folders in os.listdir(folderPath):
#         imagespath = folderPath + os.sep + folders
#         renameFile(imagespath)
# ---------------------------------------------------#


# imageList, csv_data = preprocess(testpath)
# images = [['emotion', 'pixel'], ["1", csv_data]]
# images = [find_label(testpath), preprocess(testpath)[0][1]]
# print(len(preprocess(testpath)[0][1]))


# data = pd.read_csv('../prep_images_rotated.csv')
# # data = data.sample(frac=1).reset_index(drop=True)
# print(data)


images = []
images.append(['emotion', 'pixels'])
folderPath = '../Data for project/cat'
# imagespath = '../Data for project/dog/dog_neutral'
imagespath = '../Data for project/test'
for folders in os.listdir(folderPath):
    folder = folderPath + os.sep + folders
    for image in os.listdir(folder):
        print(image)
        ipath = folder + os.sep + image
        label = find_label(ipath)
        if label != -1:
            # pixels = preprocess(ipath)
            pixels = cat_preprocess(ipath)
            if pixels is not None:
                pixel = pixels
                images.append([label, pixel])

# for image in os.listdir(imagespath):
#     print(image)
#     ipath = imagespath + os.sep + image
#     label = find_label(ipath)
#     if label != -1:
#         # pixels = preprocess(ipath)
#         pixels = cat_preprocess(ipath)
#         if pixels is not None:
#             pixel = pixels
#             images.append([label, pixel])

# csvPath = '../'
csvPath = '../result_cat_v2.csv'
if images is not None and images != []:  # found face on image
    images = pd.DataFrame(images)
    # with open(csvPath + 'result.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['emotion', 'pixels'])
    images.to_csv(csvPath, header=False, index=False)
