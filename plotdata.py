# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 00:09:23 2022

@author: ImaiT
"""

###=====COLOR SETS =====###
blue3 = ['cyan','blue','navy']; blue4 =['cyan','dodgerblue','blue','navy']
gray_blue4 = ['grey','cyan','dodgerblue','blue','navy']
red3 = ['pink','magenta','crimson']; red4 = ['lightsalmon','tomato','red','darkred']
gray_red4 = ['grey','lightsalmon','tomato','red','darkred']
###===========================================================================


###----------------PACKAGES to use------------------
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib.colors import LogNorm

# To use Japanese language
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

# input
ext_data = '.txt'

files = os.listdir('.')
files_file = [f for f in files if os.path.isfile(os.path.join('.', f))]
print(files_file)
datal = [d for d in files if os.path.splitext(d)[1] == ext_data]
print(datal)

#===Pandas DataFrame===
dl_pd = []
dd_pd = {}
i = 0
for _ in datal:
    with open(datal[i], encoding='shift-jis') as f:
        s = pd.read_csv(f, sep ='\t', skiprows = 0)
        s2 = s.reset_index()
        s2.columns = ['index', 'wavenumber (cm-1)', 'Intensity (abs)']
        dn = datal[i][:-4]
        dd_pd[dn] = s2
        dl_pd.append(dn)
        #s2.to_csv('{}_pandas.csv'.format(dn))
        i = i+1

###Check the data to prepare the labels for plot
print(dl_pd)
pltlabel = ['Avicel', 'PASC', 'Avicel-BmimCl_10min_100C', 'Avicel-BmimCl_30min_100C', 'Avicel-BmimCl_4h_100C', 'BmimCl']

###---Plot---###
fig = plt.figure(figsize = (6,10), dpi = 200)

i=0
for dn in dd_pd:
    j = i+1
    ax1 = fig.add_subplot(3,2,j)
    ax1.plot(dd_pd[dn]['wavenumber (cm-1)'], dd_pd[dn]['Intensity (abs)'], label = pltlabel[i])
    ax1.set_title(dl_pd[i], fontsize=7)
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=6)
    ax1.set_xlim(2900, 3600)
    ax1.set_xticks(np.arange(2900,3601,100))
    ax1.tick_params(labelsize=6)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('wave number (cm$^{-1}$)', fontsize=8)
    ax1.set_ylabel('Intensity (counts)', fontsize=8,labelpad=1)
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    i = i+1

opf1 = os.path.join('Raman_20220928.png')
fig.savefig(opf1, dpi=300)

###---Plot2: Superimposed---###
fig = plt.figure(figsize = (6,6), dpi = 200)
ax1 = fig.add_subplot(111)
ax1.set_title('Raman@20220928', fontsize=12)
i=0
for dn in dd_pd:
    ax1.plot(dd_pd[dn]['wavenumber (cm-1)'], dd_pd[dn]['Intensity (abs)'], label = pltlabel[i])
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=6)
    ax1.set_xlim(2900, 3600)
    ax1.set_xticks(np.arange(2900,3601,100))
    ax1.tick_params(labelsize=6)
    ax1.minorticks_on()
    ax1.grid(which='major', axis = 'x', color = 'gray')
    ax1.grid(which='minor', axis = 'x', color = 'lightgray')
    ax1.set_xlabel('wave number (cm$^{-1}$)', fontsize=10)
    ax1.set_ylabel('Intensity (counts)', fontsize=10,labelpad=2)
    i = i+1

opf1 = os.path.join('Raman_20220928_super.png')
fig.savefig(opf1, dpi=300)