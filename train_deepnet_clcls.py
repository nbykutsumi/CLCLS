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

iDTime  = datetime(2008,1,1,0,30)
eDTime  = datetime(2008,2,28,23)
dDTime  = timedelta(seconds=60*60)
lDTime  = util.ret_lDTime(iDTime,eDTime,dDTime)
lDTime_train = lDTime[::2]
lDTime_test  = lDTime[1::2]
#(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)
x_train = clcls_func.load_match_batch(lDTime_train, "IR")
t_train = clcls_func.load_match_batch(lDTime_train, "ctype_count")
x_test  = clcls_func.load_match_batch(lDTime_test, "IR")
t_test  = clcls_func.load_match_batch(lDTime_test, "ctype_count")




#network = DeepConvNet()  
#trainer = Trainer(network, x_train, t_train, x_test, t_test,
#                  epochs=20, mini_batch_size=100,
#                  optimizer='Adam', optimizer_param={'lr':0.001},
#                  evaluate_sample_num_per_epoch=1000)
#trainer.train()
#
## パラメータの保存
#network.save_params("deep_convnet_params.pkl")
#print("Saved Network Parameters!")
