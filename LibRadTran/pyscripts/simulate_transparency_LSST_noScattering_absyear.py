################################################################
#
# Script to simulate air transparency with LibRadTran
# With a pure absorbing atmosphere
#
# author: sylvielsstfr
# creation date : November 1st 2016
# 
#
#################################################################
import os
import re
import math
import numpy as np
import pandas as pd
from astropy.io import fits

import UVspec



h2ofile='info/AIRS_2016_TotH2OVap_D.csv'	
o3file='info/AIRS_2016_TotO3_D.csv'


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
Proc='ab'  # light interaction processes : sc for pure scattering,ab for pure absorption
           # sa for scattering and absorption, ae with aerosols default, as with aerosol special
Mod='rt'   # Models for absorption bands : rt for REPTRAN, lt for LOWTRAN, k2 for Kato2
ZXX='z'        # XX index for airmass z :   XX=int(10*z)

YXX='y'    # year number
MXX='m'    # month number

WVXX='wv'      # XX index for PWV       :   XX=int(pwv*10)
OZXX='oz'      # XX index for OZ        :   XX=int(oz/10)



LSST_Altitude = 2.750  # in k meters from astropy package (Cerro Pachon)
OBS_Altitude = str(LSST_Altitude)

TOPDIR='../simulations/RT/2.0/LS'



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

    ensure_dir(TOPDIR)

    pandas_fieldname=['dates','average','ct','err','std','min','max']

    atm_variations=['aver','std1','std2','min','max']
    atm_variations=np.array(atm_variations)

    # import files for airs satellite
    dataseto3=pd.read_csv(o3file)
    dataseth2o=pd.read_csv(h2ofile)

    dates_o3=dataseto3[pandas_fieldname[0]]
    dates_h2o=dataseth2o[pandas_fieldname[0]]

    if not np.array_equal(dates_h2o,dates_o3 ):
        print "Miss match of the dates"
        os._exit(1)
        
        
    dataseto3.describe()
    dataseth2o.describe()
    
    # read O3 data    
    dates_data_o3=np.array(dataseto3[pandas_fieldname[0]])
    data_month_aver_o3=np.array(dataseto3[pandas_fieldname[1]])
    avo3=data_month_aver_o3.mean()
    data_month_sdev_o3=np.array(dataseto3[pandas_fieldname[4]])
    data_month_ct_o3=np.array(dataseto3[pandas_fieldname[2]])
    data_month_err_o3=np.array(dataseto3[pandas_fieldname[3]])
    data_month_p1std_o3=data_month_aver_o3+data_month_sdev_o3
    data_month_m1std_o3=data_month_aver_o3-data_month_sdev_o3
    data_month_min_o3=np.array(dataseto3[pandas_fieldname[5]])
    data_month_max_o3=np.array(dataseto3[pandas_fieldname[6]])
     
     # read H2O data
    dates_data_h2o=np.array(dataseth2o[pandas_fieldname[0]])
    data_month_aver_h2o=np.array(dataseth2o[pandas_fieldname[1]])
    avh2o=data_month_aver_h2o.mean()
    data_month_sdev_h2o=np.array(dataseth2o[pandas_fieldname[4]])
    data_month_ct_h2o=np.array(dataseth2o[pandas_fieldname[2]])
    data_month_err_h2o=np.array(dataseth2o[pandas_fieldname[3]])
    data_month_p1std_h2o=data_month_aver_h2o+data_month_sdev_h2o
    data_month_m1std_h2o=data_month_aver_h2o-data_month_sdev_h2o
    data_month_min_h2o=np.array(dataseth2o[pandas_fieldname[5]])
    data_month_max_h2o=np.array(dataseth2o[pandas_fieldname[6]])    

    # No Ozone for a pure scattering atmosphere
    # No PWV for a pure scattering atmosphere

    # airmass indexes defined for the whole production from z=1 to z=3
    airmasses_indexes=np.arange(10,31,1)
    
    
    # build the part 1 of filename
    BaseFilename_part1=Prog+'_'+Obs+'_'+Rte+'_'
    
    


    # Set up type of run
    runtype='no_scattering' #'no_scattering' #aerosol_special #aerosol_default# #'clearsky'#     
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
    if Mod == 'lt':
        molmodel='lowtran'
    if Mod == 'kt':
        molmodel='kato'
    if Mod == 'k2':
        molmodel='kato2'
    if Mod == 'fu':
        molmodel='fu'    
    if Mod == 'cr':
        molmodel='crs'     
        
        
        
        
        
        
    	  
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
       
        # manage input and output directories
        TOPDIR2=TOPDIR+'/'+Rte+'/'+atmkey+'/'+Proc+'/'+Mod
        ensure_dir(TOPDIR2)
        
        
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
           
        # 2) LOOP on Date entries 
        for idx,the_date in np.ndenumerate(dates_data_o3):
            print idx
            the_year_str=YXX+the_date.split('-')[0]
            the_month_str=MXX+the_date.split('-')[1]
            
            TOPDIR3=TOPDIR2+'/'+the_year_str+'/'+the_month_str
            ensure_dir(TOPDIR3)
           
