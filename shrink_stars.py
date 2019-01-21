#!/usr/bin/env python

import pipeline as io
from glob import glob

# filelist = glob('data/star-lite/*.fits')

# for filename in filelist:
#     io.shrink_spectra(filename)

with open('targets2.txt', 'r') as targets:
    for line in targets:
        filepath = 'data/star-lite/{:s}'.format(line.strip())
        io.shrink_spectra(filepath)