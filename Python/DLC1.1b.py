#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - run 12*100 times simulation over all wind speed
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 22/10/2018
#
# Comments:
#     - 0.0: Init version
#     
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
import DLC1_1
from tools import utils
from pyturbsim import turb
#============================== Modules Communs ==============================
import json
import time
# import fileinput # iterate over lines from multiple input files
# import shutil # high-level file operations
# import subprocess # call a bash command e.g. 'ls'
import multiprocessing # enable multiprocessing
# from contextlib import contextmanager # utilities for with-statement contexts




#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def run_multiprocess(seed):
    ''' Run TurbSim + FAST
    '''
    # change workdirectory to DLC wind profiles and run TurbSim
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC/1.1/'):
        temp = turb.Turbulence_para(seed=seed)
        temp.run(silence=True)
    # run FAST
    temp = DLC1_1.DLC(seed=seed)
    temp.run(silence=True)

def runFAST_multiprocess(seed):
    # run FAST
    temp = DLC1_1.DLC(seed=seed)
    temp.run(silence=True)


#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    TIK = time.time()

    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC'):
        with open('100seeds.json', 'r') as f:
            seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "NTM"]
    seeds = [:600]

    # ----- Running on multi processor
    pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # [pool.apply_async(run_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    pool.map(runFAST_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the Pool instance
    pool.join() # join: wait for the worker processes to terminate

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    # TIK = time.time()

    # simu2 = DLC1_1.DLC(seed=seeds[0])
    # simu2.run(silence=False)

    # TOK = time.time()
    # print("|- Total time :", str(TOK-TIK), "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
