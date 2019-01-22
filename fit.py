#!/usr/bin/env python

"""
Main training experiment for spectral classification
"""

import numpy as np
import matplotlib.pyplot as plt
import keras
import pipeline as io
import h5py
from exif import Image

from keras.layers import Input, Dense, Conv1D, Dropout, Flatten
from keras.activations import  softmax, relu, sigmoid
from keras.models import Model, Sequential
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split


def performance_plots(filename, sgdparams, histobject, testmetrics):
    
    loss = histobject.history['loss']
    val_loss = histobject.history['val_loss']
    binary_accuracy = histobject.history['binary_accuracy']
    val_binary_accuracy = histobject.history['val_binary_accuracy']
    
    fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True,
                          sharey='row', figsize=(9,9))
    ax[0,0].plot(loss)
    ax[0,0].set_ylabel(r'Categorical cross-entropy loss')
    ax[0,1].plot(val_loss)
    ax[0,1].set_ylabel(r'Loss on validation data')
    ax[1,0].plot(binary_accuracy)
    ax[1,0].set_ylabel(r'Binary accuracy on training data')
    ax[1,1].plot(val_binary_accuracy)
    ax[1,1].set_ylabel(r'Binary accuracy on validation data')
    
    ax[1,0].set_xlabel(r'Epoch')
    ax[1,1].set_xlabel(r'Epoch')
    
    metadata = histobject.params
    metadata['test_metrics'] = testmetrics
    metadata['sgd_params'] = sgdparams
    
    plt.savefig(filename, dpi=450, metadata=metadata)
   

with h5py.File('data/dataset2K_433t.h5', 'r') as sb:
    og_shape = sb['fluxes'].shape
    data = np.array(sb['fluxes']).reshape((*og_shape, 1))
    labels = to_categorical(np.array(sb['classes']))
    
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.20,
                                                       random_state=42)
x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.50,
                                                   random_state=42)

sgdparams = {'lr':0.001, 'momentum':0.9, 'nesterov':True}
    
    
model = Sequential()
model.add(Conv1D(filters=25, kernel_size=11,
                 strides=1, activation='relu',
                input_shape=(433,1)))

model.add(Conv1D(filters=25, kernel_size=10, 
                 strides=2, activation='relu'))
model.add(Conv1D(filters=15, kernel_size=9,
                 strides=1, activation='relu'))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(**sgdparams),
             metrics=['binary_accuracy'])
training = model.fit(x_train, y_train, epochs=150, batch_size=40, validation_data=(x_val, y_val))
metrics = model.evaluate(x_test, y_test, batch_size=40)

performance_plots('plots/model0_run0.png', sgdparams,training, metrics)

print('test_loss: {}\nbinary_accuracy: {}'.format(metrics[0], metrics[1]))
# predicted = model.predict(x_test)