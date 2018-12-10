#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run calculation on lmn-cs server
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 03/12/2018
#
# Comments:
#     - 0.1: [03/12/18] Run DLC1.1b for 10 000 simulations at 21 m/s
#     - 0.2: [10/12/18] Run DLC1.1b for 10 000 simulations at 15 m/s
#
# Description:
#     
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from tools import utils, server
from DLC11b import runTurbSim_multiprocess, runFAST_multiprocess
from DLC11b import runStressFatigue_multiprocess, runALL_multiprocess
#*============================= Modules Communs ================================
import time
import json
import psutil



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
    # Check CPU usage ==========================================================
    if psutil.cpu_percent() >= 60: return

    # Load Seeds ===============================================================
    with utils.cd('~/aster1/Wind'):
        with open('10000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM" and s[1] == "15"]
    seeds = liste
    
    # Recalculate TurbSim + FAST + Stress
    # with utils.cd("~/lmn-cs/Wind"):
    #     #with open("failedRunsFAST.json", "r") as f:
    #     #    seeds1 = json.loads(f.read())
    #     #with open("failedRunsStress.json", "r") as f:
    #     #    seeds2 = json.loads(f.read())
    #     with open("recomputeALL.json", "r") as f:
    #         seeds3 = json.loads(f.read())
    # # #seeds1.extend(seeds2)
    # seeds = seeds3
    
    # Run ======================================================================
    lmn_cs = server.Aster1(inputSeeds=seeds,
                    windPath='~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                outputPath='~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                           echo=False)
    lmn_cs.seeds = seeds # set list of seeds manually

    runMode = 1
    if runMode == 1:
        # All-In-One: TurbSim + FAST + Stress + Fatigue ------------------------
        lmn_cs.run(runALL_multiprocess, 10, "", True) # thetaStep, outputFolder,
                                                      # compress, silence, echo
    
    if runMode == 2:
        # TurbSim --------------------------------------------------------------
        lmn_cs.run(runTurbSim_multiprocess, True, False) # silence, echo
        time.sleep(5)

        # FAST -----------------------------------------------------------------
        lmn_cs.run(runFAST_multiprocess, True, False) # silence, echo
        time.sleep(5)
        
        # Stress + Fatigue -----------------------------------------------------
        lmn_cs.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
        # lmn_cs.resume('Fatigue', inputFileSize=85*1024**2,
        #               outputFileSize=20*1024, compress=True)
        time.sleep(5)

        # TurbSim + FAST + Stress + Fatigue ------------------------------------
        # [ATTENTION] This will only overwrite recomputeALL.json
        # lmn_cs.resume('ALL', outputFileSize=20*1024)

    lmn_cs.finalcheck(btsFileSize=70*1024**2, outFileSize=85*1024**2,
                      tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
