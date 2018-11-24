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
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('10000seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    liste = [s for s in seeds if s[0] == "NTM" and s[1] == "25"]
    seeds = liste

    
    # Run ======================================================================
    flag = True
    wait = None
    sleepTime = 30 * 60 # in secondes
    while flag:
        aster1 = server.Aster1(seeds,
                            '~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                            '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                            echo=False)

        # TurbSim ------------------------------------------------------------------
        # [ATTENTION] This will only overwrite recomputedSeeds.json
        # aster1.resume('TurbSim', outputFileSize=70*1024**2)

        # FAST ---------------------------------------------------------------------
        aster1.resume('FAST', inputFileSize=70*1024**2)
        # a way to exit based on unchanged files during a fixed time
        if len(aster1.seeds) < os.cpu_count():
            if wait is None:
                wait = len(aster1.seeds)
                time.sleep(sleepTime)
                continue
            else:
                now = len(aster1.seeds)
                if now == wait:
                    flag = False
                else:
                    wait = now
                    time.sleep(sleepTime)
                    continue
        
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

        del aster1


#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
