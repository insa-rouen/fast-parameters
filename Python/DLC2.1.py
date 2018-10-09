#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC2.1
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.1
# Date: 21/09/2018
#
# Comments:
#     - 0.0: Init version
#     - 0.1: add reuse mode
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Communs ==============================
import json, os, platform, re, time
import fileinput # iterate over lines from multiple input files
import shutil # high-level file operations
import subprocess # call a bash command e.g. 'ls'
import multiprocessing # enable multiprocessing
from contextlib import contextmanager # utilities for with-statement contexts
#============================== Modules Personnels ==============================



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------
@contextmanager
def cd(newdir):
    prevdir = os.getcwd() # save current working path
    os.chdir(os.path.expanduser(newdir)) # change directory
    try:
        yield
    finally:
        os.chdir(prevdir) # revert to the origin workinng path

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
                                     '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC2.1')
        self.inputPath = os.path.expanduser('~/Eolien/Parameters/Python/DLC2.1')
        self.prefix = '/DLC2.1_'
        self.servodyn = ''

        self.inflowFile = '{}{}_{}mps_IW.dat'.format(self.prefix, self.seed[0],
                                                     self.seed[1])
        self.fastFile = '{}{}_{}mps.fst'.format(self.prefix, self.seed[0], self.seed[1])
        self.debug = ""

    def run(self, silence=False, reuse=False):
        print("|- Calculating {} at {} m/s with seed ID {} ...".format(self.seed[0],
                                                              self.seed[1], self.seed[2]))
        self.change_wind_profil(reuse)
        
        self._fast(silence)
        self.move()

    def move(self):
        source = self.inputPath+'{}{}_{}mps_{}.out'.format(self.prefix, self.seed[0],
                                                           self.seed[1], self.seed[2])
        destination = self.outputPath+self.outputFolder+'{}_{}mps_{}.out'.format(
                                                 self.seed[0], self.seed[1], self.seed[2])
        shutil.move(source, destination)

    def change_wind_profil(self, reuse):
        # InflowWind input file ----------------------------------------------------------
        filename = '{}{}_{}mps_IW_{}.dat'.format(self.prefix, self.seed[0], self.seed[1], 
                                                 self.seed[2])
        if reuse is False:
            # load template and change parameter
            with open(self.inputPath+self.inflowFile, 'r') as f:
                data = f.read()
                data = self._change_string(data, 'Filename')
            # write to new file
            with open(self.inputPath+filename, 'w') as f:
                f.write(data)
        
        self.inflowFile = filename # update Inflow .dat file

        # Fast input file ----------------------------------------------------------------
        filename = '{}{}_{}mps_{}.fst'.format(self.prefix, self.seed[0], self.seed[1],
                                              self.seed[2])
        if reuse is False:
            # load template and change parameter
            with open(self.inputPath+self.fastFile, 'r') as f:
                data = f.read()
                data = self._change_string(data, 'InflowFile')
            # write to new file
            with open(self.inputPath+filename, 'w') as f:
                f.write(data)
        
        self.fastFile = filename # update .fst file

    def _change_string(self, text, keyword=''):
        if keyword == 'Filename':
            old = "DLC/2.1/{}_{}mps.bts".format(self.seed[0], self.seed[1])
            new = "DLC/2.1/{}_{}mps_{}.bts".format(self.seed[0],self.seed[1],self.seed[2])
            text = re.sub(old, new ,text)

        if keyword == 'InflowFile':
            old = "DLC2.1_{}_{}mps_IW.dat".format(self.seed[0], self.seed[1])
            new = "DLC2.1_{}_{}mps_IW_{}.dat".format(self.seed[0], self.seed[1],
                                                     self.seed[2])
            text = re.sub(old, new ,text)
        return text

    def _fast(self, silence=False):            
        with cd('~/Eolien/FAST'):
            command = './{0} {1}{2}'.format(self._fastName, self.inputPath, self.fastFile)
            try:
                if silence:
                    output = subprocess.check_output([command], shell=True)
                else:
                    output = subprocess.check_call([command], shell=True)
                    # Note:
                    # When shell=False, args[:] is a command line to execute
                    # When shell=True, args[0] is a command line to execute and args[1:] 
                    # is arguments to sh
            except subprocess.CalledProcessError as error:
                errorMessage = error.output
                debug = True
            except Exception as e:
                raise e
            else:
                debug = False

        if debug:
            directory = self.inputPath + '/log'
            if not os.path.exists(directory): # create new folder is non-exist
                os.makedirs(directory)
            with open(directory+'/'+self.seed[2]+'.bug', 'wb') as f:
                f.write(errorMessage)
            print("[Error] FAST has an error for simulation {}.".format(self.seed))



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------
def frange(start, stop=None, step=1, precision=None):
    if precision is None:
        fois = 1e7
    else:
        fois = 10**precision
    
    new_start = int(start * fois)
    new_stop = int(stop * fois)
    new_step = int(step * fois)
    r = range(new_start, new_stop, new_step)
    
    l = [i/fois for i in r]
    return l

def run_multiprocess(seed):
    simulation = DLC(seed)
    simulation.run(silence=True, reuse=False)



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # Load seeds
    with cd('~/Eolien/Parameters/NREL_5MW_Onshore/DLC'):
        with open('12seeds.json', 'r') as f:
            seeds = json.loads(f.read())
    seeds = [s for s in seeds if s[0] == "NTM"]
    TIK = time.time()


    # ----- Testing
    # seed = ["NTM", "5", "-1494309489"]
    # seed = ["NTM", "3", "-615392578"]
    # seed = ["NTM", "17", "537417508"]
    # seeds = [["NTM", "5", "-1494309489"], ["NTM", "3", "-615392578"], liste[-1]]
    # run_multiprocess(seed)
    
    # Recalculate cases that have been stopped by error on aster1
    # bugseeds = []
    # bugs = [-1735756529, -188411971, -2114264661, 36387814, 52346169, 537417508, 
    #         -615392578, 741781101, 888802706, ]
    # for s in seeds:
    #     for b in bugs:
    #         if s[2] == str(b):
    #             bugseeds.append(s)
    # seeds = bugseeds


    # ----- Running on multi processor
    # define number of worker (= numbers of processor by default)
    pool = multiprocessing.Pool()
    pool.map(run_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the
                 # Pool instance
    pool.join() # join: wait for the worker processes to terminate


    # ----- Running on single processor
    # simu2 = DLC(seed=seeds[0])
    # simu2.run(silence=False)


    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
