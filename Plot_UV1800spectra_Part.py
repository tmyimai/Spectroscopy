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

### (0) Indicate the parameters
opf = os.path.join('20251023.xlsx')

### (1) Read the data ###
### Indicate the file
fl = glob.glob('*.csv')
i = 0
for _ in fl:
    dataname=fl[i][:-4]
    if i==0:
        data = pd.read_csv(fl[i], skiprows=1)
        data.rename(columns={'Abs':dataname}, inplace=True)
    else:
        sp = pd.read_csv(fl[i], skiprows=1)
        data[dataname]=sp['Abs']
    i = i+1
data.to_excel(opf) # Output as an Excel file
column_list = data.columns.tolist() # Prepare the list of the column name

###--- (2) Decide the data ---###
###=== (2.1)List the data
i = 0
for _ in column_list:
    print('{}: {}'.format(i, column_list[i]))
    i = i+1
print('-----\nSpectral range = {} - {} nm'.format(np.min(data['WL/nm']), np.max(data['WL/nm'])))

##=== (2.2) Indicate the files to plot
pltl1 = [1,3,2]
pltl2 = [1,4,6,5]
# pltl3 = [1,6,4,5,2]
pltl = [pltl1, pltl2]
titles = ['Standard (GlcA)', 'Assay']
y_max = [2, 2]

###--- (3) Plot the raw data ---###
##---- Indicate the plot parameters
x_start = 450 # Starting wavelengh
x_end = 700 # # Ending wavelengh
x_int= 50

#-------------------------------------------------
label_min = x_start; label_max = x_end+1
mask = (data['WL/nm'] >= x_start) & (data['WL/nm'] <= x_end)
region = data[mask]

##---- Make plots ---##
i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title(titles[i], fontsize=11)
    for j in pltl[i]:
        d = column_list[j]
        x = region['WL/nm']
        y = region[d]
        ax1.plot(x, y, label = '{}'.format(column_list[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10, ncol=1)
    ax1.set_xlim(x_start, x_end)
    ax1.set_xticks(np.arange(label_min, label_max, x_int))
    ax1.set_ylim(-0.05, y_max[i])
    ax1.tick_params(labelsize = 11)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('Wavelength (nm)', fontsize=14)
    ax1.set_ylabel('Absorbance', fontsize=14, labelpad=2)
    fig.savefig('{}_partial.png'.format(titles[i]), dpi=300, bbox_inches='tight')
    i = i+1

###--- (4) Plot the smoothed data ---###
w1 = 9 # window for the Savitzku-Golay filter
i = 0
for _ in pltl:
    fig = plt.figure(figsize = (8,6), dpi = 200)
    ax1 = fig.add_subplot(111)
    ax1.set_title('{} (smoothed)'.format(titles[i]), fontsize=11)
    for j in pltl[i]:
        d = column_list[j]
        x = data['WL/nm']
        y = data[d]
        y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
        ax1.plot(x, y_sm, label = '{}'.format(column_list[j]))
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10, ncol=1)
    ax1.set_xlim(x_start, x_end)
    ax1.set_xticks(np.arange(label_min, label_max, x_int))
    ax1.set_ylim(-0.05, y_max[i])
    ax1.tick_params(labelsize = 11)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('Wavelength (nm)', fontsize=14)
    ax1.set_ylabel('Absorbance', fontsize=14, labelpad=2)
    fig.savefig('{}_partial_smoothed.png'.format(titles[i]), dpi=300, bbox_inches='tight')
    i = i+1

# ###--- Smoothing and 2nd derivitization ---###
# i = 0
# for _ in samples:
#     y = np.array(sp2[i][20:121], dtype = float)
#     y_sm = scipy.signal.savgol_filter(y, w1, 2, deriv=0)
#     y_sm_2Der = np.gradient(np.gradient(y_sm))
#     i = i+1
