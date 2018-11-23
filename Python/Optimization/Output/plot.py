#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC2.3 with TRD
#
# Authors: Hao BAI
# Date: 21/11/2018
#
# Comments:
#     - Some comparing plots
#     - The value for mode 1 in TRD will be optimized
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
import sys, IPython # to colorize traceback errors in terminal
sys.excepthook = IPython.core.ultratb.ColorTB()
from pycrunch import amplitude as amp
from pygraph import chart
from tools import utils
#============================== Modules Communs ==============================
import numpy
from matplotlib import pyplot as plt
from matplotlib import gridspec

from matplotlib import ticker


#-----------------------------------------------------------------------------------------
#                                          FONCTIONS DE PLOT
#-----------------------------------------------------------------------------------------
def plot_Wind1Vel(columns=['Wind1VelX','Wind1VelY','Wind1VelZ'], xlim=[60, 90, 10], ylim=[-5, 35, 5], file='', toPDF=[]):
    data = utils.readcsv(file)

    fig, ax = plt.subplots()

    X = data.get('Time')['Records']
    Y = data.get(columns[0])['Records']
    ax.plot(X, Y, label=data.get(columns[0])['Title'])
    Y = data.get(columns[1])['Records']
    ax.plot(X, Y, 'o--', markevery=(0.1), label=data.get(columns[1])['Title'])
    Y = data.get(columns[2])['Records']
    ax.plot(X, Y, '^:', markevery=(0.05, 0.1), label=data.get(columns[2])['Title'])

    chart.adjust(ax, minor=[True, False, True, False], xlim=xlim, ylim=ylim, ylabel="Wind velocity (m/s)")

    chart.draw(fig, toPDF)


def compare_YawBrTDx(columns=['YawBrTDxt'], minor=[True, True, True, True], xlim=[60, 90, 10], ylim=[-0.9, 0.7, 0.1], file='', residu=False, withPV=False, toPDF=[]):
    # reference data
    X1 = DATA_REF.get('Time')['Records']
    Y1 = DATA_REF.get(columns[0])['Records']
    # data to be compared
    data = utils.readcsv(file)
    X2 = data.get('Time')['Records']
    Y2 = data.get(columns[0])['Records']

    fig, axeLeft = plt.subplots()
    # --- Left axis
    color = 'tab:blue'
    legendString1 = axeLeft.plot(X1, Y1, '--', label=DATA_REF.get(columns[0])['Title'])
    if not residu:
        legendString2 = axeLeft.plot(X2, Y2, label=data.get(columns[0])['Title']+file+" with TRD")
    axeLeft.set_ylabel("Deflection (m)", color=color)
    axeLeft.tick_params(axis='y', labelcolor=color)
    axeLeft.set_yticks(numpy.arange(ylim[0], ylim[1]+ylim[2], ylim[2]))
    plt.ylim(ylim[0], ylim[1])

    if withPV: # mark peak and valley
        filename = "reference_"+columns[0]+".ext"
        plot_peak_and_valley(filename, axeLeft)
        filename = file.rstrip(".out")+"_"+columns[0]+".ext"
        plot_peak_and_valley(filename, axeLeft)

    # --- Right axis
    if residu:
        color = 'tab:pink'
        axeRight = axeLeft.twinx() # instantiate a second axes that shares the same x-axis
        # calculate relative difference
        X_residu = X1
        Y_residu = [Y2[i]-Y1[i] for i in range(len(Y1))]
        legendString2 = axeRight.plot(X_residu, Y_residu, '-', linewidth=0.8, color=color, label="Residue = REF - "+file)
        axeRight.set_ylabel("Reletive difference in deflection (m)", color=color)
        axeRight.tick_params(axis='y', labelcolor=color)
        axeRight.set_yticks(numpy.arange(ylim[0], ylim[1]+ylim[2], ylim[2]))
        plt.ylim(ylim[0], ylim[1])
        
    # --- Common setting
    lns = legendString1 + legendString2
    labs = [l.get_label() for l in lns]
    axeLeft.legend(lns, labs, loc=0)
    
    plt.xlim(xlim[0], xlim[1])
    plt.xticks(numpy.arange(xlim[0], xlim[1]+xlim[2], step=xlim[2]))
    axeLeft.set_xlabel("Time (s)")
    axeLeft.grid(axis='x')
    axeLeft.grid(axis='y')

    chart.draw(fig, toPDF)


