""" This file contains the functions needed to
read the spectra in a way it is feedable into the model
"""
import numpy as np
import fitsio
from fitsio import import FITS, FITSHDR
import sys

endianess = {'big': '>', 'little':'<'}

def normalize(spectrum):
    pass

def tell_the_truth(plate, mjd, fiberid):
    """
    Database lookup to determine classification
    params:
        -plate: plate id
        -mjd: modified julian date
        -fiberid: fiber id
    returns:
        -Y: truth vector indicating class
    """
    pass


def subsample(spectrum, pixels):
    assert spectrum['flux'].byteorder() == '<'  and spectrum['loglam'].byteorder() == '<', "The endianness of the input spectrum is not
    little-endian and hence scipy.signal rescaling is not supported"
    sub_flux, sub_loglam = resample(spectrum['flux'], spectrum['loglam'], pixels)
    return sub_flux

def load_1d_spectrum(filename):
    """
    params: filename: the path to the spectrum file

    returns:
        - X : resampled spectrum  (numpy array)
        - Y : truth vector indicating class
    """
    pass







