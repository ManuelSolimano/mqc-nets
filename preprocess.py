#!/usr/bin/env python
import numpy as np
from glob import glob
import pipeline as io
import h5py
import os
import json

with open('data/class_lookup.json', 'r') as clas:
    lookup = json.load(clas)


sampling = 433
classes = 11
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

X_array = np.zeros((number_of_files, sampling,))
Y_array = np.zeros((number_of_files, classes,))

count = 0
for filename in fileglob:
    try:
        x, y = io.load_1d_spectrum(filename, lookup, sampling=sampling)
        
        # If there are no NaN values, proceed
        if not np.any(np.isnan(x)):
            X_array[count,...] = x
            Y_array[count,...] = y
            count += 1
        
    except ValueError:
        # I forgot the actual bug behind this :c
        print(filename + ' caused problems')
    
    except OSError:
        # Apparently fitsio cannot find some files
        print('Fitsio failed to open ' + filename)
        
    if count % 10 == 0:
        print('Processed  {} files so far'.format(count))

# Crop trailing empty rows

X_array, Y_array = X_array[:count,...], Y_array[:count,...]


outfile = 'data/dataset{}_{}t_{}c.h5'.format(count, sampling, classes)
if os.path.exists(outfile):
    os.remove(outfile)

with h5py.File(outfile) as hdf:       
    X_dset  = hdf.create_dataset('fluxes', shape=X_array.shape, dtype='f4')
    Y_dset = hdf.create_dataset('classes', shape=Y_array.shape, dtype='f4')
    X_dset[:] = X_array
    Y_dset[:] = Y_array

print('Done with {} files'.format(count))