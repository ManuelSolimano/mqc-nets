# Issues so far
1. No version of the Million Quasar Catalog has proper SDSS object IDs, so a direct cross-id match with Gaia was not possible
2. Until 9 January I couldn't figure out how to perform a positional cross-match of MQC objects with any SDSS release within the CasJobs service, because it does not have the ADQL functions (```DISTANCE```, ```POINT```, ```CIRCLE```). Then I found the ```dbo.fGetNearestObjAllEq``` table-valued function provided by SDSS which showed very handy for the task.
3. I also tried to retrieve the objIDs from the TAP VizieR query service, which had a version of DR9 data including the J000+blabla.. names used in MQC. However, this is an old release  and the MQC version stored in VizieR isn't up to date either.
4. The version 5.7 of the MQC (with data until 7 January 2019) is available only in simple text format, with entries separated by whitespaces. The way the file is structured is non-standard and has a lot of missing entries. I'm still trying to read it from astropy/numpy/pandas.
5. I performed a positional crossmatch between MQCv5.2 and Gaia DR2 with a max radius of 1 arcsecond. The search returned more than 200k rows, but the distribution of distances was slightly bi-modal, hence suggesting contamination from other sources. However, even selecting the nearest match and dropping the other matches, the bump was still there in the histogram.
6. Some DR14Q spectra aren't found at ```https://data.sdss.org/sas/dr15/eboss/spectro/redux/v5_10_0/spectra/``` because they are legacy spectra that belong to a different survey program and different ```RUN2D```. So the ```wget``` command has to be modified in order to retrieve those files.
7. Great, I spend a lot of time collecting the photometry of DR14Q sources while the catalog fits file included the ugriz magnitudes!
8. I have to downgrade to Python 3.6 because TensorFlow doesn't support Python 3.7, this means creating a new environment
TODO:
- [x] Find a way to read the latest version of the MQC
- [X] Keep only the spectroscopically confirmed quasars
- [X] Find a way to retrieve legacy spectra listed on DR14Q
- [X] Prototype spectrum reduction pipeline (subsampling and interpolation)
- [ ] Add class information to header of spectra, or better, create a lookup table
- [ ] Include line recognition flags, i.e should the model be a line finder?
- [ ] (almost done) Make a training/testing set 1 using ugriz photometry from DR15, known classes and redshifts, the set should also include non quasar PLOs
- [ ] Make a training/testing  set 2 using the spectra of the known quasars and stars, together with its redshift. This dataset will probably be smaller than dataset 1, but could better justify the use of deep-learning because of the automatic feature extraction