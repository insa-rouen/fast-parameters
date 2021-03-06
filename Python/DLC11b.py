#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - run 12*100 times simulation over all wind speed
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 22/10/2018
#
# Comments:
#     - 0.0: Init version
#     - 0.1: Apply to distributed computers
#     - 0.2: Run 10 000 simulation at wind speed 25 m/s
#     - 0.3: Run 10 000 simulation at wind speed 23 m/s
#     - 0.4: [09/12/18] Run 10 000 simulations at wind speed 17 m/s
#     - 0.5: [15/12/18] Run 10 000 simulations at wind speed 13 m/s
#     - 0.6: [20/12/18] Run 10 000 simulations at wind speed 9 m/s
#     - 0.7: [23/12/18] Run 10 000 simulations at wind speed 5 m/s
#     - 0.8: [25/12/18] Run 10 000 simulations at wind speed 3 m/s
#     - 1.0: [25/04/19] Run 10 simulations for wind speed [3, 3.1, 3.2, ..., 25]
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
import os



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------
CORES = int( os.cpu_count() )



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def runTurbSim_multiprocess(seeds, logpath='', silence=False, echo=True):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        turb.get_turbulence_multiprocess(seeds, logpath=logpath,
                                         silence=silence, echo=echo)

def runFAST_multiprocess(seeds, silence=False, echo=True):
    DLC.get_DLC11_multiprocess(seeds, outputFolder='',silence=silence,echo=echo)

def runStress_multiprocess(seeds, thetaStep=30, echo=True):
    # generate file names
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    # run stress calculation
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        meca.get_stress_multiprocess(list_filebase, datarow=6009,
                                     gages=[1,2,3,4,5,6,7,8,9],
                                     thetaStep=thetaStep,
                                     saveToDisk=True, echo=echo)

def runFatigue_multiprocess(seeds, echo=True):
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_fatigue_multiprocess(list_filebase, gages=[1,2,3,4,5,6,7,8,9], lifetime=20*365*24*6, echo=echo)

def runStressFatigue_multiprocess(seeds, thetaStep, echo=True):
    ''' Run Stress and Fatigue in same time
    '''
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_stress_fatigue_multiprocess(list_filebase, datarow=6009,
                                             gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep,
                                             lifetime=20*365*24*6,echo=echo)

def runALL(seed, thetaStep, outputFolder="", compress=False, silence=False,
           echo=True):
    try:
        logpath = "~/Eolien/Parameters/Python/DLC1.1/log"
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/"):
            turb.get_turbulence(seed, logpath, silence, echo) # generate TurbSim
        DLC.get_DLC11(seed, outputFolder, silence, echo) # run FAST
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/"):
            filebase = "{}_{}mps_{}".format(seed[0], seed[1], seed[2])
            life.get_stress_fatigue(filebase, datarow=6009,
                                    gages=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    thetaStep=thetaStep, lifetime=20*365*24*6,
                                    echo=echo) # calculate Stress and Fatigue
    except:
        raise
    else:
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/"):
            if compress:
                utils.compress(filename=filebase+".out", removeSource=True)
        return seed

def runALL_multiprocess(seeds, thetaStep, outputFolder="", compress=True,
                        silence=True, echo=False):
    print('All-In-One: TurbSim + FAST + Stress + Fatigue v0.1 (December 10 2018)')
    print('========== Multiprocessing Mode ==========')
    # prepare a callback function
    length = len(seeds)
    print('[INFO] {} tasks is submitted'.format(length))
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
    pool = multiprocessing.Pool(CORES)
    [pool.apply_async(runALL, args=(seed, thetaStep, outputFolder, compress,
     silence,  echo), callback=printer, error_callback=utils.handle_error) for
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
    # with utils.cd('~/aster1/Wind'):
    #     with open('10seeds.json', 'r') as f:
    #         seeds = json.loads(f.read())
    # liste = [s for s in seeds if s[0] == "NTM" and s[1] == "3"]
    # liste = [s for s in seeds if s[0] == "NTM"]
    # seeds = liste

    # Re-run
    # with utils.cd('~/aster1/Wind'):
    #     with open('failedRunsFAST.json', 'r') as f:
    #         seeds1 = json.loads(f.read())
    #     with open('failedRunsStress.json', 'r') as f:
    #         seeds2 = json.loads(f.read())
        # with open('recomputeALL.json', 'r') as f:
        #     seeds3 = json.loads(f.read())
    #     with open('recomputeTurbSim.json', 'r') as f:
    #         seeds4 = json.loads(f.read())
    # ----- Rerun failed cases
    # seeds1.extend(seeds2)
    # seeds = seeds1
    # ----- Rerun recomputed cases
    # seeds = seeds3
    # seeds = seeds4
    # seeds = [['NTM', '3', '-544599383'], ['NTM', '5', '1571779345']]
    seeds = [["NTM", "21", "-800757005"], ]
    # Some Tests ===============================================================
    # DLC.get_DLC11(['NTM', '4.0', '1879136045'], outputFolder='', silence=False, 
    #                echo=True)
    
    # runTurbSim_multiprocess(seeds, silence=1, echo=1)
    runFAST_multiprocess(seeds, silence=0, echo=1)
    # # runStress_multiprocess(seeds, echo=0)
    # # runFatigue_multiprocess(seeds, echo=0)
    # runStressFatigue_multiprocess(seeds, 10, echo=0)
    return
    

    # Initiate/Resume Tasks ====================================================
    # Distribute tasks ---------------------------------------------------------
    computers = distribute.LMN(
        windPath='~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
        outputPath='~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1')
    computers.deactivate("PC-LMN-9020")  # Shubiao WANG
    computers.deactivate("PC-LMN-9020A")
    computers.deactivate("PC-LMN-7040") # 1TB
    # computers.setEqually(seeds)
    computers.setAutomatically(seeds)
    # computers.show()
    
    # TurbSim ------------------------------------------------------------------
    # computers.resume('TurbSim', outputFileSize=70*1024**2)
    computers.run(runTurbSim_multiprocess,
                  "~/Eolien/Parameters/Python/DLC1.1/log",
                  True, False)  # logpath="...", silence=True, echo=False

    # FAST ---------------------------------------------------------------------
    computers.run(runFAST_multiprocess, True, False) #silence=True, echo=False

    # Stress -------------------------------------------------------------------
    # computers.run(runStress_multiprocess)

    # Fatigue ------------------------------------------------------------------
    # computers.run(runFatigue_multiprocess)

    # Stress + Fatigue ---------------------------------------------------------
    # computers.resume('Fatigue', outputFileSize=20*1024)
    computers.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo


#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
