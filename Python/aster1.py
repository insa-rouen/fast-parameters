#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run calculation on aster1 server
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 02/11/2018
#
# Comments:
#     - 0.2: [24/11/18] Run DLC1.1b for 10 000 simulations at 25 m/s
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
from DLC11b import runFAST_multiprocess, runStress_multiprocess, runFatigue_multiprocess, runStressFatigue_multiprocess
#*============================= Modules Communs ================================
import os
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
    if psutil.cpu_percent() >= 90: return

    # Load Seeds ===============================================================
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('10000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM" and s[1] == "25"]
    seeds = liste

    
    # Run ======================================================================
    aster1 = server.Aster1(seeds,
                        '~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                        '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                        echo=False)

    # TurbSim ------------------------------------------------------------------
    # [ATTENTION] This will only overwrite recomputedSeeds.json
    # aster1.resume('TurbSim', outputFileSize=70*1024**2)

    # FAST ---------------------------------------------------------------------
    aster1.resume('FAST', inputFileSize=70*1024**2)        
    aster1.run(runFAST_multiprocess, True, False) #silence, echo
    time.sleep(5)
    
    # Stress -------------------------------------------------------------------
    # aster1.resume('Stress',inputFileSize=90*1024**2,outputFileSize=204*1024**2)
    # aster1.run(runStress_multiprocess, 10, False) # thetaStep=90, echo
    # time.sleep(5)
    
    # Stress + Fatigue ---------------------------------------------------------
    aster1.resume('Fatigue', inputFileSize=90*1024**2, outputFileSize=20*1024, compress=True)
    aster1.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
    time.sleep(5)

    # TurbSim + FAST + Stress + Fatigue ----------------------------------------
    # [ATTENTION] This will only overwrite recomputedSeeds.json
    # aster1.resume('ALL', outputFileSize=20*1024)

    # aster1.finalcheck(btsFileSize=70*1024**2, outFileSize=90*1024**2, tgzFileSize=20*1024**2, damFileSize=20*1024)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
