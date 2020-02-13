import os
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import const
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
keras = tf.keras

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

        prediction = model.predict(img)
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

        d = {'emotion': ['Angry', 'Scared', 'Happy', 'Sad', 'Neutral'], 'prob': prediction[0]}
        df = pd.DataFrame(d, columns=['emotion', 'prob'])

        return df


def renameFile(path):
    """
    rename non-jpg file to jpg with No.
    :param path: data folder path
    """
    print('come into path:' + path)
    fileList = os.listdir(path)
    for file in fileList:
        filepath, file = os.path.split(file)
        filename, extend = os.path.splitext(file)
        oldfilename = path + os.sep + file
        newfilename = path + os.sep + filename + '.jpg'
        os.rename(oldfilename, newfilename)
        print(oldfilename + ' -> ' + newfilename)
    print("done")


def get_Classify(classify):
    """
    :param classify: cat or dog
    :return: two data path
    """
    if classify == 'cat':
        train_data = const.CAT_TRAIN_DATA
        validation_data = const.CAT_VALID_DATA
    elif classify == 'dog':
        train_data = const.DOG_TRAIN_DATA
        validation_data = const.DOG_VALID_DATA
    else:
        train_data = None
        validation_data = None
        print("by now, we only support dog and cat, please try 'cat' and 'dog' ")
    if train_data != None:
        return load_data(train_data, validation_data)
    else:
        return None



def MobileNetV2():
    """
    :return: pre-trained MobileNetV2 model imported from tf.keras.application and add transfer learning layer
    """
    base_model = tf.keras.applications.MobileNetV2(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False
    base_model.summary()
    global_average_layer = keras.layers.GlobalAveragePooling2D()
    output_layer = keras.layers.Dense(5, activation='sigmoid')
    model = keras.Sequential([
        base_model,
        global_average_layer,
        output_layer
    ])
    return model


def Xception():
    base_model = tf.keras.applications.Xception(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                include_top=False,
                                                weights='imagenet')
    base_model.trainable = False
    base_model.summary()
    global_average_layer = keras.layers.GlobalAveragePooling2D()
    output_layer = keras.layers.Dense(5, activation='sigmoid')
    model = keras.Sequential([
        base_model,
        global_average_layer,
        output_layer
    ])
    return model


def InceptionResNetV2():
    base_model = tf.keras.applications.InceptionResNetV2(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                         include_top=False,
                                                         weights='imagenet')
    base_model.trainable = False
    base_model.summary()
    global_average_layer = keras.layers.GlobalAveragePooling2D()
    output_layer = keras.layers.Dense(5, activation='sigmoid')
    model = keras.Sequential([
        base_model,
        global_average_layer,
        output_layer
    ])
    return model


def InceptionV3():
    base_model = tf.keras.applications.InceptionV3(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False
    base_model.summary()
    global_average_layer = keras.layers.GlobalAveragePooling2D()
    output_layer = keras.layers.Dense(5, activation='sigmoid')
    model = keras.Sequential([
        base_model,
        global_average_layer,
        output_layer
    ])
    return model


def VGG19():
    base_model = tf.keras.applications.VGG19(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False
    base_model.summary()
    global_average_layer = keras.layers.GlobalAveragePooling2D()
    output_layer = keras.layers.Dense(5, activation='sigmoid')
    model = keras.Sequential([
        base_model,
        global_average_layer,
        output_layer
    ])
    return model


def create_model(modelName='MobileNetV2'):
    """
    create one of four models
    :param modelName:
    :return: Model
    """
    if 'Mobile' in modelName:
        return MobileNetV2(), modelName
    elif 'Xception' in modelName:
        return Xception(), modelName
    elif 'InceptionV3' in modelName:
        return InceptionV3(), modelName
    elif 'InceptionResNet' in modelName:
        return InceptionResNetV2(), modelName
    else:
        print('error, no such a model')
        return None, None


def load_data(trainPath, validationPath):
    """
    load training and validation data by ImageDataGenerator iterator
    :param trainPath: train data folders path
    :param validationPath: validation data folders path
    :return: two data_generators and steps_per_epoch
    """
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        trainPath,
        target_size=const.IMG_SHAPE,
        batch_size=const.BATCH_SIZE,
        class_mode='categorical',
        classes=['Angry', 'Happy', 'Neutral', 'Sadness', 'Scared']
    )

    validation_generator = train_datagen.flow_from_directory(
        validationPath,
        target_size=const.IMG_SHAPE,
        batch_size=const.BATCH_SIZE,
        class_mode='categorical',
        classes=['Angry', 'Happy', 'Neutral', 'Sadness', 'Scared']
    )
    steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size)
    # steps_per_valid = np.ceil(validation_generator.samples / validation_generator.batch_size)
    return train_generator, validation_generator, steps_per_epoch


def plotInfo(model_path, modelName, history):
    """
    summarize model history for loss and accuracy
    """
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(model_path + modelName + ' loss.png', dpi=300)

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(model_path + modelName + ' loss.png', dpi=300)
