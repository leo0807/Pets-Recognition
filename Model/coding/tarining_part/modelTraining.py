import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from helper import No_Preprocessing
import helper
from keras import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, BatchNormalization, AveragePooling2D, Activation
from keras.optimizers import SGD
from keras.regularizers import l2
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

keras = tf.keras

# size of images
img_width = 200
img_height = 200
# path for results
model_path = "../../models/"




# # read image csv
# csvPath = '../../result_cat_V3.csv'
#
# pathdir, file = os.path.split(csvPath)
# filename = os.path.splitext(file)[0]
# data = pd.read_csv(csvPath)
# data = data.sample(frac=1).reset_index(drop=True)
#
# # print some information
# print('Different emotional states: ' + str(np.unique(data.emotion)))
# print("Number of Examples for both states")
# print(data.emotion.value_counts())


# # pixel array is an ndarray containing all pixels of each image
# helper = No_Preprocessing(img_width, img_height)
# pixels = helper.extract_and_prepare_pixels(data[['pixels']])
#
# x = pixels
# x = x.reshape((-1, 100, 100, 1))
# y = to_categorical(data.emotion.reset_index(drop=True))
#
# # build train/test datasets
# x_shuffle, y_shuffle = shuffle(x, y)  # Mix samples
# x_train, x_test, y_train, y_test = train_test_split(x_shuffle, y_shuffle,
#                                                     test_size=0.1)  # split for train and test block
#
# # train on all
# # x_train = x_shuffle
# # y_train = y_shuffle
#
# # plot part of the set
# fig, ax = plt.subplots(5, 5, figsize=(7, 7))
# j = -1
# k = 0
# for i in range(0, 25):
#     if i % 5 == 0:
#         j += 1
#         k = 0
#     print(pixels[i])
#     ax[j, k].imshow(pixels[i].reshape(100, 100), cmap="gray", interpolation='nearest')
#     ax[j, k].set_title(y[i])
#     ax[j, k].axis('off')
#     k += 1
# plt.savefig(model_path + 'exampleInput.png', dpi=300)
# ---------------------------------------------------------------------------------------


# model = helper.create_model()
base_model = tf.keras.applications.MobileNetV2(input_shape=(img_height, img_width, 3),
                                               include_top=False,
                                               weights='imagenet')
base_model.trainable = False
base_model.summary()
global_average_layer = keras.layers.GlobalAveragePooling2D()
output_layer = keras.layers.Dense(5, activation='sigmoid')

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        '../../../../transfer learning/Data for project/cat/train',
        target_size=(img_height, img_width),
        batch_size=32,
        # class_mode='binary'
)

validation_generator = train_datagen.flow_from_directory(
        '../../../../transfer learning/Data for project/cat/test',
        target_size=(img_height, img_width),
        batch_size=32,
        # class_mode='binary'
)

model = keras.Sequential([
    base_model,
    global_average_layer,
    output_layer
])
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='binary_crossentropy',
              metrics=['accuracy'])


import numpy as np
steps_per_epoch = np.ceil(train_generator.samples/train_generator.batch_size)
setp_per_vali = np.ceil(validation_generator.samples/validation_generator.batch_size)
history = model.fit_generator(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=5,
        validation_data=validation_generator)

model.save('../../models/' + 'cat' + 'mobileNetV2.h5')


# origin code
# history = model.fit(x_train, y_train, validation_split=0.2, epochs=2, batch_size=16)
#
# scores = model.evaluate(x_test, y_test)
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

# save trained classifier
# model.save(model_path + 'Cat_classifier_mobileNet' + '_v1' + '.h5')

# ---------------------------------------------------------------------------------------
# plotting

# summarize history for accuracy
plt.close()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(model_path + os.sep + filename + 'accuracy.png', dpi=300)

# summarize history for loss
plt.close()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig(model_path + os.sep + filename + 'loss.png', dpi=300)
