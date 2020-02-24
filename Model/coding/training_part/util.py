import numbers
import os
import matplotlib.pyplot as plt
import pycm
import tensorflow as tf
import const
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

keras = tf.keras


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


def get_Classify(classify, face=True):
    """
    :param classify: cat or dog
    :return: two data path
    """
    if classify == 'cat':
        train_data = const.CAT_TRAIN_DATA
        if face:
            validation_data = const.CAT_VALID_DATA_FACE
            test_data = const.CAT_VALID_DATA_FACE
        else:
            validation_data = const.CAT_VALID_DATA
            test_data = const.CAT_VALID_DATA
    elif classify == 'dog':
        train_data = const.DOG_TRAIN_DATA
        if face:
            validation_data = const.DOG_VALID_DATA_FACE
            test_data = const.DOG_VALID_DATA_FACE
        else:
            validation_data = const.DOG_VALID_DATA
            test_data = const.DOG_VALID_DATA
    else:
        train_data = None
        validation_data = None
        test_data = None
        print("by now, we only support dog and cat, please try 'cat' and 'dog' ")
    if train_data is not None:
        return load_data(train_data, validation_data, test_data)
    else:
        return None


# return base_model
def MobileNetV2():
    """
    :return: pre-trained MobileNetV2 model imported from tf.keras.application and add transfer learning layer
    """
    base_model = tf.keras.applications.MobileNetV2(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    return base_model


def Xception():
    """

    :return:  Xception model
    """
    base_model = tf.keras.applications.Xception(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                include_top=False,
                                                weights='imagenet')
    return base_model


def InceptionResNetV2():
    """

    :return: InceptionResNetV2 model
    """
    base_model = tf.keras.applications.InceptionResNetV2(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                         include_top=False,
                                                         weights='imagenet')
    return base_model


def InceptionV3():
    """

    :return: InceptionV3 model
    """
    base_model = tf.keras.applications.InceptionV3(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    return base_model


def VGG19():
    """

    :return: VGG19 model
    """
    base_model = tf.keras.applications.VGG19(input_shape=(const.IMG_HEIGHT, const.IMG_WIDTH, 3),
                                             include_top=False, weights='imagenet', classes=5)
    return base_model


def create_model(modelName='VGG19', connected=False, dropout=0,
                 dense=1024, BN=False, AveragePooling=True, MutiFC = False):
    """
    create one of four models
    :param modelName:
    :return: Model
    """
    if 'Mobile' in modelName:
        base_model = MobileNetV2()
    elif 'Xception' in modelName:
        base_model = Xception()
    elif 'InceptionV3' in modelName:
        base_model = InceptionV3()
    elif 'InceptionResNet' in modelName:
        base_model = InceptionResNetV2()
    elif 'VGG19' in modelName:
        base_model = VGG19()
    else:
        print('error, no such a model')
        base_model = None
    # if base_model exists, add different layers
    if base_model is not None:
        base_model.trainable = False
        # base_model.summary()

        # averagePooling layer
        global_layer = keras.layers.GlobalAveragePooling2D()

        # BN layer
        batch_normalization = keras.layers.BatchNormalization()

        # fully-connected layers
        x = keras.layers.Dense(dense, activation='relu')

        # multiple fuly-connected layer
        MutiFC_1 = keras.layers.Dense(dense, activation='relu')
        MutiFC_2 = keras.layers.Dense(dense, activation='relu')
        MutiFC_3 = keras.layers.Dense(dense/2, activation='relu')

        # dropout layers
        y = keras.layers.Dropout(dropout)

        # predict layer
        output_layer = keras.layers.Dense(5, 'softmax')

        model = keras.Sequential()
        model.add(base_model)

        if AveragePooling:
            model.add(global_layer)
        if BN:
            model.add(batch_normalization)
        model.add(y)
        if MutiFC:
            model.add(MutiFC_1)
            model.add(MutiFC_2)
            model.add(MutiFC_3)
            connected = False
        if connected:
            model.add(x)
        model.add(output_layer)

        return model, modelName
    else:
        return None, None


def load_data(trainPath, validationPath, testPath):
    """
    load training and validation data by ImageDataGenerator iterator
    :param trainPath: train data folders path
    :param validationPath: validation data folders path
    :return: two data_generators and steps_per_epoch
    """
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        # rotation_range=0.2,
        # height_shift_range=0.1,
        # width_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        # brightness_range=[0.7, 1.3],
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        trainPath,
        target_size=const.IMG_SHAPE,
        batch_size=const.BATCH_SIZE,
        class_mode='categorical',
        classes=['Angry', 'Happy', 'Neutral', 'Sad', 'Scared']
    )

    validation_generator = test_datagen.flow_from_directory(
        validationPath,
        target_size=const.IMG_SHAPE,
        batch_size=const.BATCH_SIZE,
        class_mode='categorical',
        classes=['Angry', 'Happy', 'Neutral', 'Sad', 'Scared']
    )

    test_generator = test_datagen.flow_from_directory(
        validationPath,
        target_size=const.IMG_SHAPE,
        batch_size=128,
        class_mode='categorical',
        classes=['Angry', 'Happy', 'Neutral', 'Sad', 'Scared']
    )
    steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size)
    return train_generator, validation_generator, test_generator, steps_per_epoch


def y_list_to_single(y_list):
    return np.asarray(list(map(np.argmax, y_list)))


def get_confusion_matrix(y_predicted, y_actual):
    if len(y_predicted) > 0 and len(y_actual) > 0:
        if not isinstance(y_actual[0], numbers.Number):
            y_actual = y_list_to_single(y_actual)
        if not isinstance(y_predicted[0], numbers.Number):
            y_predicted = y_list_to_single(y_predicted)
        return pycm.ConfusionMatrix(actual_vector=y_actual, predict_vector=y_predicted)
    else:
        return None


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
    plt.savefig(model_path + modelName + ' accuracy.png', dpi=300)

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(model_path + modelName + ' loss.png', dpi=300)


def show_predict_report(DataGenerator):
    model = keras.models.load_model(const.TRAINED_MODEL)
    imgs, labels = DataGenerator.next()

    from sklearn.metrics import classification_report
    import numpy as np

    Y_test = np.argmax(labels, axis=1)  # Convert one-hot to index
    y_pred = model.predict_classes(imgs)
    print(classification_report(Y_test, y_pred))

