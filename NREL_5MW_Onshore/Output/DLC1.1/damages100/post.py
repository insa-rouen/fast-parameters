#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - Analayse de fatigue
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 29/10/2018
#
# Comments:
#     - 0.0: Init version
#     
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from tools import utils
# from pyturbsim import turb
# from pylife import meca, life
from pycrunch import sensibility
#============================== Modules Communs ==============================
import json
# import time
# import math
# import collections
# import fileinput # iterate over lines from multiple input files
# import shutil # high-level file operations
# import subprocess # call a bash command e.g. 'ls'
# import multiprocessing # enable multiprocessing
# from contextlib import contextmanager # utilities for with-statement contexts
# from matplotlib import pyplot as plt



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('100seeds.json', 'r') as f:
            seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "NTM"]
    seeds = liste

    test = sensibility.Analysis(seeds=seeds, folder='theta=30', echo=True)

    test.damageOnSpot()
    exit()
    # test.plotDamageOnSpot('3','TwHt1@0')
    test.plotDamageForAllSpeeds()
    
    # test.meanDamageOnGage('3')
    test.meanDamageForAllSpeeds()
    # test.plotMeanDamageOnGage('3','1')
    test.plotMeanDamageForAllSpeeds()
    



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
