# coding: utf-8
import sys, os
#sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import matplotlib.pyplot as plt
#from dataset.mnist import load_mnist
from deep_convnet_clcls import DeepConvNet
from common.trainer import Trainer
import clcls_func
from datetime import datetime, timedelta
import myfunc.util as util
#from numpy import ma
from numpy import *
import copy

iDTime  = datetime(2008,1,1,0,30)
eDTime  = datetime(2008,1,1,3,0)
dDTime  = timedelta(seconds=60*60)
lDTime  = util.ret_lDTime(iDTime,eDTime,dDTime)
lDTime_train = lDTime[::2]
lDTime_test  = lDTime[1::2]
#(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)
x_train = clcls_func.load_match_batch(lDTime_train, "IR")
t_train = clcls_func.load_match_batch(lDTime_train, "ctype_count")



#-- test ----
t_train  = t_train[52:55]
l        = copy.copy(t_train)
#
#
denom   = ma.masked_equal(t_train[:,1:].sum(axis=1).astype(float32), 0)

t_train[:,1:] = (t_train[:,1:] / denom.reshape(-1,1)).filled(0)

t_train[:,0] = denom.mask.astype(float32)

s= t_train.sum(axis=1)
for i in range(len(s)):
    print i, t_train[i], l[i]
    
#
