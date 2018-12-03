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
    if psutil.cpu_percent() >= 60: return

    # Load Seeds ===============================================================
    with utils.cd('~/aster1/Wind'):
        with open('10000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM" and s[1] == "21"]
    seeds = liste
    
    # Run ======================================================================
    lmn_cs = server.Aster1(inputSeeds=seeds,
                    windPath='~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                outputPath='~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                           echo=False)

    # TurbSim ------------------------------------------------------------------
    lmn_cs.run(runTurbSim_multiprocess, True, False) #silence, echo
    time.sleep(5)

    # FAST ---------------------------------------------------------------------
    lmn_cs.run(runFAST_multiprocess, True, False) #silence, echo
    time.sleep(5)
    
    # Stress + Fatigue ---------------------------------------------------------
    lmn_cs.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
    # lmn_cs.resume('Fatigue', inputFileSize=85*1024**2, outputFileSize=20*1024, compress=True)
    time.sleep(5)

    # TurbSim + FAST + Stress + Fatigue ----------------------------------------
    # [ATTENTION] This will only overwrite recomputeALL.json
    # lmn_cs.resume('ALL', outputFileSize=20*1024)

    lmn_cs.finalcheck(btsFileSize=70*1024**2, outFileSize=85*1024**2, tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