#           ozon_val=float(ozfileindex*10)
#           ozon_str='O3 '+str(ozon_val)+ ' DU'
          
            INPUTDIR=TOPDIR3+'/'+'in'
            ensure_dir(INPUTDIR)
            OUTPUTDIR=TOPDIR3+'/'+'out'
            ensure_dir(OUTPUTDIR)          
          
          
#           ozon_val=float(ozfileindex*10)
#           ozon_str='O3 '+str(ozon_val)+ ' DU'          
       
            #3) LOOP on average , sdev, min,max       
            for variation in atm_variations:
               if variation == 'aver':
                   ozon_val=data_month_aver_o3[idx]
                   pwv_val=data_month_aver_h2o[idx]
                   
               elif variation == 'std1':
                   ozon_val=data_month_p1std_o3[idx]
                   pwv_val=data_month_p1std_h2o[idx]                  
               elif variation == 'std2': 
                   ozon_val=data_month_m1std_o3[idx]
                   pwv_val=data_month_m1std_h2o[idx]            
               elif variation == 'min': 
                   ozon_val=data_month_min_o3[idx]
                   pwv_val=data_month_min_h2o[idx]                   
               elif variation == 'max':
                   ozon_val=data_month_max_o3[idx]
                   pwv_val=data_month_max_h2o[idx]
               else:
                   print "Bad Variation"
                   os._exit(1)
               
               ozon_str='O3 '+str(ozon_val)+ ' DU'  
               pwv_str='H2O ' +str(pwv_val) + ' MM'
       
       
          
           # 4) LOOP ON AIRMASSES 
               for index,amfileindex in np.ndenumerate(airmasses_indexes):
                    
        
                    # airmass
                    airmass=float(amfileindex)/10.
            
                    
            
                    BaseFilename=BaseFilename_part1+atmkey+'_'+Proc+'_'+Mod+'_z'+str(amfileindex)+'_'+the_year_str+'_'+the_month_str+'_'+variation
                    
                    
                    verbose=True
                    uvspec = UVspec.UVspec()
                    uvspec.inp["data_files_path"]  =  libradtranpath+'data'
                
                    uvspec.inp["atmosphere_file"] = libradtranpath+'data/atmmod/'+atmosphere+'.dat'
                    uvspec.inp["albedo"]           = '0.2'
            
            
            
                    uvspec.inp["rte_solver"] = rte_eq
            
                    if Mod == 'rt':
                        uvspec.inp["mol_abs_param"] = molmodel + ' ' + molresol
                    else:
                        uvspec.inp["mol_abs_param"] = molmodel
                    
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
     
                    # set up the ozone and pwv value               
                    uvspec.inp["mol_modify"] = ozon_str 
                    uvspec.inp["mol_modify2"] = pwv_str     
                
                    uvspec.inp["output_user"] = 'lambda edir'
                    uvspec.inp["altitude"] = OBS_Altitude   # Altitude LSST observatory
                    uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_1.0nm.dat'
                    #uvspec.inp["source"] = 'solar '+libradtranpath+'data/solar_flux/kurudz_0.1nm.dat'
                    uvspec.inp["sza"]        = str(sza)
                    uvspec.inp["phi0"]       = '0'
                    uvspec.inp["wavelength"]       = '250.0 1200.0'
                    uvspec.inp["output_quantity"] = 'reflectivity' #'transmittance' #
#                   uvspec.inp["verbose"] = ''
                    uvspec.inp["quiet"] = ''

  

                    if "output_quantity" in uvspec.inp.keys():
                        outtextfinal=outtext+'_'+uvspec.inp["output_quantity"]

           
            
                    inputFilename=BaseFilename+'.INP'
                    outputFilename=BaseFilename+'.OUT'
                    inp=os.path.join(INPUTDIR,inputFilename)
                    out=os.path.join(OUTPUTDIR,outputFilename)
                    
            
                    uvspec.write_input(inp)
                    uvspec.run(inp,out,verbose,path=libradtranpath)

