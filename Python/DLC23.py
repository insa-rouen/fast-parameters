#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC2.3 running code
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 25/07/2018
#
# Comments:
#     - 0.0: Init version
#     - 1.0: Enable multiprocessing
#     - 2.0: [20/11/2018] Adapt to new modules
# Description:
# Combine wind condition EOG with loss of grid at different moment
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#*============================= Modules Personnels ==============================
from pyfast import DLC
from pywind import iec
from tools import utils
#*============================= Modules Communs ==============================
import json



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def runIECWind(cutin, cutout, speedstep=0.1, silence=False):
    speedRange = utils.frange(0.0, 1.0, speedstep)
    condition = ["EOGR+{}".format(s) for s in speedRange]
    for v in range(cutin, cutout, 1):
        iec.get_DLC23(cutin=float(cutin-1), rated=float(v), cutout=float(cutout), condition=condition, silence=silence, rename=True)
    # the last case: wind speed = cut-out
    iec.get_DLC23(cutin=float(cutin), rated=float(v+1), cutout=float(cutout+1), condition=["EOGR+0.0"], silence=silence, rename=True)

def runFAST_multiprocess(list_gridloss, silence=False, echo=True):
    DLC.get_DLC23_multiprocess(list_gridloss, outputFolder='', silence=silence, echo=echo)

#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Generate wind profile ==============================================================
    runIECWind(cutin=3, cutout=25, speedstep=0.1, silence=True)
    return
    # Generate gridloss time =============================================================
    timerange = utils.frange(60, 90.5+0.01, 0.1)

    list_gridloss = []
    wind = 'EOG'
    for speed in utils.frange(3.0, 25.1, 0.1):
        for time in timerange:
            list_gridloss.append([wind, speed, str(time)])
    

    # Run ================================================================================
    runFAST_multiprocess(list_gridloss, silence=1, echo=0)



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
