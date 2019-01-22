#!/usr/bin/env python
import numpy as np
from glob import glob
import pipeline as io
import h5py
import os

sampling = 433
qsoglob = glob('data/quasarboss/*.fits')[:1000]
starglob = glob('data/starboss/*.fits')[:1000]  # These files aren't reduced in size but may still work

fileglob = qsoglob + starglob

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

if os.path.exists('data/dataset2K_433t.h5'):
    os.remove('data/dataset2K_433t.h5')

with h5py.File('data/dataset2K_433t.h5') as hdf:       
    X_dset  = hdf.create_dataset('fluxes', shape=(number_of_files, sampling, ), dtype='f4')
    Y_dset = hdf.create_dataset('classes', shape=(number_of_files, 1,), dtype='f4')
    X_dset[:] = X_array
    Y_dset[:] = Y_array

print('Done with {} files'.format(i + 1))