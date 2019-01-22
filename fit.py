#!/usr/bin/env python

"""
Main training experiment for spectral classification
"""

import numpy as np
import keras
import pipeline as io
import h5py

from keras.layers import Input, Dense, Conv1D, Dropout, Flatten
from keras.activations import  softmax, relu, sigmoid
from keras.models import Model, Sequential
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split


with h5py.File('data/fulldataset_reduced.h5', 'r') as sb:
    og_shape = sb.shape
    data = np.array(sb['fluxes']).reshape((*og_shape, 1))
    labels = to_categorical(np.array(sb['classes']))
    
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.20,
                                                       random_state=42)
x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.50,
                                                   random_state=42)
    
    
    
model = Sequential()
model.add(Conv1D(filters=25, kernel_size=11,
                 strides=1, activation='relu',
                input_shape=(433,1)))

model.add(Conv1D(filters=25, kernel_size=10, 
                 strides=2, activation='relu'))
model.add(Conv1D(filters=15, kernle_size=9,
                 strides=1, activation='relu'))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))
model.fit(x_train, y_train, epochs=5, batch_size=10, validation_data=(x_val, y_val))
score = model.evaluate(x_test, y_test, batch_size=16)
print(score)