import matplotlib
matplotlib.use("Agg")

import numpy as np
import os, sys
from numpy import *
from datetime import datetime, timedelta
from clcls_fsub import *

import myfunc.util          as util
import myfunc.IO            as IO
import myfunc.IO.CloudSat   as CloudSat
import myfunc.IO.CloudSat.util as CSutil
import myfunc.IO.MERGIR     as MERGIR


import matplotlib.pyplot as plt
from   mpl_toolkits.basemap import Basemap


iDTime  = datetime(2008,1,1,3,0)
#iDTime  = datetime(2008,2,2,14,0)
#eDTime  = datetime(2008,12,31,23,30)
eDTime  = datetime(2008,1,1,3,0)

#iDTime  = datetime(2008,4,11,7,30)
#eDTime  = datetime(2008,4,11,23,30)



dDTime  = timedelta(seconds=60*30)
lDTime  = util.ret_lDTime(iDTime,eDTime,dDTime)

lNoDTime= util.ret_lDTime(datetime(2008,1,18,16,30),datetime(2008,1,22,18,30),dDTime)
lNoDTime= lNoDTime + util.ret_lDTime(datetime(2008,5,23),datetime(2008,5,28),dDTime)

lDTime  = [DTime for DTime in lDTime if DTime not in lNoDTime]

#-- CloudSat ----
prdLev    = "2B"
prdName   = "CLDCLASS"
prdVer    = "P_R04"
varName   = {"GEOPROF"  :"Radar_Reflectivity"
            ,"CLDCLASS":"cloud_scenario"
            }[prdName]

cs      = CloudSat.CloudSat(prdLev, prdName, prdVer)
nbin    = cs.nbin
liz     = arange(nbin)
lz      = arange(-4810, 24950+1, 240) /1000. # [km]
BBox    = [[-60,-180],[60,180]]

dcsName      = CSutil.ret_dclName()
dcsShortName = CSutil.ret_dclShortName()
lcsid        = sort(dcsName.keys())


dy,dx   = 3,3   # window size = 2*dy+1, 2*dx+1
#-- MERGED IR ---
ir      = MERGIR.MERGIR()
LatIR   = ir.Lat
LonIR   = ir.Lon
nyIR    = len(LatIR)
nxIR    = len(LonIR)

LatBnd  = (LatIR[1:]+LatIR[:-1])*0.5
LatBnd  = r_[-60, LatBnd, 60]

LonBnd  = (LonIR[1:]+LonIR[:-1])*0.5
LonBnd  = r_[-180, LonBnd, 180]
#----------------


a2IR0   = ones([nyIR+2*dy,nxIR+2*dx],int8)*(-128)
a2IR1   = ones([nyIR+2*dy,nxIR+2*dx],int8)*(-128)
a2IR2   = ones([nyIR+2*dy,nxIR+2*dx],int8)*(-128)

