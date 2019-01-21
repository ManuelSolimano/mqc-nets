""" This file contains the functions needed to
read the spectra in a way it is feedable into the model
"""
import numpy as np
import fitsio
from fitsio import FITS, FITSHDR
import os
import shutil
from scipy.signal import resample
from scipy.interpolate import interp1d
import tempfile
from astropy.io import fits

endianess = {'big': '>', 'little':'<'}

DATA_PATH = '/home/manuel/mqc/data'
KNOWN_QSOS = np.loadtxt('/'.join([DATA_PATH, 'dr14q_specids.txt']), dtype=np.uint64)
KNOWN_STARS = np.loadtxt('/'.join([DATA_PATH, 'dr15stars_boss_masolimano.csv']), 
                         dtype=np.uint64, delimiter=',', skiprows=1, usecols=0)

def normalize(spectrum, method='max'):
    """
    (Re)normalize spectral flux according to what I understood from
    the QuasarNET paper and code (Busca ,2018).
    parameters:
        - spectrum: recarray. Input spectrum flux, wavelength and inverse variance. Shape (n, 3)
    returns:
        -normspec: recarray. Normalized flux, the other columns are kept the same.
        
    TODO: Test function to evaluate the need  of corner case management
    """
    if method == 'quasarnet':
        mdata = np.average(spectrum['flux'] , weights = spectrum['ivar'])
        sdata = np.average((spectrum['flux'] - mdata) ** 2, weights = spectrum['ivar'])
        sdata = np.sqrt(sdata) 

        normflux = (spectrum['flux'] - mdata) / sdata
        normspec = spectrum.copy()
        normspec['flux'] = normflux
        return normspec
    
    elif method == 'max':
        normspec = spectrum.copy()
        normspec['flux'] = spectrum['flux'] / spectrum['flux'].max()
        return normspec
    
def hash_specid(plate, mjd, fiberid, run2d):
    """
    Hash function that computes the SpecObj ID from the four spectral
    identifiers. This implementation follows the specification found at
    https://www.sdss.org/dr15/help/glossary/#specobj   
    This function can return very long integers, so make sure
    to store them as unsigned 64 bit integers.
    
    parameters:
     -plate: int, Drilled plate number
     -mjd :int, Modified Julian Date (days)
     -fiberid: int, Fiber ID number
     -run2d: int or str, Version of 2D reduction pipeline
     
     returns:
         -specid: int, SpecObjID
    """
    
    run2d = str(run2d)
    
    if 'v' in run2d:
        # The string must have shape 'vN_M_P' where N, M and P are integers
        nmp = run2d.split('_')
        N = int(nmp[0].strip('v'))
        M = int(nmp[1])
        P = int(nmp[2])
        assert 5 <= N <= 6 and 0 <= M <= 99 and 0 <= P <=99, "Invalid run2d"
        run2d  = (N - 5) * 10000 + M * 100 + P
        
    elif run2d.isnumeric():
        run2d = int(run2d)

    key = '{:014b}'.format(plate)    
    key += '{:012b}'.format(fiberid)
    key += '{:014b}'.format(mjd - 50000)
    key += '{:014b}'.format(run2d)
    key += '0' * 10
    
    specid = int(key, base=2)
    return specid

def tell_the_truth(filename):
    """ Return the truth vector for a given spectrum filename.
    Constants KNOWN_QSOS and KNOWN_STARS must be loaded in memory.
    parameters:
        -filename: str, the path to the spectrum fits file
    return:
        -truth: array, [qso_prob, redshift]
    
    TODO: Implement redshift  retrieval from fits file or specobjid
    """
    header = fitsio.read_header(filename)
    spec4numbers = (header['PLATEID'], header['MJD'], header['FIBERID'], header['RUN2D'].strip())
    specid = hash_specid(*spec4numbers)  # Compute specobjid hash 
    
    if specid in KNOWN_QSOS:
#         return np.array([1., 0.])
        return np.array([1.])
        
    elif specid in KNOWN_STARS:
#         return np.array([0., 0.])
        return np.array([0.])
    
    else:
        return None
    
def shrink_spectra(filepath, delete_source=False):
    """
    Remove unnecesary data from the spectral FITS file. All
    the data needed is contained in the header and the
    flux, loglam and ivar columns. This function
    trims the original fits file and saves the lightweight
    version in a {parent}_ultralight folder. Then deletes the original
    file.
    """
    pathlist = filepath.split('/')
    ultralight_parent  = '{}_ultralight'.format('/'.join(pathlist[:-1]))
    
    # Check if the target directory exists
    if not os.path.exists(ultralight_parent):
        os.mkdir(ultralight_parent)
    
    newpath = '/'.join([ultralight_parent, pathlist[-1]])
    
    temp = tempfile.NamedTemporaryFile(delete=False)
    
    try:
        with fits.open(filepath) as hdul:
            relevant_cols = hdul[1].data.columns[:3]
            hdul[1].data = hdul[1].data.from_columns(relevant_cols)
            hdul = hdul[:2]
            hdul.writeto(temp)

        shutil.move(temp.name, newpath)
        print('Created ' + newpath)

        if delete_source:
            os.remove(filepath)
            print('Removed ' + filepath)
    
    except TypeError:
        print(filepath + ' is defective, not processed')
    
    
    temp.close()

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

def load_1d_spectrum(filename, sampling=503, endpoints=(3.58, 3.96)):
    """
    params: filename: the path to the spectrum file

    returns:
        - X : resampled spectrum  (numpy array)
        - Y : truth vector indicating class
    """
    # First, load the file while enforcing the correct endianess
    spec = fitsio.read(filename, columns=['flux', 'loglam', 'ivar'], dtype = np.dtype('<f4'))
    
    # Normalize input spectrum
    normalized = normalize(spec)
    
    # Subsampling
    X = crop_and_subsample(normalized, sampling, endpoints)
    
    # Retrieve truth vector
    Y = tell_the_truth(filename)
    
    return X, Y


if __name__ == "__main__":
    spec = fitsio.read('data/spectra1000/spec-4216-55477-0210.fits', columns=['flux','loglam', 'ivar'], dtype=np.float32)
    #subspec = crop_and_subsample(spec, 503, (3.56, 4.01))
    normalized = normalize(spec)


