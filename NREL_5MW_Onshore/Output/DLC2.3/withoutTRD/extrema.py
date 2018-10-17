#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: FIND MAXIMA AND MINIMA
# 
# 
#
#
# Authors: Hao BAI
# Date: 10/10/2018
#
# Version:
#   - 0.0: Initial version, enable multiprocessing
#   - 0.1: Use personlized packages
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from tools import utils
from pycrunch import amplitude
#============================== Modules Communs ==============================
import time



#-----------------------------------------------------------------------------------------
#                                          CLASS
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                       FUNCTIONS
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                      MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # bande of grid loss
    filelist = [str(t) for t in utils.frange(74.0, 76.1, 0.1)]

    channels = ['YawBrTDxt', 'YawBrTDyt', 'YawBrFxp', 'YawBrFyp', 'TwHt4FLxt','TwHt4FLyt',
                'TwrBsFxt', 'TwrBsFyt', 'TwrBsMxt', 'TwrBsMyt']
    TIK = time.time()  

    # # ----- Running on single processor
    # for file in filelist:
    #     amplitude.find_peak_valley(file, header=7, datarow=6009, startline=12,
    #                                channels=channels)

    # ----- Running on multi processor
    amplitude.find_peak_valley_multiprocess(filelist, 7, 6009, 12, channels)

    TOK = time.time()
    print('|- Total time :', TOK-TIK, 's')



#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
