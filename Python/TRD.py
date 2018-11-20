#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRD testing codes
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 24/10/2018
#
# Comments:
#     - 0.0: Mean wind speed fixed at cut-out and grid loss time fixed at 74.9s
#     - 0.1: [20/11/2018] Adapt to new modules
# Description:
#     - Combine wind condition EOG with loss of grid and induce Pitch-to-Feather 
#       and HSS brake shutdown
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from pyfast import DLC
from tools import utils
#*============================= Modules Communs ==============================



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    DLC.get_TRD(mode1=[290, 30, -90, -20], gridloss=['EOG', 'R', '77.7'],
                outputFolder='', silence=0, echo=1)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