def plot_trd_AON_AOFF(TRD_AON, TRD_AOFF, columns=('NTRD_FC', 'NTRD_A', 'NTRD_VA'),
                      velocities=('I','R-2','R','R+2','O'), xlim=(60, 90, 10),
                      file='', toPDF=[]):
    for v in velocities:
        fig, axes = plt.subplots()
        # Create subplots
        axes = []
        gs = gridspec.GridSpec(3, 1, height_ratios=[2, 1, 2])
        axes.append( plt.subplot(gs[0]) )
        axes.append( plt.subplot(gs[1]) )
        axes.append( plt.subplot(gs[2]) )

        # slice data
        data = utils.readcsv(file)
        start = data.get('Time')['Records'].index(xlim[0])
        end = data.get('Time')['Records'].index(xlim[1])
        X = data.get('Time')['Records'][start:end]
        
        # Chart 1: NTRD_FC -----------------------------------------------------
        Y = data.get(columns[0])['Records'][start:end]
        axes[0].plot(X, Y, label=data.get(columns[0])['Title'])

        # Chart 2: NTRD_A ------------------------------------------------------
        Y = data.get(columns[1])['Records'][start:end]
        axes[1].plot(X, Y, '--', label=data.get(columns[1])['Title'])
        
        indices = [i for (i,y) in enumerate(Y) if y == 1] # TRD is activated: A = 1
        axes[1].plot([X[i] for i in indices], [Y[i] for i in indices], '.', markersize=1, color='tab:green', label="TRD ON")
        
        indices = [i for (i,y) in enumerate(Y) if y == 0] # TRD is inactivated: A = 0
        axes[1].plot([X[i] for i in indices], [Y[i] for i in indices],'.', markersize=1, color='tab:red', label="TRD OFF")

        # Chart 3: NTRD_VA -----------------------------------------------------
        Y = data.get(columns[2])['Records'][start:end]
        axes[2].plot(X, Y, ':', label=data.get(columns[2])['Title'])
        # TRD_AON
        indices = [i for (i,y) in enumerate(Y) if y >= TRD_AON]
        axes[2].plot([X[i] for i in indices], [Y[i] for i in indices], '.', markersize=1, color='tab:green', label="AON="+str(TRD_AON))
        # TRD_AOFF
        indices = [i for (i,y) in enumerate(Y) if y <= TRD_AOFF]
        axes[2].plot([X[i] for i in indices], [Y[i] for i in indices],'.', markersize=1, color='tab:red', label="AOFF="+str(TRD_AOFF))

        # Set axes properties
        chart.adjust(axes[0], xlim=xlim, ylim=[-30e3, 30e3], ylabel="Force (kN)", xVisible=False)
        chart.adjust(axes[1], xlim=xlim, ylim=[-0.2, 1.2], ylabel="TRD Status", xVisible=False, seperator=False)
        chart.adjust(axes[2], xlim=xlim, ylim=[-0.1, 2.0], ylabel="Amplitude of vibration (m/s)", seperator=False)

        chart.draw(fig, toPDF, left=0.08, bottom=0.06, right=0.92, top=0.94, wspace=0.14, hspace=0.14)



#-----------------------------------------------------------------------------------------
#                                          FONCTIONS UTILES
#-----------------------------------------------------------------------------------------
def plot_peak_and_valley(filename, axis):
    data = utils.readfwf(filename)
    X = data.get(1)['Records']
    Y = data.get(2)['Records']
    legendString = axis.plot(X, Y, '.', label="Peak/Valley")
    return legendString



#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
def main():
    # get reference data
    filebase = 'reference'
    global DATA_REF
    DATA_REF = utils.readcsv(filebase+".out")
    
    graphNum = 1

    if graphNum == 0: # get peak/valley and its time
        amp.find_peak_valley(filebase, header=7, datarow=6009, startline=12,
                             channels=["YawBrTDxt",])

    if graphNum == 1:
        # plot_Wind1Vel(file='EOG_O_277.826.7-86.712-17.0222.out')
        compare_YawBrTDx(file='EOG_O_277.826.7-86.712-17.0222.out', withPV=True)
        # compare_YawBrTDx(file='EOG_O_277.826.7-86.712-17.0222.out', residu=True)

        # plot_trd_AON_AOFF(TRD_AON=0.4, TRD_AOFF=0.05, velocities=('O',), file='EOG_O_277.826.7-86.712-17.0222.out')


    
#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
