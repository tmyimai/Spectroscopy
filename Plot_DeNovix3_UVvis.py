# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os, glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy
import pandas as pd
import itertools

### (1) Read the data ###
### Indicate the file
dt = os.path.join('20251015.csv')
skip_cols = 25 # Indicate how many columns are found up to the spectral data
starting_WL = 190 # Indicate the first WL in the spectral region
##-------------------------------------------------
sp = pd.read_csv(dt)
samples = list(sp['Sample Name'])
Absls = list(sp['Abs 1'])

###--- (2) Decide the data ---###
i = 0
for _ in samples:
    print('{}: {} (A520 = {})'.format(i, samples[i], Absls[i]))
    i = i+1

pltl1 = [0,1,2,6,3,4]
pltl2 = [0,5,6]
pltl3 = [0,1,3,2,4,6]
pltl = [pltl1, pltl2, pltl3]
titles = ['20251015_Effect of xylose', 'Glucose and xylose', '20251015_Effect of xylose_2']
y_max = [1.2,1.2,1.2]

###--- (3) Plot the raw data ---###
##---- Indicate the plot parameters
xmin = 400; xmax= 750; xint= 100
label_min = 400; label_max = 751
col_start = (xmin-starting_WL)+skip_cols
col_end = col_start+(xmax-xmin)

##---- Make plots ---##
x = list(range(xmin, xmax+1, 1))
x2 = list(range(col_start, col_end+1, 1))

i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title(titles[i], fontsize=11)
    for j in pltl[i]:
        y = sp.iloc[j,x2]
        ax1.plot(x, y, label = '{} (A520={})'.format(samples[j], Absls[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10, ncol=1)
    ax1.set_xlim(xmin, xmax)
    ax1.set_xticks(np.arange(label_min, label_max, xint))
    ax1.set_ylim(-0.05, y_max[i])
    ax1.tick_params(labelsize = 11)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('Wavelength (nm)', fontsize=14)
    ax1.set_ylabel('Absorbance', fontsize=14, labelpad=2)
    fig.savefig('{}.png'.format(titles[i]), dpi=300, bbox_inches='tight')
    i = i+1

###--- (4) Plot the smoothed data ---###
w1 = 5 # window for the Savitzku-Golay filter
i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title('{} (smoothed)'.format(titles[i]), fontsize=11)
    for j in pltl[i]:
        y = np.array(sp.iloc[j,x2], dtype = float)
        y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
        ax1.plot(x, y_sm, label = '{} (A280={})'.format(samples[j], Absls[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10, ncol=1)
    ax1.set_xlim(xmin, xmax)
    ax1.set_xticks(np.arange(label_min, label_max, xint))
    ax1.set_ylim(-0.05, y_max[i])
    ax1.tick_params(labelsize = 11)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('Wavelength (nm)', fontsize=14)
    ax1.set_ylabel('Absorbance', fontsize=14, labelpad=2)
    fig.savefig('{}_smoothed.png'.format(titles[i]), dpi=300, bbox_inches='tight')
    i = i+1

# ###--- Smoothing and 2nd derivitization ---###
# i = 0
# for _ in samples:
#     y = np.array(sp2[i][20:121], dtype = float)
#     y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
#     y_sm_2Der = np.gradient(np.gradient(y_sm))
#     i = i+1
