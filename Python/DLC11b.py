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
def runTurbSimFAST_multiprocess(seed):
    ''' Run TurbSim + FAST
    '''
    # change workdirectory to DLC wind profiles and run TurbSim
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        temp = turb.Turbulence_para(seed=seed)
        temp.run(silence=True)
    # run FAST
    temp = DLC11.DLC(seed=seed)
    temp.run(silence=True)

def runTurbSim_multiprocess(seeds):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        turb.get_turbulence_multiprocess(seeds, False)

def runFAST_multiprocess(seeds, moveSource=False, silence=False, echo=True):
    DLC.get_DLC11_multiprocess(seeds, outputFolder='/', moveSource=moveSource, silence=silence, echo=echo)

def runStress_multiprocess(seeds, thetaStep=10, echo=True):
    # generate file names
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    # run stress calculation
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        meca.get_stress_multiprocess(list_filebase, datarow=6009, gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep, echo=echo)

def runFatigue_multiprocess(seeds, echo=True):
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_fatigue_multiprocess(list_filebase, gages=[1,2,3,4,5,6,7,8,9], lifetime=20*365*24*6, echo=echo)



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
    
    seeds = liste[168:]

    computers = distribute.LMN()
    # computers.setEqually(seeds)
    # computers.setAutomatically(seeds)
    
    # Distribute tasks -------------------------------------------------------------------
    part = [s for s in seeds if s[1] == "5" or s[1] == "7"]
    # print(len(part))
    computers.setIndividually('PC-LMR-O7010B', part)

    part = [s for s in seeds if s[1] == "9" or s[1] == "11"]
    # print(len(part))
    computers.setIndividually('PC-LMN-7050', part)

    part = [s for s in seeds if s[1] == "13" or s[1] == "15"]
    # print(len(part))
    computers.setIndividually('PC-LMN-7040', part)

    part = [s for s in seeds if s[1] == "17" or s[1] == "19"]
    # print(len(part))
    computers.setIndividually('PC-LMN-1600A', part)

    part = [s for s in seeds if s[1] == "21" or s[1] == "23"]
    # print(len(part))
    computers.setIndividually('PC-LMN-1600B', part)

    part = [s for s in seeds if s[1] == "25"]
    reste = [s for s in seeds if s[1] == "3"]
    addition = reste[:500]
    part.extend(addition)
    # print(len(part))
    computers.setIndividually('PC-LMN-9010', part)

    residu = reste[500:]
    # print(len(residu))
    computers.setIndividually('PC-LMN-9020', residu[:3])    


    # computers.show()
    # computers.run(runTurbSim_multiprocess)

    # FAST -------------------------------------------------------------------------------
    computers.run(runFAST_multiprocess)

    # Stress -----------------------------------------------------------------------------
    computers.run(runStress_multiprocess)

    # Fatigue ----------------------------------------------------------------------------
    computers.run(runFatigue_multiprocess)



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
