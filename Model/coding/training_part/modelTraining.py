import tensorflow as tf
import util
import const
import pandas as pd

keras = tf.keras

train_generator, validation_generator, steps_per_epoch = util.get_Classify('cat')


def train(classify, model, version, train_generator, validation_generator, steps_per_epoch,
          save=True, csv=True, plot=True):
    """
    training code for pet(cat and dog) emotion

    :param steps_per_epoch: step per epoch
    :param validation_generator: test data iterator
    :param train_generator: train data iterator
    :param classify: cat or dog
    :param model: the name of pre-trained model
    :param version: the current version
    :param plot: decide if need to plot & save images of acc and loss
    :param csv: if save the history to csv
    :param save: if save the model
    """
    # classify = 'cat'  # by now only support 'cat' or 'dog'

    # load pre-trained model from keras.application
    model, modelName = util.create_model(model)
    # compile model
    model.compile(optimizer=const.MODEL_OPTI,
                  loss=const.MODEL_LOSS,
                  metrics=['accuracy'])
    # fit the model
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=40,
        validation_data=validation_generator)

    modelPath = classify + ' ' + modelName + version
    # save model
    if save:
        model.save(const.MODEL_PATH + modelPath + '.h5')

    # save model history to csv for further analyse
    if csv:
        pd.DataFrame(history.history).to_csv(const.MODEL_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    if plot:
        util.plotInfo(const.MODEL_PATH, modelPath, history)


# ------------------------------------------------------------------
if __name__ == "__main__":
    train('cat', 'MobileNetV2', '_v1', train_generator, validation_generator, steps_per_epoch, plot=False)
