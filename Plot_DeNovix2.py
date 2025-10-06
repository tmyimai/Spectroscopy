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
dt = os.path.join('.', '20250929_exlx015.csv')
sp = pd.read_csv(dt)
samples = list(sp['Sample Name'])
A280s = list(sp['A280'])

###--- (2) Decide the data ---###
i = 0
for _ in samples:
    print('{}: {} (A280 = {})'.format(i, samples[i], A280s[i]))
    i = i+1

###--- Indicate the data to plot ---###
pltl1 = [0,1,2,3,4]
pltl2 = [0,5,6,7,8]
# pltl3 = [0,2,6]
# pltl = [pltl1]
pltl = [pltl1, pltl2]
titles = ['WT', 'D82N']

# The y-scale for plotting
y_max = [12.5,25]

###--- (3) Plot the raw data ---###
xmin = 220; xmax= 320; xint= 10
label_min = 220; label_max = 321
x = list(range(xmin, xmax+1, 1))
x2 = list(range(xmin-200, xmax-199, 1))

i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title(titles[i], fontsize=11)
    for j in pltl[i]:
        y = sp.iloc[j,x2]
        ax1.plot(x, y, label = '{} (A280={})'.format(samples[j], A280s[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=8, ncol=1)
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
w1 = 9 # window for the Savitzku-Golay filter
i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title('{} (smoothed)'.format(titles[i]), fontsize=11)
    for j in pltl[i]:
        y = np.array(sp.iloc[j,x2], dtype = float)
        y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
        ax1.plot(x, y_sm, label = '{} (A280={})'.format(samples[j], A280s[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=7, ncol=1)
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
