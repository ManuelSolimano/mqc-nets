# Issues so far
1. No version of the Million Quasar Catalog has proper SDSS object IDs, so a direct cross-id match with Gaia was not possible
2. Until 9 January I couldn't figure out how to perform a positional cross-match of MQC objects with any SDSS release within the CasJobs service, because it does not have the ADQL functions (```DISTANCE```, ```POINT```, ```CIRCLE```). Then I found the ```dbo.fGetNearestObjAllEq``` table-valued function provided by SDSS which showed very handy for the task.
3. I also tried to retrieve the objIDs from the TAP VizieR query service, which had a version of DR9 data including the J000+blabla.. names used in MQC. However, this is an old release  and the MQC version stored in VizieR isn't up to date either.
4. The version 5.7 of the MQC (with data until 7 January 2019) is available only in simple text format, with entries separated by whitespaces. The way the file is structured is non-standard and has a lot of missing entries. I'm still trying to read it from astropy/numpy/pandas.
5. I performed a positional crossmatch between MQCv5.2 and Gaia DR2 with a max radius of 1 arcsecond. The search returned more than 200k rows, but the distribution of distances was slightly bi-modal, hence suggesting contamination from other sources. However, even selecting the nearest match and dropping the other matches, the bump was still there in the histogram.
6. Some DR14Q spectra aren't found at ```https://data.sdss.org/sas/dr15/eboss/spectro/redux/v5_10_0/spectra/``` because they are legacy spectra that belong to a different survey program and different ```RUN2D```. So the ```wget``` command has to be modified in order to retrieve those files.
7. Great, I spend a lot of time collecting the photometry of DR14Q sources while the catalog fits file included the ugriz magnitudes!
8. I have to downgrade to Python 3.6 because TensorFlow doesn't support Python 3.7, this means creating a new environment
9. I initially thought the most narrow limits for ``loglam`` were ``[3.56-4.01]``, however, in the starboss files I found spectra with limits as narrow as ``[3.5579-3.8018]``. This is a problem because interpolation cannot be done outside these limits, and if I just crop the spectra I may end with smaller and smaller spectra. 
10. I expected that using a bigger dataset (35K spectra versus 2K), would immediately yield better results with the same architecture. After fiddling with the model and its parameters in Collab I was pretty disappointed because I cannot get the model to learn anything. It is stuck on loss ~0.6. Also the binary accuracy on the validation set is 0.4969 at the end of almost every epoch. Need to 1) tune those hyperparameters and/or 2) keep trying new  architectures (deeper or shallower) 
11. The ``performance_plots`` function has bugs: 
  - Parsing metadata to png plots is silently failing because (I guess) some values in the dictionary are not strings.
  - If the metrics passed to the compiler are other than ``binary_accuracy``, it fails.
12. 30 January: I discovered I was croping in a much narrower interval than I supposed! The default interval  of `load_1d_spec` was (3.58-3.96) instead of (3.56-4.01). Press F to pay respects :/ 
TODO:
- [x] Find a way to read the latest version of the MQC
- [X] Keep only the spectroscopically confirmed quasars
- [X] Find a way to retrieve legacy spectra listed on DR14Q
- [X] Prototype spectrum reduction pipeline (subsampling and interpolation)
- [X] Fix interpolation outside range issue
- [X] Add class information to header of spectra, or better, create a lookup table
- [ ] Study what ``scipy.signal.resample`` is doing behind the screens
- [X] Get the new model working on the extended dataset (may be necessary to check the file is OK)
- [X] Build the full-size dataset trying to match stellar type abundances with those reported by SDSS, instead of splitting in equal parts. Also, add QSO_BAL class.
- [ ] Find out why some specObjIDs are not found in the lookup json file.
- [ ] Incorporate SNR to input data
- [ ] Select spectra of galaxies to include in the dataset.
- [X] Fix bugs in ``performance_plots``.
- [X] Find a way to plot a confusion matrix
- [ ] Add more plots to the README (to further characterize the dataset)
- [ ] Add diagram of network architecture
- [ ] Upload dataset to kaggle
- [ ] Use k-fold cross-validation.
- [ ] Include line recognition flags, i.e should the model be a line finder?
- [ ] Use multitask learning to compute the redshift alongside classification 
- [ ] (almost done) Make a training/testing set 1 using ugriz photometry from DR15, known classes and redshifts, the set should also include non quasar PLOs
- [X] Make a training/testing  set 2 using the spectra of the known quasars and stars, together with its redshift. This dataset will probably be smaller than dataset 1, but could better justify the use of deep-learning because of the automatic feature extraction
