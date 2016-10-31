import os
import re
import math
import numpy as np
import pandas as pd
from astropy.io import fits

import UVspec



# Definitions and configuration
#-------------------------------------

# LibRadTran installation directory
home = os.environ['HOME']+'/'       
libradtranpath = home+'MacOsX/LSST/softs/radtran-2.0/libRadtran-2.0/'

# Filename : RT_LS_pp_us_sa_rt_z15_wv030_oz30.txt
#          : Prog_Obs_Rte_Atm_proc_Mod_zXX_wv_XX_oz_XX
  
Prog='RT'  #definition the simulation programm is libRadTran
Obs='LS'   # definition of observatory site (LS,CT,OH,MK,...)
Rte='pp'   # pp for parallel plane of ps for pseudo-spherical
Atm=['us','sw']   # short name of atmospheric sky here US standard and  Subarctic winter
Proc='sc'  # light interfaction processes : sc for pure scattering,ab for pure absorption
           # sa for scattering and absorption, ae with aerosols default, as with aerosol special
Mod='rt'   # Models for absorption bands : rt for REPTRAN, lt for LOWTRAN, k2 for Kato2
ZXX='z'        # XX index for airmass z :   XX=int(10*z)
WVXX='wv'      # XX index for PWV z :   XX=int(10*z)
OZXX='oz'



LSST_Altitude = 2.750  # in k meters
OBS_Altitude = str(LSST_Altitude)

TOPINPUTDIR='./input'
TOPOUTPUTDIR='./output'


############################################################################
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)
#########################################################################

#####################################################################
# The program simulation start here
#
####################################################################

if __name__ == "__main__":

    ensure_dir(TOPINPUTDIR)
    ensure_dir(TOPOUTPUTDIR)


    # No Ozone for a pure scattering atmosphere
    # No PWV for a pure scattering atmosphere

    # airmass indexes defined for the whole production from z=1 to z=3
    airmasses_indexes=np.arange(10,31,1)
    
    
    # build the part 1 of filename
    BaseFilename_part1=Prog+'_'+Obs+'_'+Rte+'_'
    
    


    # Set up type of run
    runtype='no_absorption' #'no_scattering' #aerosol_special #aerosol_default# #'clearsky'#     
    if Proc == 'sc':
        runtype='no_absorption'
        outtext='no_absorption'
    elif Proc == 'ab':
        runtype='no_scattering'
        outtext='no_scattering'
    elif Proc == 'sa':
        runtype=='clearsky'
        outtext='clearsky'
    elif Proc == 'ae':   
        runtype='aerosol_default'
        outtext='aerosol_default'
    elif Proc == 'as':   
        runtype='aerosol_special'
        outtext='aerosol_special'
    else:
        runtype=='clearsky'
        outtext='clearsky'

#   Selection of RTE equation solver        
    if Rte == 'pp': # parallel plan
        rte_eq='disort'
    elif Rte=='ps':   # pseudo spherical
        rte_eq='sdisort'
        
        

#   Selection of absorption model 
    molmodel='reptran'
    if Mod == 'rt':
        molmodel='reptran'
    	  
    # for simulation select only two atmosphere   
    #theatmospheres = np.array(['afglus','afglms','afglmw','afglt','afglss','afglsw'])
    atmosphere_map=dict()  # map atmospheric names to short names 
    atmosphere_map['afglus']='us'
    atmosphere_map['afglms']='ms'
    atmosphere_map['afglmw']='mw'  
    atmosphere_map['afglt']='tp'  
    atmosphere_map['afglss']='ss'  
    atmosphere_map['afglsw']='sw'  
      
    theatmospheres= []
    for skyindex in Atm:
        if re.search('us',skyindex):
            theatmospheres.append('afglus')
        if re.search('sw',skyindex):
            theatmospheres.append('afglsw')
            
   
   

    # 1) LOOP ON ATMOSPHERE
    for atmosphere in theatmospheres:
        #if atmosphere != 'afglus':  # just take us standard sky
        #    break
        atmkey=atmosphere_map[atmosphere]
       
        
        INPUTDIR=TOPINPUTDIR+'/'+atmosphere
        ensure_dir(INPUTDIR)
        OUTPUTDIR=TOPOUTPUTDIR+'/'+atmosphere
        ensure_dir(OUTPUTDIR)
    
    
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
        for index,amfileindex in np.ndenumerate(airmasses_indexes):
            print index,amfileindex
            
        
            # airmass
            airmass=float(amfileindex)/10.
            
            print amfileindex
            
            BaseFilename=BaseFilename_part1+atmkey+'_'+Proc+'_'+Mod+'_z'+str(amfileindex)                   
                    
            verbose=True
            uvspec = UVspec.UVspec()
            uvspec.inp["data_files_path"]  =  libradtranpath+'data'
                
            uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/'+atmosphere+'.dat'
            uvspec.inp["albedo"]           = '0.2'
            
            
            
            uvspec.inp["rte_solver"] = rte_eq
            
            
            uvspec.inp["mol_abs_param"] = molmodel + ' ' + molresol 

            # Convert airmass into zenith angle 
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
            uvspec.inp["altitude"] = OBS_Altitude   # Altitude LSST observatory
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

           
            
            inputFilename=BaseFilename+'.INP'
            outputFilename=BaseFilename+'.OUT'
            inp=os.path.join(INPUTDIR,inputFilename)
            out=os.path.join(OUTPUTDIR,outputFilename)
                    
            
            uvspec.write_input(inp)
            uvspec.run(inp,out,verbose,path=libradtranpath)

