# Automatic classification of SDSS (BOSS/eBOSS) spectra using a deep learning approach

The code in this repository was part of an undergraduate summer research internship at Pontificia Universidad Catolica de Chile. The main goal of the work was to learn about basic deep learning techniques and apply them to develop a model able to tell quasars apart from stars in spectroscopic data,
inspired in the work of [Busca, 2018](https://arxiv.org/abs/1808.09955).
Originally, the training dataset had to contain the spectra of all the sources listed in the Million Quasar Catalog v5.7 ([MILLIQUAS](http://quasars.org/milliquas.htm)) and in the future it might. However, it was easier to first select data from a single instrument of a single survey to rule out resolution and spectral range differences. Most of the spectroscopically confirmed quasars in MILLIQUAS come from the SDSS DR14 Quasar Catalog ([DR14Q](https://arxiv.org/abs/1712.05029)) anyway, so the exclusion of non-SDSS data isn't a problem by now.

## The Dataset

The full dataset contains 765824 BOSS spectra: 446869 from quasars and 318955 from stars. The stellar sources were selected to have spectra with human inspected redshifts. In other words, to have a not-null entry for the ``Z_PERSON`` column in the ``DR15:dbo.SpecObjAll`` table. Each spectrum was max-normalized and downsampled from about 4000 datapoints to 433, in a fixed log-wavelength interval ranging from 3.56 $\log\AA$ to 4.01 $\log\AA$. Also, every spectrum was labeled with a ground-truth class either from DR14Q (in the case of quasar spectra) or from the SDSS automatic classification routines (in the case of stellar spectra). There were 12 distinct classes: QSO, BAL (Broad absorption line quasar), O, B, A, F, G, K, M, L, WD (White Dwarfs) and C (Carbon stars).  Below is a bar chart showing the distribution of spectral types within the stellar sample used in this work:  
  ![alt text](plots/star_population.png "Stellar type distribution")

Meanwhile, the quasar sample contains 21877 BAL quasars and 424992 normal quasars. The full dataset will soon be available on Kaggle. By now, it can be constructed by manually downloading the raw data and then applying the

### Notebooks
The notebooks inclued in this repo are a detailed discussion of the methods used and the problems I encountered while developing this project.  

## The Model
The proposed architecture has 5  1d-convolutional layers and 2 fully connected layers at the end. All activations are ReLU, except for the last layer which uses softmax. Details of each layer are shown in the following diagram
## Results
Add confusion matrix
## TODO

- [ ] Add signal-to-noise ratio data to the input of the net. In this way I hope the classifier will give better generalization, and avoid misclassification of very faint objects.
- [ ] Incorporate redshift estimation as a multi-task regression problem
- [ ] Add spectra from different surveys