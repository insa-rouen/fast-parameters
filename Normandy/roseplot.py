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
import json
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
def plot_speed_range(measure_data, vmin, vmax, duration, show=False):
    ''' Filter data by wind speed between vmin (included) and vmax (not 
        included)
        INPUT
            duration: the mesured duration [min]
    '''
    df = measure_data.loc[(vmin<=measure_data.loc[:, "speed"]) & 
        (measure_data.loc[:, "speed"]<vmax)]

    ax = WindroseAxes.from_ax()
    ax.bar(df.direction, df.speed, normed=False, nsector=36)
    wd_count = np.sum(ax._info['table'], axis=0) # cumulative appearance in each
        # direction
    wd_time = wd_count * duration
    # plot result by bar
    if show:
        axis = plt.subplot()
        axis.bar(np.arange(0,360,10), wd_time, width=8)
        axis.grid(axis='y')
        axis.set_xlabel("Wind direction (°)")
        axis.set_ylabel("Time (min)")
        axis.set_xticks(np.arange(0, 360, 10))
        axis.set_title("Wind directions at mean speed {} m/s".format(
            (vmin+vmax)/2.0))
        plt.show()
    res = pandas.DataFrame(wd_time, index=range(0,360,10), columns=["Time"])
    return res


def load_sts(filename, quantile):
    import scipy.stats
    unit_damage = {}
    with open(filename, "r") as f:
        rawdata = json.loads(f.read())
        for elem in rawdata:
            # theta
            key = elem.keys()
            theta = int(list(key)[0])
            # get saved information
            info = list(elem.values())[0]
            dist_name = info[0].get("Name")
            dist_param = info[0].get("Parameters")
            # get distribution object by name
            dist = getattr(scipy.stats, dist_name)
            # add to the set of distributions
            unit_damage[theta] = dist.ppf(quantile, *dist_param[:-2], 
                loc=dist_param[-2], scale=dist_param[-1])
    res = pandas.DataFrame.from_dict(unit_damage, orient="index")
    return res


def calculate_damage_direction(wind_direction_time, unit_damage,
    simulated_time=10, show=False):
    """ Evaluate fatigue damage between a given speed range for all wind
        directions
        INPUT
            wind_direction_time: cumulative time for wind from all directions 
                [pandas.DataFrame]
            unit_damage: cumulative fatigue damage on a tower gage for all 
                spots [pandas.DataFrame]
            simulated_time: simulated time used in numerical modelisation [min]
    """
    amplifier = wind_direction_time.div(simulated_time)
    multiplication = pandas.DataFrame(amplifier.values * unit_damage.T.values)
    theta = pandas.DataFrame(list(range(0, 360, 10)))
    # Convert tower gage polar coordinates to wind polar coordinates
    all_damages = pandas.DataFrame()
    for i in range(0, 36, 1):
        row = multiplication.iloc[[i]] 
        index = (theta.T*(-1) + i*10).mod(360)
        row.columns = index.values.tolist()
        row = row.reindex(sorted(row.columns), axis=1)
        all_damages = all_damages.append(row)
    all_damages.index = theta.T.values.tolist() # row: wind direction; column: 
        # angle in polar coordinates
    # plot damage induced by individual wind direction
    if show:
        axis = plt.subplot(111, polar=True)
        axis.set_theta_zero_location("N") # set angle=0 at the top
        axis.set_theta_direction(-1) # set angle increasing clockwise
        axis.set_thetagrids(range(0, 360, 30))  # change theta gridlines
        X = np.radians(theta)
        X = X.append(X.iloc[0], ignore_index=True)
        for i in range(0, 360, 10):
            Y = all_damages.loc[i].T
            Y = Y.append(Y.iloc[0], ignore_index=True)
            axis.plot(X, Y.values, label="Wind from {} degree".format(i))
        plt.show()
    return all_damages
    
def calculate_damage_speed(damages_direction, show=False):
    """ Calculate total damage between a given wind speed range
        INPUT
            damages_direction: fatigue damage induced by wind from every
                direction [DataFrame]
    """
    damage = damages_direction.sum(axis=1)
    if show:
        axis = plt.subplot(111, polar=True)
        axis.set_theta_zero_location("N")  # set angle=0 at the top
        axis.set_theta_direction(-1)  # set angle increasing clockwise
        axis.set_thetagrids(range(0, 360, 30))  # change theta gridlines
        # theta = pandas.DataFrame(list(range(0, 360, 10)))
        X = np.radians(range(0,360,10))
        X = np.append(X, X[0])
        Y = np.append(damage, damage.iloc[0])
        axis.plot(X, Y)
        axis.set_title("Damage at 3 m/s for 1 year")
        plt.show()


#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
def main2():

    # Step 1
    location = "Caen"  # Octeville, Le Touquet
    filename = "./data/SM_{}_2009 UV.csv".format(location)
    dataframe = pandas.read_csv(filename, delimiter=";", header=None)

    df = dataframe.iloc[:, [3, 2]].copy()
    df.columns = ["direction", "speed"]

    wd_time = plot_speed_range(measure_data=df, vmin=2.0, vmax=4.0, duration=30,
        show=False)
    
    # Step 2
    unit_dam = load_sts("/Users/hbai/PhD/Memo/DLC1.1b/Figures/10000seeds/10000@9mps.sts", quantile=0.95)
    
    # Step 3
    dmg_dir = calculate_damage_direction(wind_direction_time=wd_time,
        unit_damage=unit_dam, show=False)
    calculate_damage_speed(dmg_dir, show=True)


def main1():
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
        main2()
