#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Optimization: some utilities
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
#
# Comments:
#     - 0.0: [19/12/2018] Initial version
#
# Description:
#     
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                   MODULES
#!------------------------------------------------------------------------------
#============================= Modules Personnels =============================
import csv
import pickle
import numpy
import pandas
import time
import collections
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from matplotlib import gridspec
from matplotlib import ticker
from matplotlib import pyplot as plt
from pycrunch import amplitude as amp
from tools import utils
try:
    import sys, IPython
    sys.excepthook = IPython.core.ultratb.ColorTB()
except:
    pass
#============================= Modules Communs =============================





#!------------------------------------------------------------------------------
#!                               CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                             FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def plot(item, file_ref, file2):
    data1 = utils.readcsv(file_ref, datarow=6009)
    data2 = utils.readcsv(file2, datarow=6009)

    fig, ax = plt.subplots()

    X = data1.get(1)['Records']
    Y1 = data1.get(item)['Records']
    ax.plot(X, Y1, label="Ref.")

    X = data2.get(1)['Records']
    Y2 = data2.get(item)['Records']
    ax.plot(X, Y2, "--", markevery=(0.1), label="with TRD")

    ax.set_title(item)
    plt.legend()

    plt.show()

def plot_YawBrTD(file_ref, file2):
    data1 = utils.readcsv(file_ref, datarow=6009)
    data2 = utils.readcsv(file2, datarow=6009)

    fig, ax = plt.subplots()

    X = data1.get(1)['Records']
    Y1 = data1.get("YawBrTDxt")['Records']
    ax.plot(X, Y1, label="Ref.")

    X = data2.get(1)['Records']
    Y2 = data2.get("YawBrTDxt")['Records']
    ax.plot(X, Y2, "--", markevery=(0.1), label="with TRD")

    ref_index = (1509, 1736, 1902, 2054, 2211, 2361, 2515, 2669, 2823, 2976)
    for i in ref_index:
        ax.plot(X[i], Y2[i], 'ro')
    plt.legend()
    

    plt.show()


def plot_NTRD(file_ref, file2):
    data1 = utils.readcsv(file_ref, datarow=6009)
    data2 = utils.readcsv(file2, datarow=6009)

    fig, ax = plt.subplots()

    X = data1.get(1)['Records']
    Y1 = data1.get("NTRD_A")['Records']
    ax.plot(X, Y1, label="Ref.")

    X = data2.get(1)['Records']
    Y2 = data2.get("NTRD_A")['Records']
    ax.plot(X, Y2, "--", markevery=(0.1), label=data2.get("NTRD_A")['Title'])

    ref_index = (1509, 1736, 1902, 2054, 2211, 2361, 2515, 2669, 2823, 2976)
    for i in ref_index:
        ax.plot(X[i], Y2[i], 'ro')
    plt.legend()

    plt.show()

def find_ref_time_for_peak():
    ''' time that occurs extremum deflection
    '''
    channels = ['YawBrTDxt', ]
    amp.find_peak_valley("DLC2.3_EOG_O", header=7, startline=12,
        datarow=6009, channels=channels)
    temp = amp.Amplitude.max_p2p_amplitude("DLC2.3_EOG_O", channels, ".ext", N=10)
    
    ref_time = (75.09, 77.36, 79.02, 80.54, 82.11, 83.61, 85.15, 86.69, 88.23,
                89.76,)
    data = utils.readcsv("./DLC2.3_EOG_O.out", datarow=6009)
    X = data.get(1)['Records']
    ref_index = [X.index(t) for t in ref_time]
    print(ref_index)



#!------------------------------------------------------------------------------
#!                                MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    file_ref = "./DLC2.3_EOG_O_ref.out"
    file2 = "./DLC2.3_EOG_O.out"
    plot("Wind1VelX", file_ref=file_ref, file2=file2)
    plot_NTRD(file_ref=file_ref, file2=file2)
    plot_YawBrTD(file_ref=file_ref, file2=file2)
    # find_ref_time_for_peak()



#!------------------------------------------------------------------------------
#!                                 DEBUG TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
