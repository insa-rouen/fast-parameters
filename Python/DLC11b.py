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
from iffast import DLC
#============================== Modules Communs ==============================
import json



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def runTurbSim_multiprocess(seeds, silence=False, echo=True):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        turb.get_turbulence_multiprocess(seeds, silence=silence, echo=echo)

def runFAST_multiprocess(seeds, silence=False, echo=True):
    DLC.get_DLC11_multiprocess(seeds, outputFolder='', silence=silence, echo=echo)

def runStress_multiprocess(seeds, thetaStep=30, echo=True):
    # generate file names
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    # run stress calculation
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        meca.get_stress_multiprocess(list_filebase, datarow=6009, gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep, saveToDisk=True, echo=echo)

def runFatigue_multiprocess(seeds, echo=True):
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_fatigue_multiprocess(list_filebase, gages=[1,2,3,4,5,6,7,8,9], lifetime=20*365*24*6, echo=echo)

def runStressFatigue_multiprocess(seeds, thetaStep, echo=True):
    ''' Run Stress and Fatigue in same time
    '''
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_stress_fatigue_multiprocess(list_filebase, datarow=6009, gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep, lifetime=20*365*24*6, echo=echo)



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('6seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM"]
    
    seeds = liste[:2]
    # seeds = [['NTM', '3', '-544599383'], ['NTM', '5', '1571779345']]
    # Some testing ...
    # runTurbSim_multiprocess(seeds, silence=1, echo=0)
    # runFAST_multiprocess(seeds, silence=1, echo=0)
    # runStress_multiprocess(seeds, echo=0)
    # runFatigue_multiprocess(seeds, echo=0)
    # with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1'):
    #     life.get_stress_fatigue('NTM_3mps_-544599383', 6009, [1,2,3,4,5,6,7,8,9], 30)
    # runStressFatigue_multiprocess([['NTM', '11', '-1500121613'], ['NTM', '9', '324541780']], 30, echo=0)

    # runStressFatigue_multiprocess(seeds, 30, echo=0)
    
    # Resume Tasks -----------------------------------------------------------------
    # Load seeds
    with utils.cd('~/aster1/Wind'):
        with open('recomputedSeeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM"]
    seeds = liste
    computers = distribute.LMN()
    
    # Distribute tasks -------------------------------------------------------------------
    # computers.setEqually(seeds)
    computers.setAutomatically(seeds)
    # computers.show()
    
    # TurbSim ----------------------------------------------------------------------------
    computers.run(runTurbSim_multiprocess, True, False) # silence=True, echo=False

    # FAST -------------------------------------------------------------------------------
#     computers.run(runFAST_multiprocess)

    # Stress -----------------------------------------------------------------------------
#     computers.run(runStress_multiprocess)

    # Fatigue ----------------------------------------------------------------------------
#     computers.run(runFatigue_multiprocess)

    # Stress + Fatigue -------------------------------------------------------------------
#     computers.run(runStressFatigue_multiprocess)


#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
