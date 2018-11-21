#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Optimization: TRD mode 1 parameters
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
#
# Comments:
#     - 0.0: [20/11/2018] Initial version
#
# Description:
#     
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                   MODULES
#!------------------------------------------------------------------------------
#*         ==================== Modules Personnels ====================
from pyfast import DLC
from tools import utils
#*           ==================== Modules Communs ====================



#!------------------------------------------------------------------------------
#!                               CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                             FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def run_TRD(mode1, gridloss, case='DLC2.3', outputFolder='', silence=False,
            echo=False):
    temp = DLC.TRD(mode1=mode1,gridloss=gridloss,case=case,outputFolder=outputFolder, 
               echo=echo)
    # set path
    temp.workPath = "~/Eolien/Parameters/Python/Optimization"
    temp.outputPath = "~/Eolien/Parameters/Python/Optimization/Output"
    temp.windPath = "~/Eolien/Parameters/Python/Optimization/Wind"
    temp.wtPath = "~/Eolien/Parameters/Python/Optimization/WT"
    temp.logPath = "~/Eolien/Parameters/Python/Optimization/log"
    # run calculation
    temp.run(silence)
    return mode1



#!------------------------------------------------------------------------------
#!                                MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    run_TRD(mode1=[277.8, 26.7, -86.712, -17.0222], gridloss=['EOG', 'O'],
            outputFolder='', silence=0, echo=1)



#!------------------------------------------------------------------------------
#!                                 DEBUG TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
