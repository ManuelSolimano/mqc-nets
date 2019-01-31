#!/usr/bin/env python
import numpy as np
from glob import glob
import pipeline as io
import h5py
import os
import json
import argparse


def create_hdf5(path, sampling,
                classes, verbose=True):
    """ Build a HDF5 file containing the subsampled spectra
    and their truth vectors.
    
    Parameters
    ----------
    
    path: str,
        filename of the list containing the path to every
        selected spectra
    
    sampling: int
        Number of wavelength steps for subsampling spectra.
        
    classes: int
        Number of classes the dataset may have. Must match the
        length of the truth vectors returned by load_1d_spectrum.
    """
    with open('data/class_lookup.json', 'r') as clas:
        lookup = json.load(clas)


#     qsoglob = glob('data/quasarboss/*.fits')
#     if quasarnum > 0:
#         qsoglob = np.array(qsoglob)
#         qsoglob = qsoglob[np.random.choice(qsoglob.size,
#                                            quasarnum,
#                                            replace=False)].tolist()

    with open(path, 'r') as pb:
        fileglob = []
        for line in pb:
            fileglob.append(line.strip())

    number_of_files = len(fileglob)
    print('Files listed: {}'.format(number_of_files))
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
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Loop processing through all the spectra')
    parser.add_argument("path", help='Filename of the list of FITS files to process')

    parser.add_argument("--verbose", help='If True will print a line every 10 processed files. Else will only issue the warnings and erros. Defaults to true', action='store_true')
    args = parser.parse_args()
    
    create_hdf5(args.path, 433, 13, verbose=args.verbose)