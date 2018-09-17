#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1
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
                                     '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1')
        self.inputPath = os.path.expanduser('~/Eolien/Parameters/Python/DLC1.1')
        self.prefix = '/DLC1.1_'
        self.servodyn = ''

        self.inflowFile = '{}{}_{}mps_IW.dat'.format(self.prefix, self.seed[0], self.seed[1])
        self.fastFile = '{}{}_{}mps.fst'.format(self.prefix, self.seed[0], self.seed[1])

    def run(self, silence=False):
        self.change_wind_profil()
        self._fast(silence)
        self.move()

    def move(self):
        shutil.move(self.inputPath+'{}{}_{}mps_{}.out'.format(self.prefix, self.seed[0], self.seed[1], self.seed[2]),
                    self.outputPath+self.outputFolder)

    # def move_and_rename(self, time):
    #     shutil.move(self.inputPath+self.prefix+self.wind+self._suffix+'.out',
    #                self.outputPath+self.outputFolder+'/'+self.wind+'/'+str(time)+'.out')

    def change_wind_profil(self):
        # InflowWind file
        with open(self.inputPath+self.inflowFile, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'Filename')

        filename = '{}{}_{}mps_IW_{}.dat'.format(self.prefix, self.seed[0], self.seed[1], self.seed[2])
        with open(self.inputPath+filename, 'w') as f:
            f.write(data)
        self.inflowFile = filename # update Inflow .dat file

        # Fast file
        with open(self.inputPath+self.fastFile, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'InflowFile')
        
        filename = '{}{}_{}mps_{}.fst'.format(self.prefix, self.seed[0], self.seed[1], self.seed[2])
        with open(self.inputPath+filename, 'w') as f:
            f.write(data)
        self.fastFile = filename # update .fst file

    def _change_string(self, text, keyword=''):
        if keyword == 'Filename':
            old = "DLC/1.1/{}_{}mps.bts".format(self.seed[0], self.seed[1])
            new = "DLC/1.1/{}_{}mps_{}.bts".format(self.seed[0], self.seed[1], self.seed[2])
            text = re.sub(old, new ,text)

        if keyword == 'InflowFile':
            old = "DLC1.1_{}_{}mps_IW.dat".format(self.seed[0], self.seed[1])
            new = "DLC1.1_{}_{}mps_IW_{}.dat".format(self.seed[0], self.seed[1], self.seed[2])
            text = re.sub(old, new ,text)
        return text

    # def _replace(self, string, keyword, value):
    #     position = string.find(keyword)
    #     substring = string[:position]
    #     # replace float number (e.g. 12.34; 12.; .34)
    #     newtime = re.sub('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', str(value), substring)
    #     newline = newtime + string[position:]
    #     return newline

    def _fast(self, silence=False):            
        with cd('~/Eolien/FAST'):
            command = './{0} {1}{2}'.format(self._fastName, self.inputPath, self.fastFile)
            if silence:
                # print("|- Running FAST in silence mode ...")
                subprocess.check_output([command], shell=True)
            else:
                # print("|- Running FAST ...")
                subprocess.call([command], shell=True)
                # Note:
                # When shell=False, args[:] is a command line to execute
                # When shell=True, args[0] is a command line to execute and args[1:] is 
                # arguments to sh


class DLC_para(DLC):
    """DLC class reserved for multiprocessing use"""
    def __init__(self, wind='', gridLoss=0.0, outputFolder='/', toLog=False):
        super(DLC_para, self).__init__(wind=wind, outputFolder=outputFolder, toLog=toLog)
        self.time = gridLoss
        # some fixed path
        self.outputPath = os.path.expanduser(
                                        '~/Eolien/Parameters/Python/DLC1.1/Output/DLC1.1')
        self.inputPath = os.path.expanduser('~/Eolien/Parameters/Python/DLC1.1')
        self.prefix = '/DLC1.1_'
        self.servodyn = os.path.expanduser(
                               '~/Eolien/Parameters/Python/DLC1.1/WT/ServoDyn_DLC1.1.dat')

        self._suffix = '_'+str(gridLoss)
        self.__fst_copy = ''
        self.__servodyn_copy = ''

        self.make_copy()

    def make_copy(self):
        # ServoDyn.dat
        filename = self.servodyn
        with open(filename, 'r') as f:
            data = f.readlines()            
            for index, line in enumerate(data):
                if 'TPitManS' in line:
                    data[index] = self._replace(line, 'TPitManS', self.time+0.2)
                elif 'TimGenOf' in line:
                    data[index] = self._replace(line, 'TPitManS', self.time)
        
        filename = self.servodyn.rstrip('.dat')
        filename = filename+'_'+str(self.time)+'.dat'
        with open(filename, 'w') as f:
            f.writelines(data)
        self.__servodyn_copy = filename # update .dat file

        # .fst
        filename = self.inputPath+self.prefix+self.wind+'.fst'
        with open(filename, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'ServoFile')
        
        filename = self.inputPath+self.prefix+self.wind+'_'+str(self.time)+'.fst'
        with open(filename, 'w') as f:
            f.write(data)
        self.__fst_copy = filename # update .fst file

    def run(self, silence=False):
        print("|- Calculating the case of", self.time, "...")
        self._fast(silence)

    def _change_string(self, text, keyword, new=""):
        if keyword == 'ServoFile':
            old = "WT/ServoDyn_DLC1.1.dat"
            new = "WT/ServoDyn_DLC1.1_{}.dat".format(self.time)
            text = re.sub(old, new ,text)
            return text
    
    def _change_number(self, text, keyword, new):
        pass


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

def run_multiprocess(wind, gridloss):
    simulation = DLC_para(wind=wind, gridLoss=gridloss, outputFolder='/withoutTRD')
    simulation.run(True)
    simulation.move_and_rename(simulation.time)

#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # ----- Running on multi processor
    # TIK = time.time()    
    # timerange = frange(110, 140.5+0.01, 30)

    # wind = 'EOGR'
    # print("========== {} ==========".format(wind))
    # pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # [pool.apply_async(run_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    # pool.close() # close: call .close only when never going to submit more work to the Pool instance
    # pool.join() # join: wait for the worker processes to terminate

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    TIK = time.time()
    with open(os.path.expanduser('~/Eolien/Parameters/NREL_5MW_Onshore/DLC/6seeds.json'), 'r') as f:
        seeds = json.loads(f.read())

    simu2 = DLC(seed=seeds[0])
    # print("========== {} ==========".format(simu2.wind))
    simu2.run(silence=False)

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
