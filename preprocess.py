#!/usr/bin/env python
import numpy as np
from glob import glob
import pipeline as io
import h5py
import os

sampling = 433
fileglob = glob('data/starboss/*.fits')[:200]
number_of_files = len(fileglob)

X_array = np.zeros((number_of_files, sampling, ))
Y_array = np.zeros((number_of_files, 1,))

try:
    for i, filename in enumerate(fileglob):
        x, y = io.load_1d_spectrum(filename, sampling=sampling)
        X_array[i,...] = x
        Y_array[i,...] = y
        if i % 10 == 0:
            print('Processed  {} files so far'.format(i + 1))
except ValueError:
    print(filename + ' caused problems')
os.remove('data/reduced_starboss.h5')
with h5py.File('data/reduced_starboss.h5') as hdf:       
    X_dset  = hdf.create_dataset('fluxes', shape=(number_of_files, sampling, ), dtype='f')
    Y_dset = hdf.create_dataset('classes', shape=(number_of_files, 1,), dtype='f')
    X_dset[:] = X_array
    Y_dset[:] = Y_array

print('Done with {} files'.format(i + 1))