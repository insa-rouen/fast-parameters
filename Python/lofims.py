#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run calculation on PC-LOFIMS-T7610
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 01/12/2018
#
# Comments:
#     - 0.1: [01/12/18] Complete DLC1.1b for 10 000 simulations at 25 m/s
#     - 0.2: [09/12/18] Run 10 000 simulations at 19 m/s
#     - 0.3: [17/12/18] Run 10 000 simulations at 11 m/s
#     - 0.4: [10/01/19] Run 10 000 simulations at ETM 17 m/s
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
#from DLC11b import runTurbSim_multiprocess, runFAST_multiprocess
#from DLC11b import runStressFatigue_multiprocess, runALL_multiprocess
from DLC13b import runTurbSim_multiprocess, runFAST_multiprocess
from DLC13b import runStressFatigue_multiprocess, runALL_multiprocess
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
    liste = [s for s in seeds if s[0] == "ETM" and s[1] == "17"]
    seeds = liste

    # Recalculate TurbSim + FAST + Stress
    # with utils.cd("~/lmn-cs/Wind"):
    #     #with open("failedRunsFAST.json", "r") as f:
    #     #    seeds1 = json.loads(f.read())
    #     #with open("failedRunsStress.json", "r") as f:
    #     #    seeds2 = json.loads(f.read())
    #     with open("recomputeALL.json", "r") as f:
    #         seeds3 = json.loads(f.read())
    # #seeds1.extend(seeds2)
    # seeds = seeds3
 
    # Run ======================================================================
    lofims = server.Aster1(inputSeeds=seeds,
                    windPath="~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.3",
                outputPath="~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.3",
                           echo=False)
    lofims.seeds = seeds # set list of seeds manually

    runMode = 1
    if runMode == 1:
        # All-In-One: TurbSim + FAST + Stress + Fatigue ------------------------
        lofims.run(runALL_multiprocess, 10, "", False) # thetaStep, outputFolder,
                                                      # compress, silence, echo

    if runMode == 2:
        # TurbSim --------------------------------------------------------------
        lofims.run(runTurbSim_multiprocess, True, False) # silence, echo
        time.sleep(5)

        # FAST -----------------------------------------------------------------
        lofims.run(runFAST_multiprocess, True, False) # silence, echo
        time.sleep(5)
        
        # Stress + Fatigue -----------------------------------------------------
        lofims.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
        # lofims.resume('Fatigue', inputFileSize=85*1024**2,
        #               outputFileSize=20*1024, compress=True)
        time.sleep(5)

        # TurbSim + FAST + Stress + Fatigue ------------------------------------
        # [ATTENTION] This will only overwrite recomputeALL.json
        # lofims.resume("ALL", outputFileSize=20*1024)

    lofims.finalcheck(btsFileSize=70*1024**2, outFileSize=85*1024**2,
                      tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == "__main__":
        main()
