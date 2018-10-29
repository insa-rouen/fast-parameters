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
# 
# Description:
# 
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Communs ==============================
import json, time, platform, os, re
import fileinput # iterate over lines from multiple input files
import shutil # high-level file operations
import subprocess # call a bash command e.g. 'ls'
import multiprocessing # enable multiprocessing
#============================== Modules Personnels ==============================



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------
class Turbulence(object):
    """docstring for TurbSim"""
    def __init__(self, seed):
        self.seed = seed

        # Get OS platform name
        self._system = {'Linux':'TurbSim_glin64', 'Darwin':'TurbSim_gdar64'}
        self._turbsimName = self._system.get(platform.system())
        # input filename
        self.prefix = self.seed[0]        
        self.inpFile = '_'+self.seed[1]+'mps'
        self.suffix = ''
        self._extension = '.inp'
        self.filename = self.prefix + self.inpFile + self.suffix + self._extension

    def run(self, silence=False):
        print("|- Generating {} wind at {} m/s with seed ID {} ...".format(self.seed[0],
                                                              self.seed[1], self.seed[2]))
        self.change_seed()
        self._turbsim(silence)

    def change_seed(self):
        with fileinput.input(self.filename, inplace=True, backup='.bak') as f:
            for line in f:
                if "RandSeed1" in line:                    
                    print(self._replace(line, "RandSeed1", self.seed[2]), end="")
                else:
                    print(line, end="")

    def _replace(self, string, keyword, value):
        position = string.find(keyword)
        substring = string[:position]
        # replace float number (e.g. 12.34; 12.; .34)
        newtime = re.sub('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', str(value), substring)
        newline = newtime + string[position:]
        return newline

    def _turbsim(self, silence=False):
        command = '~/Eolien/FAST/{0} {1}'.format(self._turbsimName, self.filename)

        if silence:
            # print("|- Running TurbSim in silence mode ...")
            subprocess.check_output([command], shell=True)
        else:
            # print("|- Running TurbSim ...")
            subprocess.call([command], shell=True)


class Turbulence_para(Turbulence):
    """TurbSim class reserved for multiprocessing use"""
    def __init__(self, seed):
        super(Turbulence_para, self).__init__(seed)
        self.suffix = '_'+self.seed[2]

        self.make_copy()

    def make_copy(self):
        # origine .inp file
        with open(self.filename, 'r') as f:
            data = f.readlines()            
            for index, line in enumerate(data):
                if 'RandSeed1' in line:
                    data[index] = self._replace(line, 'RandSeed1', self.seed[2])
        
        # creat new .inp file
        self.filename = self.prefix + self.inpFile + self.suffix + self._extension
        with open(self.filename, 'w') as f:
            f.writelines(data)

    def run(self, silence=False):
        print("|- Generating {} wind at {} m/s with seed ID {} ...".format(self.seed[0],
                                                              self.seed[1], self.seed[2]))
        self._turbsim(silence)



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
    simulation = Turbulence_para(seed)
    simulation.run(True)



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # ----- Running on multi processor
    TIK = time.time()
    
    with open('../6seeds.json','r') as f:
        seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "ETM"]
    seeds = liste

    pool = multiprocessing.Pool(4) # define number of worker (= numbers of processor by default)
    # [pool.apply_async(run_multiprocess, args=s) for s in seeds] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    pool.map(run_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the Pool instance
    pool.join() # join: wait for the worker processes to terminate
    
    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    # TIK = time.time()
    # with open('../6seeds.json','r') as f:
    #     seeds = json.loads(f.read())

    # test = Turbulence_para(seeds[1])
    # test.run()

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
