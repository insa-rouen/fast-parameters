#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 28/10/2018
#
# Comments:
#     - 0.0: Init version
#     
# Description:
#     Prepare a general class for DLC input scripts
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from tools import utils
import sys, IPython # to colorize traceback errors in terminal
sys.excepthook = IPython.core.ultratb.ColorTB()
#============================== Modules Communs ==============================
import json, os, platform, re, time
import fileinput # iterate over lines from multiple input files
import shutil # high-level file operations
import subprocess # call a bash command e.g. 'ls'
import multiprocessing # enable multiprocessing



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------
class DLC(object):
    ''' Specify FAST input scripts for DLC
        *ATTRIBUTES*
    '''
    def __init__(self, list_filename, outputFolder='/', toLog=False):
        self.list_filename =  list_filename
        self.outputFolder = outputFolder
        self.toLog = toLog
        # Get OS platform name
        # some fixed path
       
        # self.servodyn = ''
        self.run()

    def run(self, silence=False, ignore=False):
        for filename in self.list_filename:
            self.change_wind_profil(filename)


    def change_wind_profil(self, filename):
        self.prefix = filename[3:6]
        
        # InflowWind input script --------------------------------------------------------
        with open(filename, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'Filename')

        with open(filename, 'w') as f:
            f.write(data)
        


    def _change_string(self, text, keyword=''):
        if keyword == 'Filename':
            old = "DLC/{}/".format(self.prefix)
            new = "Wind/DLC{}/".format(self.prefix)
            text = re.sub(old, new ,text)

        return text




