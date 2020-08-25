#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 22:36:42 2018

@author: bmoseley
"""

import numpy as np

import sys
sys.path.insert(0, '../shared_modules/')
import processing_utils


class C:
    
    if 'linux' in sys.platform.lower(): ROOT_DIR = "/data/greypartridge/not-backed-up/aims/aims17/bmoseley/DPhil/Mini_Projects/DIP/forward_seisnets_paper/generate_data/"
    else: ROOT_DIR = ""
    
    VELOCITY_DIR = ROOT_DIR + "velocity/layers/"
    
    N_VELS = 50000
    
    REFLECTIVITY_SHAPE = (1, 512)
    DELTAT = 0.002
    SOURCE_Zi = 14 # depth of source (samples)
    DELTAZ = 5.# depth interval (m)

c = C()

# parse to flat binary
for i in range(c.N_VELS):


    # load velocity data from .npy
    # **CUT TOP SECTION** so that source is effectively at Z=0
    # only take first trace
    v_d = np.copy(np.load(c.VELOCITY_DIR+"velocity_%.8i.npy"%(i))[0,c.SOURCE_Zi:])
    
    # get r_t input
    r_t = np.zeros(c.REFLECTIVITY_SHAPE, dtype=np.float32)
    r_t[0,:] = processing_utils.get_1d_reflectivity_model(v_d, qc=False, srate=c.DELTAT, DZ=c.DELTAZ, NSTEPS=c.REFLECTIVITY_SHAPE[1])
    r_t[0,0] += 1 # add direct arrival
    np.save(c.VELOCITY_DIR+"reflectivity_%.8i.npy"%(i), r_t)
    
    if (i+1)%1000 == 0: print(i+1)
