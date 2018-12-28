#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.3 ETM
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 19/09/2018
#
# Comments:
#     - 0.0: Init version
# 
# Description:
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#* =========================== Modules Personnels =============================
from tools import utils
#* ============================= Modules Communs ==============================
import json, os, platform, re, time
import fileinput # iterate over lines from multiple input files
import shutil # high-level file operations
import subprocess # call a bash command e.g. 'ls'
import multiprocessing # enable multiprocessing
from contextlib import contextmanager # utilities for with-statement contexts



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------
class DLC(object):
    """docstring for DLC"""
    def __init__(self, seed, outputFolder='/', toLog=False):
        self.seed =  seed

        self.outputFolder = outputFolder
        self.toLog = toLog
        # Get OS platform name
        self._system = {'Linux':'FAST_glin64', 'Darwin':'FAST_gdar64'}
        self._fastName = self._system.get(platform.system())
        # some fixed path
        self.outputPath = os.path.expanduser(
                                     '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.3')
        self.inputPath = os.path.expanduser('~/Eolien/Parameters/Python/DLC1.3')
        self.prefix = '/DLC1.3_'
        self.servodyn = ''

        self.inflowFile = '{}{}_{}mps_IW.dat'.format(self.prefix, self.seed[0],
                                                     self.seed[1])
        self.fastFile = '{}{}_{}mps.fst'.format(self.prefix, self.seed[0], self.seed[1])

    def run(self, silence=False):
        print("|- Calculating {} at {} m/s with seed ID {} ...".format(self.seed[0],
                                                              self.seed[1], self.seed[2]))
        self.change_wind_profil()
        self._fast(silence)
        self.move()

    def move(self):
        source = self.inputPath+'{}{}_{}mps_{}.out'.format(self.prefix, self.seed[0],
                                                           self.seed[1], self.seed[2])
        destination = self.outputPath+self.outputFolder+'{}_{}mps_{}.out'.format(
                                                 self.seed[0], self.seed[1], self.seed[2])
        shutil.move(source, destination)

    def change_wind_profil(self):
        # InflowWind file
        with open(self.inputPath+self.inflowFile, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'Filename')

        filename = '{}{}_{}mps_IW_{}.dat'.format(self.prefix, self.seed[0], self.seed[1], 
                                                 self.seed[2])
        with open(self.inputPath+filename, 'w') as f:
            f.write(data)
        self.inflowFile = filename # update Inflow .dat file

        # Fast file
        with open(self.inputPath+self.fastFile, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'InflowFile')
        
        filename = '{}{}_{}mps_{}.fst'.format(self.prefix, self.seed[0], self.seed[1],
                                              self.seed[2])
        with open(self.inputPath+filename, 'w') as f:
            f.write(data)
        self.fastFile = filename # update .fst file

    def _change_string(self, text, keyword=''):
        if keyword == 'Filename':
            old = "DLC/1.3/{}_{}mps.bts".format(self.seed[0], self.seed[1])
            new = "DLC/1.3/{}_{}mps_{}.bts".format(self.seed[0],self.seed[1],self.seed[2])
            text = re.sub(old, new ,text)

        if keyword == 'InflowFile':
            old = "DLC1.3_{}_{}mps_IW.dat".format(self.seed[0], self.seed[1])
            new = "DLC1.3_{}_{}mps_IW_{}.dat".format(self.seed[0], self.seed[1],
                                                     self.seed[2])
            text = re.sub(old, new ,text)
        return text

    def _fast(self, silence=False):            
        with utils.cd('~/Eolien/FAST'):
            command = './{0} {1}{2}'.format(self._fastName, self.inputPath, self.fastFile)
            if silence:
                subprocess.check_output([command], shell=True)
            else:
                subprocess.call([command], shell=True)
                # Note:
                # When shell=False, args[:] is a command line to execute
                # When shell=True, args[0] is a command line to execute and args[1:] is 
                # arguments to sh



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def run_multiprocess(seed):
    simulation = DLC(seed)
    simulation.run()



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC'):
        with open('6seeds.json', 'r') as f:
            seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "ETM"]
    seeds = liste

    # ----- Running on multi processor
    TIK = time.time()    

    pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # [pool.apply_async(run_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    pool.map(run_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the Pool instance
    pool.join() # join: wait for the worker processes to terminate

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    # TIK = time.time()

    # simu2 = DLC(seed=seeds[0])
    # simu2.run(silence=False)

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
