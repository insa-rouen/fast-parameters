#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRD testing codes
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 02/11/2018
#
# Comments:
#     - 0.0: 
#     
# Description:
#     
# 
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from tools import utils, server
from DLC11b import runFAST_multiprocess, runStress_multiprocess, runFatigue_multiprocess
#============================== Modules Communs ==============================
import time


#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    aster1 = server.Aster1('NTM',
                           '~/Eolien/Parameters/NREL_5MW_Onshore/Wind/1000seeds.json',
                           '~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
                           '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1',
                           False)
    # aster1.initiate()
    aster1.resume('TurbSim', outputFileSize=70*1024**2)

    # aster1.resume('FAST', inputFileSize=70*1024**2, outputFileSize=90*1024**2)
    # aster1.run(runFAST_multiprocess, True, True, True) # moveSource=True
    # time.sleep(5)

    # test.resume('Stress', inputFileSize=90*1024**2, outputFileSize=204*1024**2)
    # aster1.run(runStress_multiprocess, 10, True) # thetaStep=90
    # time.sleep(5)
    
    # test.resume('Fatigue', inputFileSize=204*1024**2, outputFileSize=20*1024)
    # aster1.run(runFatigue_multiprocess, False)



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
