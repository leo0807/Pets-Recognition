import os
import time

import cv2
import dlib
import pandas as pd

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
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + pathCat)
detector = dlib.cnn_face_detection_model_v1(pathDet)


def find_label(path):
    """
    find the label of the images
    :param path:
    :return:
    """
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
    """
    create the path if there is no directory exists
    :param savePath:
    :return:
    """
    if os.path.exists(savePath):
        pass
        # print("path found: " + savePath)
    else:
        os.mkdir(os.path.abspath(savePath))
        print("create path: " + savePath)


def write2csv(csvPath, images):
    if images is not None and images != []:  # found face on image
        images = pd.DataFrame(images)
        images.to_csv(csvPath, header=False, index=False)


def saveImage(savePath, folderName, saveImage, little):
    checkPath(savePath + folderName)
    cv2.imwrite(saveImage, little)
    print('saved: ', saveImage)


def splitPath(imagePath):
    """
    :param imagePath:
    :return: image name and the folder name
    """
    dirpath, filedir = os.path.split(imagePath)
    filename, extend = os.path.splitext(filedir)
    folderName = dirpath.split(os.sep)[-1]
    return filename, folderName


def PetProcess(Pet, imagePath, savePath):
    """
    process Pet's image
    :param Pet: cat & dog
    :param imagePath:
    :param savePath:
    :return: pixels in RGB channels of cats' or dogs' faces
    """
    orig = cv2.imread(imagePath)
    filename, folderName = splitPath(imagePath)
    saveimgPath = savePath + folderName + os.sep + filename + '.jpg'
    if not orig is None:
        # resize
        height, width, channels = orig.shape  # read size
        ratio = picSize / height
        image = cv2.resize(orig, None, fx=ratio, fy=ratio)
        # color gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if Pet == 'cat':
            if not os.path.exists(saveimgPath):
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.05,
                    minNeighbors=3,
                    minSize=(60, 60),
                    # flags=cv2.CASCADE_DO_ROUGH_SEARCH
                )
                for (i, (x, y, w, h)) in enumerate(faces):
                    print(x, y, w, h)
                    # prepare for prediction
                    little = cv2.resize(image[y:y + h, x:x + w], (img_width, img_height))
                    saveImage(savePath, folderName, filename, little)
                    return little.flatten()
            else:
                pass
        elif Pet == 'dog':
            if not os.path.exists(saveimgPath):
                start = time.time()
                dets = detector(gray, upsample_num_times=1)
                print('detection time:', time.time() - start)

                for i, d in enumerate(dets):
                    # save coordinates
                    x1 = max(int(d.rect.left()), 1)
                    y1 = max(int(d.rect.top()), 1)
                    x2 = min(int(d.rect.right()), width - 1)
                    y2 = min(int(d.rect.bottom()), height - 1)
                    print(i, x1, y1, x2, y2)
                    if i != 0:
                        try:
                            little = cv2.resize(image[y1:y2, x1:x2], (img_width, img_height))
                            saveImage(savePath, folderName, filename + str(i), little)
                            return little.flatten()
                        except:
                            pass
                    else:
                        try:
                            little = cv2.resize(image[y1:y2, x1:x2], (img_width, img_height))
                            saveImage(savePath, folderName, filename, little)
                            return little.flatten()
                        except:
                            pass
            else:
                pass
        else:
            print('error, we only support cat and dog images preprocess')
            return None

        # detect face(s)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(60, 60),
        )
        for (i, (x, y, w, h)) in enumerate(faces):
            print(x, y, w, h)
            # prepare for prediction
            little = cv2.resize(image[y:y + h, x:x + w], (img_width, img_height))
            # checkPath(savePath + folderName)
            cv2.imwrite(savePath + folderName + os.sep + filename + '.jpg', little)
            return little.flatten()
    return None


# --------define dog or cat to classify--------
if __name__ == '__main__':

    classify = 'dog'

    images = [['emotion', 'pixels']]
    folderPath = '../../../../Data for project' + os.sep + classify
    savePath = '../../../../Data for project/new/' + classify + os.sep

    for folders in os.listdir(folderPath):
        folder = folderPath + os.sep + folders
        for image in os.listdir(folder):
            print(image)
            ipath = folder + os.sep + image
            label = find_label(ipath)
            pixels = PetProcess(classify, ipath, savePath)
            if label != -1 and pixels is not None:
                pixel = pixels
                images.append([label, pixel])

    csvPath = '../../csv/' + classify + 'all_data' + '_V1' + '.csv'
    write2csv(csvPath, images)
