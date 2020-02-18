import tensorflow as tf
import util
import const
import pandas as pd
from multiprocessing import Process

keras = tf.keras


def train(classify, model, version, save=True, csv=True, plot=True,
          connected=False, dropout=False, dense=1024, load_model=False,BN=False):
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

    # load pre-trained model from keras.application
    print('now is running: ', classify, ' ', model, ' ', version)
    train_generator, validation_generator, test_generator, steps_per_epoch = util.get_Classify(classify)
    model, modelName = util.create_model(model, connected, dropout, dense)
    # compile model

    model.compile(optimizer=const.MODEL_OPTIMISER,
                  loss=const.MODEL_LOSS,
                  metrics=['mae', 'accuracy'])
    if not load_model:
        # fit the model
        history = model.fit_generator(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=const.EPOCH,
            validation_data=validation_generator,
        )
    else:
        model = keras.models.load_model(const.TRAINED_MODEL)
        imgs, labels = test_generator.next()

        from sklearn.metrics import classification_report
        import numpy as np

        Y_test = np.argmax(labels, axis=1)  # Convert one-hot to index
        y_pred = model.predict_classes(imgs)
        print(classification_report(Y_test, y_pred))

    modelPath = classify + '_' + modelName + version

    # save model history to csv for further analyse
    if csv:
        pd.DataFrame(history.history).to_csv(const.MODEL_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    if plot:
        util.plotInfo(const.MODEL_PATH, modelPath, history)

    # save model
    if save:
        model.save(const.MODEL_PATH + modelPath + '.h5')


# ------------------------------------------------------------------
if __name__ == "__main__":
    Pet = 'cat'
    # version = '_v2_3layers'
    tf.keras.backend.clear_session()
    # train(Pet, 'Xception', '_v3_connected4096', plot=False, connected=True,
    #       dropout=False, dense=4096, load_model=False)
    VGG19 = Process(target=train(Pet, 'VGG19', '_v3_connected4096_BN',
                                plot=False, connected=True, dropout=False, dense=4096))
    VGG19.start()
    VGG19.join()
    VGG191 = Process(target=train(Pet, 'VGG19', '_v3_connected4096_MaxPooling',
                                  plot=False, connected=True, dropout=False, dense=4096))
    VGG191.start()
    VGG191.join()

