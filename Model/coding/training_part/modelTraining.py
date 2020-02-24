import os

import tensorflow as tf
import util
import const
import pandas as pd
from multiprocessing import Process

keras = tf.keras


def train(classify, model, version, save=True, csv=True, plot=True,
          connected=True, dropout=0.0, dense=4096, load_model=False, BN=False, AveragePooling=True, MutiFC=False,
          test_face=True):
    """
    training code for pet(cat and dog) emotion
    :param classify: cat or dog
    :param model: the name of pre-trained model
    :param version: the current version
    :param plot: decide if need to plot & save images of acc and loss
    :param csv: if save the history to csv
    :param save: if save the model
    """
    # classify = 'cat'  # by now only support 'cat' or 'dog'
    tf.keras.backend.clear_session()

    # load pre-trained model from keras.application
    train_generator, validation_generator, test_generator, steps_per_epoch = util.get_Classify(classify, test_face)

    # create model
    model, modelName = util.create_model(model, connected, dropout, dense, BN, AveragePooling, MutiFC)

    # file name for model
    modelPath = classify + os.sep + modelName + version

    # compile model
    model.compile(optimizer=const.MODEL_OPTIMISER,
                  loss=const.MODEL_LOSS,
                  metrics=['accuracy'])
    model.summary()
    print('Now is running: ', classify, ' ', version)

    # fit data
    if not load_model:
        # add tensorboard log save_path
        log_dir = const.LOG_PATH + modelPath
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        # fit the model
        history = model.fit(train_generator, steps_per_epoch=steps_per_epoch, epochs=const.EPOCH,
                            validation_data=validation_generator, workers=4,
                            # callbacks=[tensorboard_callback]
                            )
    else:
        # show classification report on predicting
        util.show_predict_report(test_generator)

    # save model history to csv for further analyse
    if csv:
        pd.DataFrame(history.history).to_csv(const.CSV_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    if plot:
        util.plotInfo(const.PLOT_PATH, modelPath, history)

    # save model
    if save:
        try:
            model.save(const.MODEL_PATH + modelPath + '.h5')
        except OSError:
            # I found a bug in saving model with tf. it shows os error but it did save model
            print("OSError, is it saved? ")
            pass

    # show each class report
    y_actual = validation_generator.classes
    y_predicted = model.predict(validation_generator)
    test_result = model.evaluate(validation_generator)
    class_ = util.get_confusion_matrix(y_actual=y_actual, y_predicted=y_predicted)
    print(class_)
    print("test result- accuracy:", test_result[1])


# ------------------------------------------------------------------
if __name__ == "__main__":
    Dog = 'dog'
    Cat = 'cat'
    tf.keras.backend.clear_session()

    # train(Dog, 'Xception', '_FC2048_BN_Face', dense=2048, BN=True)
    # train(Dog, 'VGG19', '_FC2048_BN_Face', dense=2048,BN=True)
    # train(Dog, 'MobileNet', '_FC2048_BN_Face', dense=2048,BN=True)
    # train(Dog, 'InceptionResNet', '_FC2048_BN_Face', dense=2048, BN=True)
    # train(Dog, 'Xception', '_FC4096_BN_Face_dp000', dense=1024, BN=True,)
    # train(Dog, 'Xception', '_FC4096_BN_Face_dp050', dense=512, BN=True,)
    # train(Cat, 'Xception', '_FC2048_BN_Face', dense=2048, BN=True)
    # train(Dog, 'VGG19', '_FC2048_BN_Face', dense=2048, BN=True)
    # train(Cat, 'MobileNet', '_FC2048_BN_Face', dense=2048, BN=True)
    # train(Cat, 'InceptionResNet', '_FC2048_BN_Face', dense=2048, BN=True)
    train(Dog, 'Xception', 'Face_BN_FC2048', dense=2048, BN=True)
    train(Cat, 'VGG19', 'Face_BN_FC2048', dense=2048, BN=True)
