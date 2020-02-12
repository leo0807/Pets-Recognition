import os
import cv2
import dlib
import numpy as np
import pandas as pd
import imutils
import math

# image size for prediction
img_width = 100
img_height = 100
# scale factor for preprocessing
picSize = 200
rotation = True

# face detector
pathDet = 'Emotion_Dog/dogHeadDetector.dat'
pathCat = "Emotion_Cat/haarcascade_frontalcatface.xml"

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)
detector = dlib.cnn_face_detection_model_v1(pathDet)


class No_Preprocessing:

    def __init__(self, img_width, img_height):
        self.img_width = img_width
        self.img_height = img_height

    def extract_and_prepare_pixels(self, pixels):
        """
        Takes in a string (pixels) that has space separated integer values and returns an array which includes the
        pixels for all images.
        """
        pixels_as_list = [item[0] for item in pixels.values.tolist()]
        np_image_array = []
        for index, item in enumerate(pixels_as_list):
            # split space separated ints
            pixel_data = item.split()
            img_size_row = img_size_col = 256
            if len(pixel_data) % 490 == 0:
                img_size_row = 490
                img_size_col = 640
            elif len(pixel_data) == 10000:
                img_size_row = img_size_col = 100

            data = np.zeros((img_size_row, img_size_col), dtype=np.uint8)

            # Loop through rows
            for i in range(0, img_size_row):
                try:
                    # (0 = 0), (1 = 47), (2 = 94), ...
                    pixel_index = i * img_size_col
                    # (0 = [0:47]), (1 = [47: 94]), (2 = [94, 141]), ...
                    data[i] = pixel_data[pixel_index:pixel_index + img_size_col]
                except:
                    pass

            np_image_array.append(np.array(data))
        np_image_array = np.array(np_image_array)
        return np_image_array

    def predict_emotion(self, model, img):
        """
        Use a trained model to predict emotional state
        """

        emotion = 'None'

        prediction = model.predict(img)[0]
        # ->
        prediction = [round(x * 100, 2) for x in prediction]
        print(prediction)
        prediction_ = np.argmax(prediction)

        if prediction_ == 0:
            emotion = 'Angry'
        elif prediction_ == 1:
            emotion = 'Scared'
        elif prediction_ == 2:
            emotion = 'Happy'
        elif prediction_ == 3:
            emotion = 'Sad'
        elif prediction_ == 4:
            emotion = 'Neutral'

        d = {'emotion': ['Angry', 'Scared', 'Happy', 'Sad', 'Neutral'], 'prob': prediction}
        df = pd.DataFrame(d, columns=['emotion', 'prob']).sort_values(by=['prob'], ascending=False)
        df.prob = [str(x) + '%' for x in df.prob]
        return df


def dog_preprocess(path):
    # read image from path
    orig = cv2.imread(path)
    dirpath, filedir = os.path.split(path)
    filename, extend = os.path.splitext(filedir)

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

            # # detect landmarks
            # shape = face_utils.shape_to_np(predictor(gray, d.rect))
            # points = []
            # index = 0
            # for (x, y) in shape:
            #     x = int(round(x / ratio))
            #     y = int(round(y / ratio))
            #     index = index + 1
            #     if index == 3 or index == 4 or index == 6:
            #         points.append([x, y])
            # points = np.array(points)  # right eye, nose, left eye

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

            imageList.append(orig)
            print(x1, x2, y1, y2)

            # prepare for prediction
            little = cv2.resize(gray[y1:y2, x1:x2], (img_width, img_height))  # crop and resize
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
            roiImg = gray[y:y + h, x:x + w]
            # prepare for prediction
            little = cv2.resize((image[y:y + h, x:x + w]), (img_width, img_height))
            pi = cv2.cvtColor(little, cv2.COLOR_BGR2GRAY)
            to_csv_data = ' '.join(map(str, pi.flatten()))
            return to_csv_data
    return None


def renameFile(path):
    print('come into path:' + path)
    fileList = os.listdir(path)
    for file in fileList:
        oldfilename = path + os.sep + file
        newfilename = path + os.sep + file[:-4] + '.jpg'
        os.rename(oldfilename, newfilename)
        print(oldfilename + ' -> ' + newfilename)
    print("done")
