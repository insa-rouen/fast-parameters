#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC0.1 running code
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 28/11/2018
#
# Comments:
#     - 0.0: Init version
#
# Description:
# The results calculated in this DLC will be used to initiate other DLCs
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================ Modules Personnels ==============================
from pyfast import DLC
from pywind import iec
from tools import utils
from pywt import elasto
#* ============================= Modules Communs ==============================



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    # Generate wind profile ====================================================
    windSpeedRange = utils.frange(3.0, 25.1, 0.1)
    iec.get_uniform(speedRange=windSpeedRange)
    
    # Run FAST =================================================================
    DLC.get_DLC01_multiprocess(list_speed=windSpeedRange, silence=True)
    
    # Generate ElastoDyn script ================================================
    elasto.generate_script(speedRange=windSpeedRange)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
