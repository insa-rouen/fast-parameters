#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Draw polar rose plot
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 13/05/2019
#
# Comments:
#     - 0.0: Initial version
#
# Description:
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from tools import utils
#* ============================= Modules Communs ==============================
# import windrose
from windrose import WindroseAxes, WindAxesFactory
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas
from math import pi
# import platform
# import subprocess
# from pathlib import Path


#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------




#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------




#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    location = "Caen" # Octeville, Le Touquet
    filename = "./data/SM_{}_2009 UV.csv".format(location)
    dataframe = pandas.read_csv(filename, delimiter=";", header=None)

    df = dataframe.iloc[:,[3,2]].copy()
    df.columns = ["direction", "speed"]
    
    

    # --- stacked histogram
    ax = WindroseAxes.from_ax()
    ax.bar(df.direction, df.speed, bins=np.arange(0, 20, 2), normed=False, opening=0.9)
    ax.set_legend()
    ax.set_title("Polar rose plot in {} (not normed)".format(location))    


    # --- Histogram presentation
    # ax = WindroseAxes.from_ax()
    # ax.bar(df.direction, df.speed, normed=True, nsector=16)
    # table = ax._info['table']
    # wd_freq = np.sum(table, axis=0)

    # axis = plt.subplot()
    # wd_freq = np.sum(table, axis=0)
    # axis.bar(np.arange(16), wd_freq,)
    # xlabels = ('N', '', 'N-E', '', 'E', '', 'S-E', '',
    #            'S', '', 'S-W', '', 'W', '', 'N-W', '',)
    # xticks = np.arange(16)
    # axis.grid(axis='y')
    # axis.set_ylabel("Percentage (%)")
    # axis.set_yticks(np.arange(0,18,3))
    # axis.set_xticks(xticks)
    # axis.set_xticklabels(xlabels)
    # axis.set_title("Frequency of wind directions in {}".format(location))
    
    # PDF
    # from windrose import WindAxes
    # ax = WindAxes.from_ax()
    # # bins = np.arange(0, 6+1, 1)
    # # bins = bins[1:]
    # ax, params = ax.pdf(df.speed, bins=16)
    # # ax.legend(["Weibull dist: {}".format(params),])
    # ax.set_title("PDF and fitting Weibull distribution for wind in {}".format(
    #     location))
    # ax.set_xlabel("Wind velocity (m/s)")
    # ax.set_ylabel("Probability")
    # print(params)

    plt.show()
    


#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
