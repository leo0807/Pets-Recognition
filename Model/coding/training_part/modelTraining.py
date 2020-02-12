import tensorflow as tf
from coding.training_part import util
from coding.training_part import const

keras = tf.keras


def train(classify, model):
    # classify = 'cat'  # by now only support 'cat' or 'dog'
    train_data, validation_data = util.get_Classify(classify)
    # load training and validation data
    train_generator, validation_generator, steps_per_epoch = util.load_data(train_data, validation_data)
    # load pre-trained model from keras.application
    model, modelName = util.create_model(model)
    # compile model
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # fit the model
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=40,
        validation_data=validation_generator)

    # save model
    modelPath = classify + ' ' + modelName
    model.save(const.MODEL_PATH + modelPath + '.h5')

    # save model history to csv for further analyse
    history.history.to_csv(const.MODEL_PATH + modelPath + '.csv')

    # summarize history for accuracy & loss
    util.plotInfo(const.MODEL_PATH, modelPath, history)


# ------------------------------------------------------------------
if __name__ == "__main__":
    train('cat', 'MobileNetV2')
