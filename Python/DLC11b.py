#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - run 12*100 times simulation over all wind speed
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 22/10/2018
#
# Comments:
#     - 0.0: Init version
#     - 0.1: apply to distributed computers
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
import DLC11
from tools import utils, distribute
from pyturbsim import turb
from pylife import meca, life
#============================== Modules Communs ==============================
import json
# import time
# import fileinput # iterate over lines from multiple input files
# import shutil # high-level file operations
# import subprocess # call a bash command e.g. 'ls'
# import multiprocessing # enable multiprocessing
# from contextlib import contextmanager # utilities for with-statement contexts




#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def runTurbSimFAST_multiprocess(seed):
    ''' Run TurbSim + FAST
    '''
    # change workdirectory to DLC wind profiles and run TurbSim
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC/1.1/'):
        temp = turb.Turbulence_para(seed=seed)
        temp.run(silence=True)
    # run FAST
    temp = DLC1_1.DLC(seed=seed)
    temp.run(silence=True)

def runTurbSim_multiprocess(seeds):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        turb.get_turbulence_multiprocess(seeds, False)
#TODO
def runFAST_multiprocess(seed):
    # run FAST
    temp = DLC11.DLC(seed=seed)
    temp.run(silence=True)

def runStress_multiprocess(seeds):
    # generate file names
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    # run stress calculation
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        meca.get_stress_multiprocess(list_filebase, datarow=6009, gages=[1,2,3,4,5,6,7,8,9], thetaStep=30)

def runFatigue_multiprocess(seeds):
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_fatigue_multiprocess(list_filebase, gages=[1,2,3,4,5,6,7,8,9], lifetime=20*365*24*6)
    

#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('1000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM"]
    
    seeds = liste[:56]
    

    computers = distribute.LMN(runTurbSim_multiprocess)
    computers.setEqually(seeds)
    # computers.show()
    computers.run()




#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
