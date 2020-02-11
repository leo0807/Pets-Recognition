import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Conv2D, BatchNormalization, Activation, AveragePooling2D, Dropout
from keras.optimizers import SGD


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
    print('come into path:' + path)
    fileList = os.listdir(path)
    for file in fileList:
        oldfilename = path + os.sep + file
        newfilename = path + os.sep + file[:-4] + '.jpg'
        os.rename(oldfilename, newfilename)
        print(oldfilename + ' -> ' + newfilename)
    print("done")


# ---------------------------------------------------------------------------------------

def create_model():
    model = Sequential()

    model.add(Conv2D(filters=16, kernel_size=(3, 3), input_shape=(100, 100, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=16, kernel_size=(7, 7), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Flatten())
    model.add(Dense(160, activation='relu', kernel_regularizer=l2(0.1)))
    model.add(Dense(80, activation='relu'))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(5, activation='softmax'))

    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=["accuracy"])

    return model

# ---------------------------------------------------------------------------------------