for DTime in lDTime:
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour
    Mnt     = DTime.minute    
    #-- load IR --
    DTime0  = DTime - timedelta(seconds=60*30)
    DTime1  = DTime
    DTime2  = DTime + timedelta(seconds=60*30)

    a2IR0[dy:-dy,dx:-dx] = (ir.load_30min(DTime0) -200).astype(int8).filled(-128)
    a2IR1[dy:-dy,dx:-dx] = (ir.load_30min(DTime1) -200).astype(int8).filled(-128)
    a2IR2[dy:-dy,dx:-dx] = (ir.load_30min(DTime2) -200).astype(int8).filled(-128)

    #-- load CloudSat --
    dDTime15 = timedelta(seconds=60*15)

    try:
        csobt  = cs(varName, DTime-dDTime15, DTime+dDTime15, BBox)
    except IOError:
        print "-"*50
        print "No granule:", DTime-dDTime15, DTime+dDTime15
        print "Skip"
        print "-"*50
        continue
    #csobt  = cs(varName, iDTime, eDTime, BBox)   # test
    if len(csobt.data)==0:
        print "-"*50
        print "No date for", DTime-dDTime15, DTime+dDTime15
        print "Skip"
        print "-"*50
        continue
    a2prof = cs.Resolve_CloudScenario(csobt.data[0]).astype(int)

    #-- count ----
    a2count = empty([a2prof.shape[0],9],int8)
    for i,csid in enumerate(lcsid):
        try:
            a2count[:,i]= ma.masked_equal(a2prof,csid).mask.sum(axis=1)
        except ValueError:
            a2count[:,i]=0

    #-- track X & Y -----
    #LatObt  = csobt.lat
    #LonObt  = csobt.lon
    LatObt  = csobt.lat[0]
    LonObt  = csobt.lon[0]

    a1y,a1x = clcls_fsub.ret_pyyx_mergir(LatBnd, LonBnd, LatObt, LonObt)

    #-- mask edge region ----
    print "Bef",len(a1y),len(a1x)
    nlenOrg    = len(a1y)
    a1y_mask   = ma.masked_outside(a1y, dy, nlenOrg-dy)
    a1x_mask   = ma.masked_outside(a1x, dx, nlenOrg-dx)
    a1mask     = a1y_mask.mask + a1x_mask.mask

    
    if type(a1mask) !=np.bool_:
        a1y        = a1y[~a1mask]
        a1x        = a1x[~a1mask]
    
        LatObt     = LatObt[~a1mask]
        LonObt     = LonObt[~a1mask]

        a2count    = a2count[~a1mask,:]
    
    nlenAft = len(a1x)
    #-- Extract IR-observations --
    if nlenAft ==0:
        #a4irout  = empty([],int8)
        #a2latlon = empty([],int8)
        #a2count  - empty([],int8)
        print "-"*50
        print "No observations over the domain"
        print "Skip"
        print "-"*50
        continue
    else:
        a4irout  = empty([nlenAft, 3,2*dy+1,2*dx+1],int8)
        a2latlon = empty([nlenAft, 2], float32)
    
        X,Y = meshgrid(nxIR, nyIR)
    
        for iy,idy in enumerate(range(-dy,dy+1)):
            for ix,idx in enumerate(range(-dx,dx+1)):
                a4irout[:,0,iy,ix] = a2IR0[a1y+idy+dy, a1x+idx+dx]
                a4irout[:,1,iy,ix] = a2IR1[a1y+idy+dy, a1x+idx+dx]
                a4irout[:,2,iy,ix] = a2IR2[a1y+idy+dy, a1x+idx+dx]

        #-- lat & lon ---
        a2latlon[:,0] = LatObt 
        a2latlon[:,1] = LonObt 

        #-- save --------
        rootDir  = "/home/utsumi/mnt/wellshare/CLCLS/MATCH"
        outDir   = rootDir + "/%04d/%02d%02d"%(Year,Mon,Day)
        util.mk_dir(outDir)

        irPath   = outDir + "/IR.%02d.%02d.npy"%(Hour,Mnt)
        np.save(irPath, a4irout)

        latlonPath = outDir + "/latlon.%02d.%02d.npy"%(Hour,Mnt)
        np.save(latlonPath, a2latlon)


        ctypePath = outDir + "/ctype_count.%02d.%02d.npy"%(Hour,Mnt)
        np.save(ctypePath, a2count)

        print ""
        print "---------SAVE---------------"
        print irPath
        print "----------------------------"
        print ""


    ##----- figure ----------
    ##dLon  = (LonIR[1:]-LonIR[:-1]).mean()
    ##a1xtmp= floor((array(LonObt)-(-180))/dLon)


    #ny    = len(LatIR)
    #nx    = len(LonIR)
    #a2dat = zeros([ny,nx])
    #a2dat[a1y,a1x]=1
    #print "*"*50
    #print "ny,nx=",ny,nx
    #print "*"*50

    #fig = plt.figure()
    #ax  = fig.add_axes([0.1,0.1,0.8,0.8])
    #M = Basemap(resolution="l", llcrnrlat=-90,llcrnrlon=-180, urcrnrlat=90, urcrnrlon=180, ax=ax)
    ##M = Basemap(resolution="l", llcrnrlat=-60,llcrnrlon=-40, urcrnrlat=0, urcrnrlon=0, ax=ax)
    #M.drawcoastlines()

    #X,Y = meshgrid(LonBnd, LatBnd)
    #im = M.pcolormesh(X,Y,a2dat)
    #figPath = "/home/utsumi/temp/pict/temp1.png"
    #plt.savefig(figPath)
    #print figPath

    ##-- plot ----
    #fig = plt.figure()
    #ax  = fig.add_axes([0.1,0.1,0.8,0.8])
    #ax.plot(a1x,"o")
    #sPath = "/home/utsumi/temp/pict/X.png"
    #plt.savefig(sPath)
    #
    #fig = plt.figure()
    #ax  = fig.add_axes([0.1,0.1,0.8,0.8])
    #ax.plot(a1y,"o")
    #sPath = "/home/utsumi/temp/pict/Y.png"
    #plt.savefig(sPath)
    #
    #aMnt= array([(dtime - iDTime).total_seconds() for dtime in csobt.dtime[0]])
    #fig = plt.figure()
    #ax  = fig.add_axes([0.1,0.1,0.8,0.8])
    #ax.plot(aMnt)
    #sPath = "/home/utsumi/temp/pict/Mnt.png"
    #plt.savefig(sPath)
    #

    #sys.exit()
    


