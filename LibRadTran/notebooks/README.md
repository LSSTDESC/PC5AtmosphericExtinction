PC5AtmosphericExtinction/LibRadTran/notebooks/README.md
-------------------------------------------------------

Directory containing notebooks to control input and output of LibRadtran.


These notebook are written for python 2.7
Packages required:

- numpy
- matplotlib
- astropy


Directory templates: 
-------------------
Provided by astropy package to have nice matplotlib images.


View air transparencies for pure scattering sky:
----------------------------------------------
- Show_RT_LS_pp_sc_rt.ipynb
- Show_RT_LS_ps_sc_rt.ipynb



View air transparencies for pure absorbing sky:
----------------------------------------------
- vary ozone : simulate_transparency_LSST_noScattering_absoz.py
- vary water vapor :simulate_transparency_LSST_noScattering_abspwv.py


View air transparencies for scattering and absorbing sky:
-------------------------------------------------
- vary ozone : Show_RT_LS_pp_sa_rt_oz.ipynb



Examples of two old notebooks to read LibRadTran output:
--------------------------------------------------------
- ShowLibRadTranAllSpectra.ipynb
- ShowLibRadTranOneAMSpectra.ipynb

