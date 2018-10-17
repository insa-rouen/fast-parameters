#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: FIND MAXIMA AND MINIMA
# 
# 
#
#
# Authors: Hao BAI
# Date: 02/10/2018
#
# Version:
#   - 0.0: Initial version, enable multiprocessing
#   - 0.1: Use personlized packages
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from tools import utils
from pycrunch import amplitude
#============================== Modules Communs ==============================
import json
import time



#-----------------------------------------------------------------------------------------
#                                          CLASS
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                       FUNCTIONS
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                      MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC'):
        with open('6seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = []
    [liste.append(s) for s in seeds if s[0] == 'ETM']
    seeds = liste
    # generate a list of file basenames (i.e. filename without extension)
    filelist = []
    for seed in seeds:
        file ='{}_{}mps_{}'.format(seed[0], seed[1], seed[2])
        filelist.append(file)

    channels = ['YawBrTDxt', 'YawBrTDyt', 'YawBrFxp', 'YawBrFyp', 'YawBrMyp', 'YawBrMzp',
                'RootMxc1', 'RootMyc1', 'TipDxc1', 'TipDyc1']
    TIK = time.time()  

    # # ----- Running on single processor
    # for file in filelist:
    #     amplitude.find_peak_valley(file, header=7, datarow=6009, startline=12,
    #                                channels=channels)

    # ----- Running on multi processor
    amplitude.find_peak_valley_multiprocess(filelist, 7, 6009, 12, channels)

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")



#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
