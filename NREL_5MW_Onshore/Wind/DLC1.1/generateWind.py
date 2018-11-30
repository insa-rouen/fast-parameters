#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Creat wind profil at the same time 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 15/09/2018
#
# Comments:
#     - 0.0: Init version
#     - 0.1: use personalized package turb
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
from pywind import turb
#============================== Modules Communs ==============================
import time
import json
import multiprocessing # enable multiprocessing



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def run_multiprocess(seed):
    simulation = turb.Turbulence_para(seed)
    simulation.run(True)



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    TIK = time.time()
    
    with open('../100seeds.json','r') as f:
        seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "NTM"]
    seeds = liste[:600]

    # ----- Running on multi processor
    pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # [pool.apply_async(run_multiprocess, args=s) for s in seeds] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    pool.map(run_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the Pool instance
    pool.join() # join: wait for the worker processes to terminate
    
    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")

    # ----- Running on single processor
    # test = turb.Turbulence_para(seeds[0])
    # test.run()

    # TOK = time.time()
    # print("|- Total time :", str(TOK-TIK), "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
