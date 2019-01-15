#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.3 - run 12*100 times simulation over all wind speed
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 28/12/2018
#
# Comments:
#     - 0.0: Init version (duplicate from DLC11b.py)
#     - 0.1: [03/01/19] Execute 10 000 runs at 3 m/s
#     - 0.2: [05/01/19] Execute 10 000 runs at 21 m/s
#     - 0.3: [11/01/19] Execute 10 000 runs at 15 m/s
#     - 0.4: [15/01/19] Execute 10 000 runs at 11 m/s
#
# Description:
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                        MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from tools import utils, distribute
from pywind import turb
from pylife import meca, life
from pyfast import DLC
#* ============================= Modules Communs ==============================
import json
import time
import multiprocessing



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def runTurbSim_multiprocess(seeds, logpath='', silence=False, echo=True):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.3/'):
        turb.get_turbulence_multiprocess(seeds, logpath=logpath,
                                         silence=silence, echo=echo)

def runFAST_multiprocess(seeds, silence=False, echo=True):
    DLC.get_DLC13_multiprocess(seeds, outputFolder='',silence=silence,echo=echo)

def runStressFatigue_multiprocess(seeds, thetaStep, echo=True):
    ''' Run Stress and Fatigue in same time
    '''
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.3/'):
        life.get_stress_fatigue_multiprocess(list_filebase, datarow=6009,
                                             gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep,
                                             lifetime=20*365*24*6,echo=echo)

def runALL(seed, thetaStep, outputFolder="", compress=False, silence=False,
           echo=True):
    try:
        logpath = "~/Eolien/Parameters/Python/DLC1.3/log"
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.3/"):
            turb.get_turbulence(seed, logpath, silence, echo) # generate TurbSim
        DLC.get_DLC13(seed, outputFolder, silence, echo) # run FAST
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.3/"):
            filebase = "{}_{}mps_{}".format(seed[0], seed[1], seed[2])
            life.get_stress_fatigue(filebase, datarow=6009,
                                    gages=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    thetaStep=thetaStep, lifetime=20*365*24*6,
                                    echo=echo) # calculate Stress and Fatigue
    except:
        raise
    else:
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.3/"):
            if compress:
                utils.compress(filename=filebase+".out", removeSource=True)
        return seed

def runALL_multiprocess(seeds, thetaStep, outputFolder="", compress=True,
                        silence=True, echo=False):
    print('All-In-One: TurbSim + FAST + Stress + Fatigue v0.1 (December 10 2018)')
    print('========== Multiprocessing Mode ==========')
    length = len(seeds)
    print("{} tasks will be calculated".format(length))
    # prepare a callback function
    completed = []
    def printer(seed):
        pos = seeds.index(seed) + 1
        completed.append(seed)
        rest = length - len(completed)
        hour, minute = time.strftime("%H,%M").split(',')
        print('|- [{}/{}] {} at {} m/s with seed ID {} is finished at {}:{}. '
              '{} tasks waiting to be completed ...'.format(pos, length,seed[0],
              seed[1], seed[2], hour, minute, rest))
    # begin multiprocessing
    pool = multiprocessing.Pool()
    [pool.apply_async(runALL, args=(seed, thetaStep, outputFolder, compress,
     silence, echo), callback=printer, error_callback=utils.handle_error) for
     seed in seeds]
    pool.close()
    pool.join()



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    # Load Seeds ===============================================================
    # Initiation
    with utils.cd('~/aster1/Wind'):
        with open('10000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "ETM" and s[1] == "11"]
    seeds = liste

    # Re-run
    # with utils.cd('~/aster1/Wind'):
    #     with open('failedRunsFAST.json', 'r') as f:
    #         seeds1 = json.loads(f.read())
    #     with open('failedRunsStress.json', 'r') as f:
    #         seeds2 = json.loads(f.read())
    #     with open('recomputeALL.json', 'r') as f:
    #         seeds3 = json.loads(f.read())
    #     with open('recomputeTurbSim.json', 'r') as f:
    #         seeds4 = json.loads(f.read())
    # ----- Rerun failed cases
    # seeds1.extend(seeds2)
    # seeds = seeds1
    # ----- Rerun recomputed cases
    # seeds = seeds3
    # seeds = seeds4
    # seeds = [['NTM', '3', '-544599383'], ['NTM', '5', '1571779345']]

    # Some Tests ===============================================================
    # runTurbSim_multiprocess(seeds, silence=1, echo=1)
    # runFAST_multiprocess(seeds, silence=1, echo=1)
    # # runStress_multiprocess(seeds, echo=0)
    # # runFatigue_multiprocess(seeds, echo=0)
    # runStressFatigue_multiprocess(seeds, 10, echo=0)
    # return
    

    # Initiate/Resume Tasks ====================================================
    # Distribute tasks ---------------------------------------------------------
    computers = distribute.LMN("~/aster1/Wind/DLC1.3")
    computers.deactivate("PC-LMN-9020")  # Shubiao WANG
    # computers.setEqually(seeds)
    computers.setAutomatically(seeds)
    # computers.show()
    
    # TurbSim ------------------------------------------------------------------
    computers.resume("TurbSim")
    computers.run(runTurbSim_multiprocess,
                  "~/Eolien/Parameters/Python/DLC1.3/log",
                  True, False) # logpath="...", silence=True, echo=False

    # FAST ---------------------------------------------------------------------
    # computers.run(runFAST_multiprocess, True, False) #silence=True, echo=False

    # Stress -------------------------------------------------------------------
    # computers.run(runStress_multiprocess)

    # Fatigue ------------------------------------------------------------------
    # computers.run(runFatigue_multiprocess)

    # Stress + Fatigue ---------------------------------------------------------
    # computers.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
