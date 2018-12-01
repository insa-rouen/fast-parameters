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
from DLC11b import runStressFatigue_multiprocess
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
    if psutil.cpu_percent() >= 80: return

    # Load Seeds ===============================================================
    # Recalculate TurbSim + FAST + Stress
    with utils.cd("~/aster1/Wind"):
        with open("failedRunsFAST.json", "r") as f:
            seeds1 = json.loads(f.read())
        with open("failedRunsStress.json", "r") as f:
            seeds2 = json.loads(f.read())
    seeds1.extend(seeds2)
    seeds = seeds1
    
    # Run ======================================================================
    lofims = server.Aster1(seeds,
                           "~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1",
                           "~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1",
                           echo=False)
    print(len(seeds))
    lofims.seeds = seeds[:2] # set list of seeds manually

    # TurbSim ------------------------------------------------------------------
    lofims.run(runTurbSim_multiprocess, True, False) #silence, echo
    time.sleep(5)

    # FAST ---------------------------------------------------------------------
    lofims.run(runFAST_multiprocess, True, False) #silence, echo
    time.sleep(5)
    
    # Stress + Fatigue ---------------------------------------------------------
    lofims.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
    time.sleep(5)

    # TurbSim + FAST + Stress + Fatigue ----------------------------------------
    # [ATTENTION] This will only overwrite recomputedSeeds.json
    # lofims.resume("ALL", outputFileSize=20*1024)

    lofims.finalcheck(btsFileSize=70*1024**2, outFileSize=90*1024**2, tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == "__main__":
        main()
