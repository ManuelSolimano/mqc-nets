#!/usr/bin/env python
import numpy as np
from glob import glob
import pipeline as io
import h5py
import os

sampling = 433
# qsoglob = glob('data/quasarboss/*.fits')[:1000]
# starglob = glob('data/starboss/*.fits')[:1000]  # These files aren't reduced in size but may still work

qsoglob = np.array(glob('data/quasarboss/*.fits'))
qsoglob = qsoglob[np.random.choice(qsoglob.size, 17750, replace=False)].tolist()

with open('data/filelist_starboss_homosample_17750.txt', 'r') as sb:
    starglob = []
    for line in sb:
        starglob.append(line.strip())

fileglob = qsoglob + starglob

number_of_files = len(fileglob)

X_array = np.zeros((number_of_files, sampling, ))
Y_array = np.zeros((number_of_files, 1,))

count = 0
for i, filename in enumerate(fileglob):
    try:
        x, y = io.load_1d_spectrum(filename, sampling=sampling)
        X_array[i,...] = x
        Y_array[i,...] = y
        count += 1
        
    except ValueError:
        # I forgot the actual bug behind this :c
        print(filename + ' caused problems')
    
    except OSError:
        # Apparently fitsio cannot find some files
        print(filename + ' Fitsio failed to open')
    
    if count % 10 == 0:
        print('Processed  {} files so far'.format(count))


outfile = 'data/dataset{}_{}t.h5'.format(count, sampling)
if os.path.exists(outfile):
    os.remove(outfile)

with h5py.File(outfile) as hdf:       
    X_dset  = hdf.create_dataset('fluxes', shape=(number_of_files, sampling, ), dtype='f4')
    Y_dset = hdf.create_dataset('classes', shape=(number_of_files, 1,), dtype='f4')
    X_dset[:] = X_array
    Y_dset[:] = Y_array

print('Done with {} files'.format(count))