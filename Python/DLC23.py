#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC2.3 running code
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Date: 25/07/2018
#
# Comments:
#     - 0.0: Init version
#     - 1.0: Enable multiprocessing
#     - 2.0: [20/11/2018] Adapt to new modules
#     - 2.1: [30/11/2018] Add reliability study for time of grid loss
# Description:
# Combine wind condition EOG with loss of grid at different moment
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from pyfast import DLC
from pywind import iec
from tools import utils
#* ============================= Modules Communs ==============================
import  re
import json
import copy
from pathlib import Path



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def runIECWind(cutin, cutout, speedstep=0.1, silence=False):
    speedRange = utils.frange(0.0, 1.0, speedstep)
    condition = ["EOGR+{}".format(s) for s in speedRange]
    for v in range(cutin, cutout, 1):
        iec.get_DLC23(cutin=float(cutin-1), rated=float(v),cutout=float(cutout),
                      condition=condition, silence=silence, rename=True)
    # the last case: wind speed = cut-out
    iec.get_DLC23(cutin=float(cutin), rated=float(v+1), cutout=float(cutout+1),
                  condition=["EOGR+0.0"], silence=silence, rename=True)

def generateInflowWind(speedRange):
    template = Path("./DLC2.3/DLC2.3_EOG_*.IW.dat").open().readlines()
    for v in speedRange:
        script = copy.deepcopy(template)
        script[1] = re.sub('\*', str(v), script[1])
        script[15] = re.sub('\*', str(v), script[15])
        file = Path("./DLC2.3/DLC2.3_EOG_{}.IW.dat".format(v))
        file.open("w").writelines(script)

def _change_number(string, keyword, value):
    position = string.find(keyword)
    substring = string[:position]
    # replace float number (e.g. 12.34; 12.; .34)
    new_substring = re.sub('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', str(value), 
                           substring)
    newline = new_substring + string[position:]
    return newline

def runFAST_multiprocess(list_gridloss, silence=False, echo=True):
    DLC.get_DLC23_multiprocess(list_gridloss, outputFolder='', silence=silence,
                               echo=echo)


def _find(path, pattern, size):
    ''' size: minimum size in bytes (1 GB = 1024 MB = 1024^2 KB = 1024^3 Bytes) [num]
    '''
    with utils.cd(path):
        p = Path().expanduser()
        matched = sorted(p.glob(pattern))
        if size is None:
            result = [x.stem.split('.')[0] for x in matched]
        else:
            result = [x.stem for x in matched if x.stat().st_size >= size]
    return result

def _convertToSeed(list_filebase):
    seeds = []
    for filebase in list_filebase:
        seed = filebase.split('_')
        seed[1] = float(seed[1])
        seed[2] = float(seed[2])
        seeds.append(seed)
    return seeds

#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    wind = 'EOG'
    speedRange = utils.frange(3.0, 25.1, 0.1) # wind speed [m/s]
    timeRange = utils.frange(70.0, 80.1, 0.1) # grid loss time [s]
    
    # Restart unfinished tasks
    outputList =_find("~/Eolien/Parameters/Python/DLC2.3/Output/DLC2.3", '*.out', 25*1024**2)
    # find out wind profiles that are planned to be generated
    inputList = ["{}_{}_{}".format(wind, v, t) for v in speedRange
                        for t in timeRange]
    recompute = list(set(inputList).difference(set(outputList)))
    list_recompute = _convertToSeed(recompute)

    # Generate wind profile ====================================================
    runIECWind(cutin=3, cutout=25, speedstep=0.1, silence=True)
    generateInflowWind(speedRange)
    
    # Generate gridloss time ===================================================
    list_gridloss = []
    for speed in speedRange:
        for time in timeRange:
            list_gridloss.append([wind, speed, time])
    
    # For testing ...
    # list_gridloss = []
    # wind = 'EOG'
    # for speed in ['O',]:
    #    for time in timeRange:
    #        list_gridloss.append([wind, speed, str(time)])
    # Run ======================================================================
    # list_gridloss = [["EOG", 25.0, 75.7], ["EOG", "O", 75.7]] # testing
    runFAST_multiprocess(list_recompute, silence=1, echo=0)



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
