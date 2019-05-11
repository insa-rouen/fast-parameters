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
#     - 0.4: [10/12/18] Run DLC1.1b for 10 000 simulations at 17 m/s
#     - 0.5: [15/12/18] Run DLC1.1b for 10 000 simulations at 13 m/s
#     - 0.5: [20/12/18] Run DLC1.1b for 10 000 simulations at 9 m/s
#     - 0.6: [23/12/18] Run DLC1.1b for 10 000 simulations at 5 m/s
#     - 0.7: [31/12/18] Run DLC1.3b for 10 000 simulations at 25 m/s
#     - 0.8: [05/01/19] Run DLC1.3b for 10 000 simulations at 3 m/s
#     - 0.9: [07/01/19] Run DLC1.3b for 10 000 simulations at 21 m/s
#     - 1.0: [11/01/19] Run DLC1.3b for 10 000 simulations at 15 m/s
#     - 1.1: [15/01/19] Run DLC1.3b for 10 000 simulations at 11 m/s
#     - 1.2: [19/01/19] Run DLC1.3b for 10 000 simulations at 9 m/s
#     - 1.3: [22/01/19] Run DLC1.3b for 10 000 simulations at 7 m/s
#     - 1.4: [28/01/19] Run DLC1.3b for 10 000 simulations at 5 m/s
#     - 2.0: [11/05/19] Change simulated time to 1 hour (60 min)
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
from DLC11b import runFAST_multiprocess, runStress_multiprocess
from DLC11b import runFatigue_multiprocess, runStressFatigue_multiprocess
from DLC11b import runALL_multiprocess
# from DLC13b import runTurbSim_multiprocess, runFAST_multiprocess
# from DLC13b import runStressFatigue_multiprocess, runALL_multiprocess
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
    # with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
    #     with open('10000seeds.json', 'r') as f:
    #         seeds = json.loads(f.read())
    # liste = [s for s in seeds if s[0] == "ETM" and s[1] == "5"]
    # seeds = liste

    seeds = [["NTM",  "3",  "3333"],
             ["NTM",  "5", "-5555"],
             ["NTM",  "7",  "7777"],
             ["NTM",  "9", "-9999"],
             ["NTM", "11",  "1111"],
             ["NTM", "13", "-1313"],
             ["NTM", "15",  "1515"],
             ["NTM", "17", "-1717"],
             ["NTM", "19",  "1919"],
             ["NTM", "21", "-2121"],
             ["NTM", "23",  "2323"],
             ["NTM", "25", "-2525"],
            ]
    # Run ======================================================================
    aster1 = server.Aster1(inputSeeds=seeds,
                    windPath='~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                outputPath='~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                           echo=False)
    
    runMode = 1
    if runMode == 1:
        # All-In-One: TurbSim + FAST + Stress + Fatigue ------------------------
        # [ATTENTION] This will only overwrite recomputeALL.json
        # aster1.resume('ALL', outputFileSize=20*1024)
        aster1.run(runALL_multiprocess, 10, "", True) # thetaStep, outputFolder,
            # compress, silence, echo

    if runMode == 2:
        # TurbSim --------------------------------------------------------------
        # [ATTENTION] This will only overwrite recomputeTurbSim.json
        # aster1.resume('TurbSim', outputFileSize=70*1024**2)

        # FAST -----------------------------------------------------------------
        aster1.resume('FAST', inputFileSize=70*1024**2)        
        aster1.run(runFAST_multiprocess, True, False) #silence, echo
        time.sleep(5)
        
        # Stress + Fatigue -----------------------------------------------------
        aster1.resume('Fatigue', inputFileSize=85*1024**2, 
            outputFileSize=20*1024, compress=True)
        aster1.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo
        aster1.resume('Fatigue', inputFileSize=85*1024**2,     
            outputFileSize=20*1024, compress=True)
        time.sleep(5)

    # Final checking phase -----------------------------------------------------
    aster1.finalcheck(btsFileSize=70*1024**2, outFileSize=85*1024**2,
                      tgzFileSize=20*1024**2, damFileSize=20*1024)

    aster1.sendmail('hao.bai@insa-rouen.fr')


#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