#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def run_multiprocess(seed):
    simulation = DLC(seed)
    simulation.run(True)



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Load seeds
    liste = ['DLC0.1.IW.dat', 'DLC0.2_EOGR.IW.dat', 'DLC1.1_NTM_11mps.IW.dat', 'DLC1.1_NTM_13mps.IW.dat', 'DLC1.1_NTM_15mps.IW.dat', 'DLC1.1_NTM_17mps.IW.dat', 'DLC1.1_NTM_19mps.IW.dat', 'DLC1.1_NTM_21mps.IW.dat', 'DLC1.1_NTM_23mps.IW.dat', 'DLC1.1_NTM_25mps.IW.dat', 'DLC1.1_NTM_3mps.IW.dat', 'DLC1.1_NTM_5mps.IW.dat', 'DLC1.1_NTM_7mps.IW.dat', 'DLC1.1_NTM_9mps.IW.dat', 'DLC1.2_NTM_11mps.IW.dat', 'DLC1.2_NTM_13mps.IW.dat', 'DLC1.2_NTM_15mps.IW.dat', 'DLC1.2_NTM_17mps.IW.dat', 'DLC1.2_NTM_19mps.IW.dat', 'DLC1.2_NTM_21mps.IW.dat', 'DLC1.2_NTM_23mps.IW.dat', 'DLC1.2_NTM_25mps.IW.dat', 'DLC1.2_NTM_3mps.IW.dat', 'DLC1.2_NTM_5mps.IW.dat', 'DLC1.2_NTM_7mps.IW.dat', 'DLC1.2_NTM_9mps.IW.dat', 'DLC1.3_ETM_11mps.IW.dat', 'DLC1.3_ETM_13mps.IW.dat', 'DLC1.3_ETM_15mps.IW.dat', 'DLC1.3_ETM_17mps.IW.dat', 'DLC1.3_ETM_19mps.IW.dat', 'DLC1.3_ETM_21mps.IW.dat', 'DLC1.3_ETM_23mps.IW.dat', 'DLC1.3_ETM_25mps.IW.dat', 'DLC1.3_ETM_3mps.IW.dat', 'DLC1.3_ETM_5mps.IW.dat', 'DLC1.3_ETM_7mps.IW.dat', 'DLC1.3_ETM_9mps.IW.dat', 'DLC1.4_ECD+R+2.0.IW.dat', 'DLC1.4_ECD+R-2.0.IW.dat', 'DLC1.4_ECD+R.IW.dat', 'DLC1.4_ECD-R+2.0.IW.dat', 'DLC1.4_ECD-R-2.0.IW.dat', 'DLC1.4_ECD-R.IW.dat', 'DLC1.5_EWSH+3.0.IW.dat', 'DLC1.5_EWSH-3.0.IW.dat', 'DLC1.5_EWSV+3.0.IW.dat', 'DLC1.5_EWSV-3.0.IW.dat', 'DLC2.1_NTM_11mps.IW.dat', 'DLC2.1_NTM_13mps.IW.dat', 'DLC2.1_NTM_15mps.IW.dat', 'DLC2.1_NTM_17mps.IW.dat', 'DLC2.1_NTM_19mps.IW.dat', 'DLC2.1_NTM_21mps.IW.dat', 'DLC2.1_NTM_23mps.IW.dat', 'DLC2.1_NTM_25mps.IW.dat', 'DLC2.1_NTM_3mps.IW.dat', 'DLC2.1_NTM_5mps.IW.dat', 'DLC2.1_NTM_7mps.IW.dat', 'DLC2.1_NTM_9mps.IW.dat', 'DLC2.2_NTM_11mps.IW.dat', 'DLC2.2_NTM_13mps.IW.dat', 'DLC2.2_NTM_15mps.IW.dat', 'DLC2.2_NTM_17mps.IW.dat', 'DLC2.2_NTM_19mps.IW.dat', 'DLC2.2_NTM_21mps.IW.dat', 'DLC2.2_NTM_23mps.IW.dat', 'DLC2.2_NTM_25mps.IW.dat', 'DLC2.2_NTM_3mps.IW.dat', 'DLC2.2_NTM_5mps.IW.dat', 'DLC2.2_NTM_7mps.IW.dat', 'DLC2.2_NTM_9mps.IW.dat', 'DLC2.3_EOGI.IW.dat', 'DLC2.3_EOGO.IW.dat', 'DLC2.3_EOGR+2.0.IW.dat', 'DLC2.3_EOGR-2.0.IW.dat', 'DLC2.3_EOGR.IW.dat', 'DLC2.4_NTM_11mps.IW.dat', 'DLC2.4_NTM_13mps.IW.dat', 'DLC2.4_NTM_15mps.IW.dat', 'DLC2.4_NTM_17mps.IW.dat', 'DLC2.4_NTM_19mps.IW.dat', 'DLC2.4_NTM_21mps.IW.dat', 'DLC2.4_NTM_23mps.IW.dat', 'DLC2.4_NTM_25mps.IW.dat', 'DLC2.4_NTM_3mps.IW.dat', 'DLC2.4_NTM_5mps.IW.dat', 'DLC2.4_NTM_7mps.IW.dat', 'DLC2.4_NTM_9mps.IW.dat', 'DLC3.1_NWP_11mps.IW.dat', 'DLC3.1_NWP_13mps.IW.dat', 'DLC3.1_NWP_15mps.IW.dat', 'DLC3.1_NWP_17mps.IW.dat', 'DLC3.1_NWP_19mps.IW.dat', 'DLC3.1_NWP_21mps.IW.dat', 'DLC3.1_NWP_23mps.IW.dat', 'DLC3.1_NWP_25mps.IW.dat', 'DLC3.1_NWP_3mps.IW.dat', 'DLC3.1_NWP_5mps.IW.dat', 'DLC3.1_NWP_7mps.IW.dat', 'DLC3.1_NWP_9mps.IW.dat', 'DLC3.2_EOGI.IW.dat', 'DLC3.2_EOGO.IW.dat', 'DLC3.2_EOGR+0.0.IW.dat', 'DLC3.2_EOGR+2.0.IW.dat', 'DLC3.2_EOGR-2.0.IW.dat', 'DLC3.3_EDC+I.IW.dat', 'DLC3.3_EDC+O.IW.dat', 'DLC3.3_EDC+R+0.0.IW.dat', 'DLC3.3_EDC+R+2.0.IW.dat', 'DLC3.3_EDC+R-2.0.IW.dat', 'DLC3.3_EDC-I.IW.dat', 'DLC3.3_EDC-O.IW.dat', 'DLC3.3_EDC-R+0.0.IW.dat', 'DLC3.3_EDC-R+2.0.IW.dat', 'DLC3.3_EDC-R-2.0.IW.dat', 'DLC4.1_NWP_11mps.IW.dat', 'DLC4.1_NWP_13mps.IW.dat', 'DLC4.1_NWP_15mps.IW.dat', 'DLC4.1_NWP_17mps.IW.dat', 'DLC4.1_NWP_19mps.IW.dat', 'DLC4.1_NWP_21mps.IW.dat', 'DLC4.1_NWP_23mps.IW.dat', 'DLC4.1_NWP_25mps.IW.dat', 'DLC4.1_NWP_3mps.IW.dat', 'DLC4.1_NWP_5mps.IW.dat', 'DLC4.1_NWP_7mps.IW.dat', 'DLC4.1_NWP_9mps.IW.dat', 'DLC4.2_EOGO.IW.dat', 'DLC4.2_EOGR+0.0.IW.dat', 'DLC4.2_EOGR+2.0.IW.dat', 'DLC4.2_EOGR-2.0.IW.dat', 'DLC5.1_NTM_11.4mps.IW.dat', 'DLC5.1_NTM_13.4mps.IW.dat', 'DLC5.1_NTM_25mps.IW.dat', 'DLC5.1_NTM_9.4mps.IW.dat', 'DLC6.1_EWM50.IW.dat', 'DLC6.2_EWM50.IW.dat', 'DLC6.3_EWM01.IW.dat', 'DLC6.4_NTM_0mps.IW.dat', 'DLC6.4_NTM_10mps.IW.dat', 'DLC6.4_NTM_12mps.IW.dat', 'DLC6.4_NTM_14mps.IW.dat', 'DLC6.4_NTM_16mps.IW.dat', 'DLC6.4_NTM_18mps.IW.dat', 'DLC6.4_NTM_20mps.IW.dat', 'DLC6.4_NTM_22mps.IW.dat', 'DLC6.4_NTM_24mps.IW.dat', 'DLC6.4_NTM_26mps.IW.dat', 'DLC6.4_NTM_28mps.IW.dat', 'DLC6.4_NTM_2mps.IW.dat', 'DLC6.4_NTM_30mps.IW.dat', 'DLC6.4_NTM_32mps.IW.dat', 'DLC6.4_NTM_34mps.IW.dat', 'DLC6.4_NTM_35mps.IW.dat', 'DLC6.4_NTM_4mps.IW.dat', 'DLC6.4_NTM_6mps.IW.dat', 'DLC6.4_NTM_8mps.IW.dat', 'DLC7.1_EWM01.IW.dat', ]



    # # ----- Running on multi processor
    # TIK = time.time()    

    # pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # # [pool.apply_async(run_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    # pool.map(run_multiprocess, seeds)
    # pool.close() # close: call .close only when never going to submit more work to the Pool instance
    # pool.join() # join: wait for the worker processes to terminate

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    simu2 = DLC(liste)
    simu2.run(silence=False, ignore=True)


#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
