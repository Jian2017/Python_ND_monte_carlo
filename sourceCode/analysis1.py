#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 17:04:32 2018

@author: jian
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt





from ANALYSIS import   readm1, autocorr


m1=readm1("MC10.hdf5")


r=autocorr(m1**2)

'''
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(r[:100],'.')
fig.savefig('test.png')
'''

plt.plot(r[:100],'.')
plt.show()

