from numpy import *
from datetime import datetime, timedelta
import myfunc.util
import numpy as np
from collections import deque
import os

def load_match(DTime,vartype="IR"):
    # vartype == "IR","latlon","ctype_count"
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour
    Mnt     = DTime.minute
    baseDir ="/home/utsumi/mnt/wellshare/CLCLS/MATCH"
    srcDir  = baseDir + "/%04d/%02d%02d"%(Year,Mon,Day)
    srcPath = srcDir  + "/%s.%02d.%02d.npy"%(vartype,Hour,Mnt)
    if os.path.exists(srcPath):
        return np.load(srcPath)
    else:
        return array([])

def load_match_batch(lDTime,vartype="IR"):
    ltmp = deque([])
    for DTime in lDTime:
    
        Dat = load_match(DTime, vartype)
        if Dat != array([]):
            ltmp.append(Dat)
        else:
            print "Skip",DTime
    return concatenate(ltmp, axis=0)
