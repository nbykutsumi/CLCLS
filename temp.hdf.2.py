import os, sys
from numpy import *
from pyhdf import HDF, VS, SD
from datetime import datetime, timedelta

srcPath = "/home/utsumi/mnt/wellshare/CloudSat/2B-CLDCLASS.P_R04/2014/100/2014100023333_42291_CS_2B-CLDCLASS_GRANULE_P_R04_E06.hdf"

#srcPath = "/home/utsumi/mnt/wellshare/CloudSat/2B-CLDCLASS.P_R04/2014/100/2014100041226_42292_CS_2B-CLDCLASS_GRANULE_P_R04_E06.hdf"

#varName = "cloud_scenario"

h4 = SD.SD(srcPath)
tmp2=h4.select('cloud_scenario')

# -- time ---
Year, DOY = map(int, srcPath.split("/")[-3:-1])
varName = "UTC_start"
#instVar = h4.select(varName)
#sUTC    = instVar
#sDTime  = datetime(Year,1,1,0) + timedelta(days=DOY-1)\
#                               + timedelta(seconds=sUTC)
#instVar.detach()
#
#
#
# -- ptime ---
#varName = "Profile_time"
#instVar = vs.attach(varName)
#tmp     = instVar
#pTIME   = array(instVar[:]).reshape(1,-1)[0]
#instVar.detach()
#pDTime  =  sDTime + \
#         + array([timedelta(seconds = sec)
#                          for sec in pTIME])
#
#print pDTime
#
#
#vs.end()
#f.close()
#
#
