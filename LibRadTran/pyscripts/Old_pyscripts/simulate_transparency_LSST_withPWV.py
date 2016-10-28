import os
import math
import numpy as np
import pandas as pd
from astropy.io import fits

import UVspec

home = os.environ['HOME']+'/'
        


#####################################################################
# The program simulation start here
#
####################################################################

if __name__ == "__main__":



    PWV_names = ['pwv00','pwv01','pwv02','pwv03','pwv04','pwv05','pwv10','pwv15','pwv20','pwv25','pwv30','pwv35','pwv40','pwv45','pwv50','pwv55','pwv60','pwv65','pwv70','pwv75','pwv80' ]   # name 

    PWV_values= [0.,0.1,0.2,0.3,0.4,0.5,1.,1.5,2.0,2.5,3,3.5,4.,4.5,5,5.5,6,6.5,7.,7.5,8]  # mm  PWV 



    airmasses_indexes=np.arange(10,21,1)
    
    

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


    # atmospheric models
    # afglus.dat
    # afglms.dat
    # afglmw.dat
    # afglt.dat
    # afglss.dat				
    # afglsw.dat		  

    #theatmospheres = np.array(['afglus','afglms','afglmw','afglt','afglss','afglsw'])
    theatmospheres = np.array(['afglus'])

    for atmosphere in theatmospheres:
        #if atmosphere != 'afglus':  # just take us standard sky
        #    break
        # loop on molecular model resolution
        #molecularresolution = np.array(['COARSE','MEDIUM','FINE'])    
        molecularresolution = np.array(['COARSE'])    
        for molres in molecularresolution:
            if molres=='COARSE':
                molresol ='coarse'
            elif molres=='MEDIUM':
                molresol ='medium'
            else:
                molresol ='fine'
           
            #libradtranpath = home+'develop/libRadtran/'
            libradtranpath = home+'MacOsX/LSST/softs/radtran-2.0/libRadtran-2.0/'
    
            # Rough estimate of center wavlengths of LSST filters. Should use filter functions
            # instead.

            # loop on PWV
            for idx, pwv in enumerate(PWV_values):
                precipitablewatervaporstring='H2O '+str(pwv) + ' MM'
                          
                print ' ** PWV_names = ',PWV_names[idx],' ** pwv=', pwv,'** idx= ',idx
                
                print ' ** precipitablewatervaporstring= ',precipitablewatervaporstring
     
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

                    am=airmass
                    sza=math.acos(1./am)*180./math.pi

                    uvspec.inp["mol_modify"] = precipitablewatervaporstring

                    if runtype=='aerosol_default':
                        uvspec.inp["aerosol_default"] = ''
                    elif runtype=='aerosol_special':
                        uvspec.inp["aerosol_set_tau_at_wvl"] = '500 0.02'
                    
                
                    uvspec.inp["output_user"] = 'lambda edir'
                    uvspec.inp["altitude"] = '2.663'   # Altitude LSST observatory
                    uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_1.0nm.dat'
                    #uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_0.1nm.dat'
                    uvspec.inp["sza"]        = str(sza)
                    uvspec.inp["phi0"]       = '0'
                    uvspec.inp["wavelength"]       = '250.0 5000.0'
                    uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #
#                    uvspec.inp["verbose"] = ''
                    uvspec.inp["quiet"] = ''

                    if runtype=='no_scattering':
                        uvspec.inp["no_scattering"] = ''
                    if runtype=='no_absorption':
                        uvspec.inp["no_absorption"] = ''
                        uvspec.inp["aerosol_set_tau_at_wvl"] = '500 0.0'




                    if "output_quantity" in uvspec.inp.keys():
                        outtextfinal=outtext+'_'+uvspec.inp["output_quantity"]

                    inp = 'input/UVSPEC_REPTRAN_SOLAR_ALT26_REFL_{}_{}'.format(PWV_names[idx],filenum)+'.inp'
                    out = 'output/{}/{}/UVSPEC_REPTRAN_SOLAR_ALT26_{}_{}_{}'.format(runtype,atmosphere,molres,PWV_names[idx],filenum)+'.out'
                    uvspec.write_input(inp)
                    uvspec.run(inp,out,verbose,path=libradtranpath)

