#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 15:42:18 2018

@author: jian

get rough estimation of error, correlation steps

"""

from MONTECARLO import IsingND


for i in range(15):
    filename="MC"+str(i)+".hdf5"
    p=IsingND((32,),(1.0,),i/10.0)
    p.run(filename,200,1000,1)


    

"""
"""

