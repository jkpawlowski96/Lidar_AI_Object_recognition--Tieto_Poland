from keras.models import Sequential
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.layers import Dense,Dropout, Flatten, Convolution1D
from keras import optimizers
from sklearn.model_selection import StratifiedKFold
import numpy as np
from keras.utils import np_utils
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D


def data_conv(x_data):
    size = np.shape(x_data)[1]
    x_data = x_data.reshape(x_data.shape[0], size, 1).astype('float32')
    return x_data


def teach_nn(x_data, y_data, layers, recursive=False, learning_rate=0.05, optimizer='sgd', epochs=100, activation='relu', batch=50):
    model = Sequential()

    look_back = 1
    size_nn = np.shape(x_data)[1]

    if recursive:
        x_data = np.reshape(x_data, (x_data.shape[0], 1, x_data.shape[1]))
        print(x_data.shape[0:])
        model.add(LSTM(units=layers[0], return_sequences = True, activation='tanh', input_shape=(look_back,size_nn)))
        for layer in layers[1:]:
            model.add(LSTM(units=layer, return_sequences = True, activation=activation))
            model.add(Dropout(0.2))
    else:
        model.add(Dense(units=layers[0], activation=activation, input_dim=size_nn))
        for layer in layers[1:]:
            model.add(Dense(units=layer, activation=activation))

    model.add(Dense(units=2, activation='softmax'))

    if optimizer == 'sgd':
        opt = optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    if optimizer == 'adam':
        opt = optimizers.SGD(lr=learning_rate, clipnorm=1.)
    if recursive:
        model.compile(opt, loss='binary_crossentropy', metrics=['accuracy'])
    else:
        model.compile(opt, loss='categorical_crossentropy', metrics=['accuracy'])
    folds = StratifiedKFold(n_splits=10, shuffle=True, random_state=0).split(x_data, y_data)
    for fold in folds:
        X_train_cv = x_data[fold[0]]
        y_train_cv = y_data[fold[0]]
        X_valid_cv = x_data[fold[1]]
        y_valid_cv = y_data[fold[1]]
        if recursive:
            y_train_cv = np.reshape( y_train_cv, ( y_train_cv.shape[0], 1,  1))
            y_valid_cv = np.reshape(  y_valid_cv, (  y_valid_cv.shape[0], 1,  1))
        y_train_cv = np_utils.to_categorical(y_train_cv)
        y_valid_cv = np_utils.to_categorical(y_valid_cv)
        print(y_train_cv.shape[0:])
        model.fit(
            x=X_train_cv,
            y=y_train_cv,
            batch_size=batch,
            epochs=epochs,
            shuffle=True,
            verbose=True,
            validation_data=(X_valid_cv, y_valid_cv),
            )

    return model


def teach_conv_nn(x_data, y_data, layers=[100, 100], kernel=12, learning_rate=0.05, optimizer='sgd', epochs=200, batch=32):


    size = np.shape(x_data)[1]

    num_classes = 2

    x_data = data_conv(x_data)

    model = Sequential()

    if optimizer == 'sgd':
        opt = optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    if optimizer == 'adam':
        opt = optimizers.SGD(lr=learning_rate, clipnorm=1.)

    model.add(Conv1D(filters=layers[0], kernel_size=kernel, input_shape=(size, 1)))
    model.add(Conv1D(filters=layers[0], kernel_size=kernel))
    model.add(MaxPooling1D(pool_size=kernel))

    model.add(Flatten())
    for layer in layers[1:]:
        model.add(Dense(layer, activation='relu'))

    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    folds = StratifiedKFold(n_splits=4, shuffle=True, random_state=0).split(x_data, y_data)
    for fold in folds:
        X_train_cv = x_data[fold[0]]
        y_train_cv = y_data[fold[0]]
        X_valid_cv = x_data[fold[1]]
        y_valid_cv = y_data[fold[1]]

        y_train_cv = np_utils.to_categorical(y_train_cv,2)
        y_valid_cv = np_utils.to_categorical(y_valid_cv,2)

        model.fit(
            x=X_train_cv,
            y=y_train_cv,
            batch_size=batch,
            epochs=epochs,
            shuffle=True,
            verbose=True,
            validation_data=(X_valid_cv, y_valid_cv),)

    score = model.evaluate(x_data, np_utils.to_categorical(y_data, 2), batch_size=16)

    print('Trainded score:', score)

    return model
