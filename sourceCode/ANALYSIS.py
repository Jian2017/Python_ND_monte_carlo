#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 11:15:52 2018

@author: jian
"""
import h5py
import numpy as np
#import matplotlib.pyplot as plt



# for any dimension


def readm(MCfile):
    f = h5py.File(MCfile, 'r')
    m=f['bigFFT'][...]
    f.close()
    return m

"""
def readm2(MCfile):

    f = h5py.File(MCfile, 'r')
    m=f['m2'][...]
    f.close()
    return m
"""


def readm1(MCfile):

    f = h5py.File(MCfile, 'r')
    m=f['m1'][...]
    f.close()
    return m

def autocorr(x):
    r2=np.fft.ifft(np.abs(np.fft.fft(x))**2).real
    c=(r2/x.shape-np.mean(x)**2)/np.std(x)**2
    return c[:len(x)//2]










# for 0+1 D only

def bestANDerror0(MCfile):#,Datafile):

    f = h5py.File(MCfile, 'r')
    m=f['bigFFT'][200000:][...]
    f.close()
    
    m_mean=np.mean(m,axis=0)
    

    m_S=np.std( m,axis=0 )
    # m.shape[0] is Monte Carlo step time
    # m.shape[1] is the imaginary time
    # m.shape[2] ... spacial

    Ntrunk=m.shape[1]//2
    
    print(Ntrunk)


    output1=m_mean[:Ntrunk]

    output2=m_S[:Ntrunk]/m.shape[0]
    
    #np.save(Datafile,output1)
    
    return output1, output2      
        
def bestANDerror(MCfile):#,Datafile):
    f = h5py.File(MCfile, 'r')
    m=f['bigFFT'][...]
    f.close()    
    Ns=m.shape
    Nrest=1
    for i in range(1,len(Ns)):
        Nrest=Nrest*Ns[i]


    m_mean=np.mean(m,axis=0)
    
    twoDmatrix=np.reshape(m, ((Ns[0],)+(Nrest,)) )

    m_S=np.reshape( np.cov(np.transpose(twoDmatrix) ), Ns[1:]+Ns[1:] )
    # np.cov can not take large matrix, sorry!

    Ntrunk=Ns[1]//2


    output1=m_mean[:Ntrunk,...]

    output2=m_S[:Ntrunk,:Ntrunk]/Ns[0]
    
    #np.save(Datafile,output1)
    
    return output1, output2
