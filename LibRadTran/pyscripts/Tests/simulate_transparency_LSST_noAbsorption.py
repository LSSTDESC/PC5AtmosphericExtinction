import os
import math
import numpy as np
import pandas as pd
from astropy.io import fits

import UVspec

# LibRadTran installation directory
home = os.environ['HOME']+'/'       
libradtranpath = home+'MacOsX/LSST/softs/radtran-2.0/libRadtran-2.0/'

# Filename : RT_LS_pp_us_sa_rt_z15_wv030_oz30.txt


#####################################################################
# The program simulation start here
#
####################################################################

if __name__ == "__main__":



    # airmass indexes
    airmasses_indexes=np.arange(10,31,1)
    
    

    # Set up type of run
    runtype='no_absorption' #'no_scattering' #aerosol_special #aerosol_default# #'clearsky'#     
    #runtype='clearsky' #'clearsky'#     
    if runtype=='clearsky':
        outtext='clearsky'
    elif runtype=='aerosol_default':
        outtext='aerosol_default'
    elif runtype=='no_scattering':
        outtext='no_scattering'
    elif runtype=='no_absorption':
        outtext='no_absorption'
    else:
        outtext='aerosol_special'
        


    molmodel='reptran'

    	  
    # for simulation select only two atmosphere   
    #theatmospheres = np.array(['afglus','afglms','afglmw','afglt','afglss','afglsw'])
    theatmospheres = np.array(['afglus','afglsw'])

    # 1) LOOP ON ATMOSPHERE
    for atmosphere in theatmospheres:
        #if atmosphere != 'afglus':  # just take us standard sky
        #    break
        # loop on molecular model resolution
        #molecularresolution = np.array(['COARSE','MEDIUM','FINE']) 
        # select only COARSE Model
        molecularresolution = np.array(['COARSE'])    
        for molres in molecularresolution:
            if molres=='COARSE':
                molresol ='coarse'
            elif molres=='MEDIUM':
                molresol ='medium'
            else:
                molresol ='fine'
           
        # 2) LOOP ON AIRMASSES 
        for index,fileindex in np.ndenumerate(airmasses_indexes):
            airmass=float(fileindex)/10.
            filenum=fileindex
            print '**** file numbers = ',filenum
            print '**** simulation number = ',index , ' for airmass = ',airmass                   
                    
            verbose=True
            uvspec = UVspec.UVspec()
            uvspec.inp["data_files_path"]  =  libradtranpath+'data'
                
            uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/'+atmosphere+'.dat'
            uvspec.inp["albedo"]           = '0.2'
            uvspec.inp["rte_solver"] = 'disort'
            uvspec.inp["mol_abs_param"] = molmodel + ' ' + molresol 

            # TODO calculate correcty the zenith angle from airmass 
            am=airmass
            sza=math.acos(1./am)*180./math.pi

            # Should be no_absorption
            if runtype=='aerosol_default':
                uvspec.inp["aerosol_default"] = ''
            elif runtype=='aerosol_special':
                uvspec.inp["aerosol_set_tau_at_wvl"] = '500 0.02'
                        
            if runtype=='no_scattering':
                uvspec.inp["no_scattering"] = ''
            if runtype=='no_absorption':
                uvspec.inp["no_absorption"] = ''
                uvspec.inp["aerosol_set_tau_at_wvl"] = '500 0.0'

                    
                
            uvspec.inp["output_user"] = 'lambda edir'
            uvspec.inp["altitude"] = '2.663'   # Altitude LSST observatory
            uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_1.0nm.dat'
            #uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_0.1nm.dat'
            uvspec.inp["sza"]        = str(sza)
            uvspec.inp["phi0"]       = '0'
            uvspec.inp["wavelength"]       = '250.0 1200.0'
            uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #
#           uvspec.inp["verbose"] = ''
            uvspec.inp["quiet"] = ''

  

            if "output_quantity" in uvspec.inp.keys():
                outtextfinal=outtext+'_'+uvspec.inp["output_quantity"]

            inp = 'input/UVSPEC_REPTRAN_SOLAR_ALT26_REFL_{}_{}'.format(atmosphere,fileindex)+'.INP'
            out = 'output/UVSPEC_REPTRAN_SOLAR_ALT26_{}_{}'.format(atmosphere,fileindex)+'.OUT'
            uvspec.write_input(inp)
            uvspec.run(inp,out,verbose,path=libradtranpath)

