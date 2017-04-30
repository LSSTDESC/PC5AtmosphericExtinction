import os
import math
import numpy as np
import UVspec

home = os.environ['HOME']+'/'
        


#####################################################################
# The program simulation start here
#
####################################################################

if __name__ == "__main__":


    # Set up type of run
    runtype='aerosol_special' #'aerosol_special' #aerosol_default# #'clearsky'#     
    #runtype='clearsky' #'clearsky'#     
    if runtype=='clearsky':
        outtext='clearsky'
    elif runtype=='aerosol_default':
        outtext='aerosol_default'
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

#    theatmospheres = np.array(['afglus','afglms','afglmw','afglt','afglss','afglsw'])
    theatmospheres = np.array(['afglms'])

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
            libradtranpath = home+'MacOsX/LSST/softs/libRadtran-2.0.1/'
    
            # Rough estimate of center wavlengths of LSST filters. Should use filter functions
            # instead.

            # loop on air-masses
#            airmassesval = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            airmassesval = np.array([10])
     
            for airmass in airmassesval:
                verbose=True
                uvspec = UVspec.UVspec()
                uvspec.inp["data_files_path"]  =  libradtranpath+'data'
                #uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/afglt.dat'
                uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/'+atmosphere+'.dat'
                uvspec.inp["albedo"]           = '0.2'
                uvspec.inp["rte_solver"] = 'disort'
                uvspec.inp["mol_abs_param"] = molmodel + ' ' + molresol 

                am=airmass/10.
                sza=math.acos(1./am)*180./math.pi
        

#                uvspec.inp["mol_modify"]= 'H2O 4.0 MM'

                if runtype=='aerosol_default':
                    uvspec.inp["aerosol_default"] = ''
                elif runtype=='aerosol_special':
                    uvspec.inp["aerosol_set_tau_at_wvl"] = '532 0.157276'
                    
                
                uvspec.inp["output_user"] = 'lambda edir'
                uvspec.inp["altitude"] = '0.650'
                uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_1.0nm.dat'
                #uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_0.1nm.dat'
                uvspec.inp["sza"]        = str(sza)
                uvspec.inp["phi0"]       = '0'
                uvspec.inp["wavelength"]       = '300.0 1000.0'
                uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #
                #uvspec.inp["quiet"] = ''
                uvspec.inp["verbose"] = ''

                if "output_quantity" in uvspec.inp.keys():
                    outtextfinal=outtext+'_'+uvspec.inp["output_quantity"]

                inp = 'input/UVSPEC_REPTRAN_SOLAR_ALTOHP_REFL_{:2.0f}'.format(airmass)+'.inp'
                out = 'output/{}/UVSPEC_REPTRAN_SOLAR_ALTOHP_{}_{:2.0f}'.format(atmosphere,molres,airmass)+'.out'
                uvspec.write_input(inp)
                uvspec.run(inp,out,verbose,path=libradtranpath)

