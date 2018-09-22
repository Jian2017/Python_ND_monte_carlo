#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 21:31:49 2018

@author: jian
"""
from ANALYSIS import   readm1
import numpy as np

import matplotlib.pyplot as plt




def binderRatio(x):
    R2=np.mean(x**4)/np.mean(x**2)**2
    return 1.5-R2/2

def binderRatioError(m1,bins):
    BR=np.zeros(bins)

    N=m1.shape[0]//bins
    
    res=m1.shape[0]%bins

    for i in range(bins):
        BR[i]=binderRatio(m1[res+i*N:res+(i+1)*N])

    #plt.hist(BR)

    return np.mean(BR), np.std(BR)/np.sqrt(bins)


    
x=np.zeros(15)    
B_best=np.zeros(15)    
B_error=np.zeros(15)


cut=9
for i in range(cut,15):
    filename="MC"+str(i)+".hdf5"
    m1=readm1(filename)
    x[i]=i/10.0
    B_best[i],B_error[i]=binderRatioError(m1,20)
    
plt.figure()
plt.errorbar(x[cut:],B_best[cut:],yerr=B_error[cut:],fmt='.-')

