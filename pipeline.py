""" This file contains the functions needed to
read the spectra in a way it is feedable into the model
"""
import numpy as np
import fitsio
from fitsio import FITS, FITSHDR
import sys
from scipy.signal import resample
from scipy.interpolate import interp1d

endianess = {'big': '>', 'little':'<'}

def normalize(spectrum):
    """
    (Re)normalize spectral flux according to what I understood from
    the QuasarNET paper and code (Busca ,2018).
    parameters:
        - spectrum: recarray. Input spectrum flux, wavelength and inverse variance. Shape (n, 3)
    returns:
        -normspec: recarray. Normalized flux, the other columns are kept the same.
        
    TODO: Test function to evaluate the need  of corner case management
    """
    
    mdata = np.average(spectrum['flux'] , weights = spectrum['ivar'])
    sdata = np.average((spectrum['flux'] - mdata) ** 2, weights = spectrum['ivar'])
    sdata = np.sqrt(sdata) 
    
    normflux = (spectrum['flux'] - mdata) / sdata
    normspec = spectrum
    normspec['flux'] = normflux
    return normspec

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


def crop_and_subsample(nspec, pixels, borders):
    """
    This function forces the wavelength axis to match the given borders
    and then resamples the flux signal to the new number of pixels.
    parameters:
        -nspec: recarray, input spectrum table including at least flux and log10(wavelength)
        -pixels: int, number of new samples of data to produce
        -borders: tuple, (min-wav, max-wav). Indicates the log10(wavelength) interval to consider.
    returns:
        -sub_flux: array, Resampled spectrum flux of shape (1, n).
    
    TODO: Test and add exception catching for the endianness problem (scipy.signal.resample does not support dtpye='>f4')
    """
    
    #     assert spectrum['flux'].byteorder() == '<'  and spectrum['loglam'].byteorder() == '<', "The endianness of the input spectrum is notlittle-endian and hence scipy.signal rescaling is not supported"
    
    flux, loglam =  nspec['flux'], nspec['loglam']
    
    # Interpolate the input spectrum over the desired borders
    inter_spec = interp1d(loglam, flux, kind = 'cubic')
    new_loglam = np.linspace(*borders, len(flux), endpoint=True)
    new_flux = inter_spec(new_loglam)
    
    # Resample to a total of 'pixels' equally spaced data points
    sub_flux, sub_loglam = resample(new_flux, pixels, new_loglam)
    return sub_flux

def load_1d_spectrum(filename):
    """
    params: filename: the path to the spectrum file

    returns:
        - X : resampled spectrum  (numpy array)
        - Y : truth vector indicating class
    """
    pass



if __name__ == "__main__":
    spec = fitsio.read('data/spectra1000/spec-4216-55477-0210.fits', columns=['flux','loglam', 'ivar'], dtype=np.float32)
    #subspec = crop_and_subsample(spec, 503, (3.56, 4.01))
    normalized = normalize(spec)


