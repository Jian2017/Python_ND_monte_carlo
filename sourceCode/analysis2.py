#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 11:52:00 2018

@author: jian
"""

from ANALYSIS import bestANDerror
import matplotlib.pyplot as plt
import numpy as np


fileName="MC22"

out1,out2=bestANDerror(fileName+".hdf5")


# warnming , this is only hold for 0+1 D problem

plt.plot(out1,'.-')


# 6 comes from estimation of correlation time
out2=out2*6
plt.imshow(out2[:10,:10])
plt.colorbar()

print(out2[0,0]/out1[0])


np.save(fileName+"best",out1)
np.save(fileName+"error",out2)

