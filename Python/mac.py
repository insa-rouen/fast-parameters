#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run calculation on Macbook Pro de Hao
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 01/12/2018
#
# Comments:
#     - 0.1: [15/12/18] Complete failed runs
#     - 0.2: [03/01/19] Complete failed runs for DLC1.3 ETM
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
# from DLC13b import runTurbSim_multiprocess, runFAST_multiprocess
# from DLC13b import runStressFatigue_multiprocess, runALL_multiprocess
#*============================= Modules Communs ================================
import time
import json



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
    # Load Seeds ===============================================================
    # with utils.cd('~/aster1/Wind'):
    #     with open('10000seeds.json', 'r') as f:
    #         seeds = json.loads(f.read())
    # liste = [s for s in seeds if s[0] == "NTM" and s[1] == "19"]
    # seeds = liste

    # Recalculate TurbSim + FAST + Stress
    # with utils.cd("~/aster1/Wind"):
    #     with open("10seeds.json", "r") as f:
    #        seeds1 = json.loads(f.read())
    #     #with open("failedRunsStress.json", "r") as f:
    #     #    seeds2 = json.loads(f.read())
        # with open("failedRunsFAST.json", "r") as f:
        #     seeds3 = json.loads(f.read())
    # #seeds1.extend(seeds2)
    # with utils.cd("~/lmn-cs/Wind"):
    #     with open("recomputeALL.json", "r") as f:
    #         seeds4 = json.loads(f.read())
    #     with open("failedRunsFAST.json", "r") as f:
    #         seeds5 = json.loads(f.read())
    
    # liste = [s for s in seeds1 if s[0] == "NTM"]
    # seeds1 = [ liste[303], liste[1700], ]
    seeds = [["NTM", "21", "-800757005"], ]
    # Run ======================================================================
    mac = server.Aster1(inputSeeds=seeds,
                    windPath="~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1",
                outputPath="~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1",
                        echo=False)
    mac.seeds = seeds # set list of seeds manually
    
    runMode = 2
    if runMode == 1:
        # All-In-One: TurbSim + FAST + Stress + Fatigue ------------------------
        mac.run(runALL_multiprocess, 10, "", False) # thetaStep, outputFolder,
                                                      # compress, silence, echo

    if runMode == 2:
        # TurbSim --------------------------------------------------------------
        mac.run(runTurbSim_multiprocess, False, True) # silence, echo
        # time.sleep(5)

        # FAST -----------------------------------------------------------------
        mac.run(runFAST_multiprocess, False, True) # silence, echo
        time.sleep(5)
        
        # Stress + Fatigue -----------------------------------------------------
        # mac.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
        # mac.resume('Fatigue', inputFileSize=85*1024**2,
        #               outputFileSize=20*1024, compress=True)
        # time.sleep(5)

        # TurbSim + FAST + Stress + Fatigue ------------------------------------
        # [ATTENTION] This will only overwrite recomputeALL.json
        # mac.resume("ALL", outputFileSize=20*1024)

    # mac.finalcheck(btsFileSize=70*1024**2, outFileSize=85*1024**2,
    #                tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == "__main__":
        main()
