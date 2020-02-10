import os

import cv2
import dlib
import pandas as pd
from helper import No_Preprocessing

# image size for prediction
img_width = 160
img_height = 160
# scale factor for preprocessing
picSize = 320
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

# helper class
helper = No_Preprocessing(img_width, img_height)


# ------------ find the label ------------
def find_label(path):
    label = -1
    if 'Angry' in path:
        label = 0
    elif 'Scared' in path:
        label = 1
    elif 'Happy' in path:
        label = 2
    elif 'Sadness' in path:
        label = 3
    elif 'Neutral' in path:
        label = 4
    return str(label)


# ----------------------------------------


def preprocess(path, savePath):
    orig = cv2.imread(path)
    dirpath, filedir = os.path.split(path)
    filename, extend = os.path.splitext(filedir)

    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)

        imageList = []  # for return
        # t = datetime.datetime.now()
        for (i, (x, y, w, h)) in enumerate(faces):
            print(x, y, w, h)
            # draw a rectangle on cats' faces
            # cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
            # larger area to include the ears of cats
            roiImg = gray[int(y * 0.75):y + int(h * 1.25), int(x * 0.75):x + int(w * 1.25)]
            # roiImg = gray[y-int(h*0.8):y + int(h*1.3), x-int(h*0.8):x + int(w*1.3)]

            # cv2.imwrite(savePath + os.sep + filename + '.jpg', roiImg)
            # prepare for prediction
            # little = cv2.resize((rotated[y1:y2, x1:x2]), (img_width, img_height))  # crop and resize
            little = cv2.resize((image[y:y + h, x:x + w]), (img_width, img_height))
            pi = cv2.cvtColor(little, cv2.COLOR_BGR2GRAY)
            to_csv_data = ' '.join(map(str, pi.flatten()))
            return to_csv_data
    return None


# writeImage2csv("..\\Data for project\\cat\\cat_angry", "..\\test.csv")


# --------define dog or cat to classify--------
classify = 'dog'

images = []
images.append(['emotion', 'pixels'])
folderPath = '..' + os.sep + 'Data for project' + os.sep + classify
savePath = '..\\Data for project\\' + classify
# imagespath = '../Data for project/dog/dog_neutral'
imagespath = '../Data for project/test'

if os.path.exists(savePath):
    print("path found: " + savePath)
else:
    os.mkdir(savePath)
    print("create path: " + savePath)

for folders in os.listdir(folderPath):
    folder = folderPath + os.sep + folders
    for image in os.listdir(folder):
        print(image)
        ipath = folder + os.sep + image
        label = find_label(ipath)
        pixel = None
        if classify == 'dog':
            pixels = dog_preprocess(ipath, savePath)
        else:
            pixels = cat_preprocess(ipath, savePath)
        if label != -1 and pixels is not None:
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

csvPath = '..\\result_' + classify + '_V3' + '.csv'
if images is not None and images != []:  # found face on image
    images = pd.DataFrame(images)
    # with open(csvPath + 'result.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['emotion', 'pixels'])
    images.to_csv(csvPath, header=False, index=False)
