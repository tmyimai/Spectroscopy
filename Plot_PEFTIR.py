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

from specio import specread
from sklearn.decomposition import PCA
###===Indicate the directories
datadir = os.path.join('.', '20231127')
opdir = datadir
measurement = 'CESEC071'

###=========================================================================
### (1) Read the data ###
##### Use "try" for the case of unreadable data, which will be listed in errl
fl = glob.glob(os.path.join(datadir,'*.sp'))
i=0; j=0; fnl =[]; fd ={}; rmfl =[]; errl =[]
for s in fl:
   try:
       spectra = specread(s)
       if np.min(0.01*spectra.amplitudes) < 0.2:
           print("{} is not included".format(s))
           rmfl.append(s)
           j = j+1
       else:
           print("{} is OK".format(s))
           IR = pd.DataFrame() 
           fn = os.path.basename(s)[:-3]
           fnl.append(fn)
           IR['wavenumber'] = spectra.wavelength
           T = 0.01*spectra.amplitudes
           IR['percent Transmittance'] = T
           IR['Absorbance'] = -1*np.log10(T)
           fd[fn] = IR
           i = i+1
   except:
        f = os.path.basename(s)
        print("Cannot read {}".format(f))
        errl.append(f)
print('\nThe list of files not included')
i1 = 0
for _ in rmfl:
    print('{}: {}'.format(i+1,rmfl[i1]))
    i1 = i1+1
print('Files read: {}\nFiles NOT read: {}\n'.format(i, j))

###=========================================================================
###--- (2) Smoothing ---###
w1 = 9 # window for the Savitzku-Golay filter
for s in fnl:
    y = np.array(fd[s]['Absorbance'], dtype = float)
    y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
    fd[s]['Absorbance_SG_Smoothed'] = y_sm
    fd[s]['2ndDer_SG'] = np.gradient(np.gradient(y_sm))

###=========================================================================
###--- (3) Plot all the data in the directory---###
title1 = 'Smoothed data'
xmin = 400; xmax= 4000; xint= 500
label_min = 1000; label_max = 4001
###----------------------------------
fig = plt.figure(figsize = (8,6), dpi = 200)
ax1 = fig.add_subplot(111)
ax1.set_title(title1, fontsize=12)
y_scale = -1
for s in fnl:
    x = fd[s]['wavenumber']
    y = fd[s]['Absorbance_SG_Smoothed']
    y_max = np.max(y)
    if y_scale < y_max:
        y_scale = y_max
    else:
        pass
    ax1.plot(x, y, label = '{}'.format(s))
ax1.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0, fontsize=7, ncol=2)
ax1.set_xlim(xmin, xmax)
ax1.invert_xaxis()
ax1.set_xticks(np.arange(label_min, label_max, xint))
ax1.set_ylim(-0.005, 1.1*y_scale)
ax1.tick_params(labelsize = 8)
ax1.minorticks_on()
ax1.grid(which='major', axis = 'x', color = 'gray')
ax1.grid(which='minor', axis = 'x', color = 'lightgray')
ax1.set_xlabel('Wave number (cm$^{-1}$)', fontsize=10)
ax1.set_ylabel('Absorbance', fontsize=10,labelpad=2)

opf3 = os.path.join(opdir, 'AllSpectra_{}.png'.format(measurement))
fig.savefig(opf3, dpi=300, bbox_inches='tight')

###=========================================================================
###--- (3B) Plot the selected data ---###
###--- Select the data in pltl
i=0
for _ in fnl:
    print('{}: {}'.format(i, fnl[i]))
    i = i+1

opname = 'CESEC071'
pltl = [5,2,3,4]

labels =['EV#51 (WT)', 'EV#345 (Y15-BcsA_d3-6)', 'EV#346 (BcsA_d740-754-Y15)', 'EV#347 (BcsB-Y15)']
color_list =['red', 'orange', 'green','blue'] 

###--- Plot the data
title1 = '{}_smoothed'.format(opname)
xmin = 500; xmax= 4000; xint= 500
label_min = 1000; label_max = 4001
###----------------------------------
fig = plt.figure(figsize = (8,6), dpi = 300)
ax1 = fig.add_subplot(111)
ax1.set_title(title1, fontsize=12)
i=0
for _ in pltl:
    j = i*1
    s = fnl[pltl[i]]
    x = fd[s]['wavenumber']
    y = fd[s]['Absorbance_SG_Smoothed']
    scale= np.max(fd[s]['Absorbance_SG_Smoothed'])-np.min(fd[s]['Absorbance_SG_Smoothed'])
    y1 = y/scale + j
    ax1.plot(x, y1, label = labels[i], color = color_list[i])
    i = i+1
ax1.legend(bbox_to_anchor=(0.01, 0.99), loc='upper left', borderaxespad=0, fontsize=7, ncol=2)
ax1.set_xlim(xmin, xmax)
ax1.invert_xaxis()
ax1.set_xticks(np.arange(label_min, label_max, xint))
ax1.set_yticks([])
ax1.set_ylim(-0.05,4.5)
ax1.tick_params(labelsize = 8)
ax1.minorticks_on()
ax1.grid(which='major', axis = 'x', color = 'gray')
ax1.grid(which='minor', axis = 'x', color = 'lightgray')
ax1.set_xlabel('Wave number (cm$^{-1}$)', fontsize=10)
ax1.set_ylabel('Absorbance', fontsize=10, labelpad=2)

opf3 = os.path.join('.', 'SmoothedPlot_{}.png'.format(opname))
fig.savefig(opf3, dpi=300, bbox_inches='tight')
