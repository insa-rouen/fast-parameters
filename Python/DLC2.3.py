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
#
# Description:
# Combine wind condition EOG with loss of grid at different moment
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Communs ==============================
import os, platform, re, time
import fileinput # iterate over lines from multiple input files
import shutil # high-level file operations
import subprocess # call a bash command e.g. 'ls'
from multiprocessing import Pool # enable multiprocessing
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
    def __init__(self, wind='', gridLossTime=[0,0,0], outputFolder='/', toLog=False):
        self.wind =  wind
        self.time = {'start':gridLossTime[0],'stop':gridLossTime[1],'step':gridLossTime[2]}
        self.outputFolder = outputFolder
        self.toLog = toLog
        # Get OS platform name
        self._system = {'Linux':'FAST_glin64', 'Darwin':'FAST_gdar64'}
        self._fastName = self._system.get(platform.system())
        # some fixed path
        self.__outputPath = os.path.expanduser(
                                     '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC2.3')
        self._fstPath = os.path.expanduser('~/Eolien/Parameters/NREL_5MW_Onshore')
        self._prefix = '/DLC2.3_'
        self.__servodyn = os.path.expanduser(
                            '~/Eolien/Parameters/NREL_5MW_Onshore/WT/ServoDyn_DLC2.3.dat')
        self._suffix = ''

    def run(self, loop=False, silence=False):
        if loop:
            for t in frange(self.time['start'], self.time['stop']+self.time['step'],
                            self.time['step']):
                print("|- Simulating loss of grid at", t,"s")
                self.change_gridloss(t)
                self._fast(silence)
                self.move_and_rename(t)
                print("[ OK ] Output file has been moved to {} folder !"
                      .format(self.outputFolder))
        else:
            self._fast(silence)

    def move_and_rename(self, time):
        shutil.move(self._fstPath+self._prefix+self.wind+'.out',
                   self.__outputPath+self.outputFolder+'/'+self.wind+'/'+str(time)+'.out')

    def change_gridloss(self, time):
        with fileinput.input(self.__servodyn, inplace=True, backup='.bak') as f:
            for line in f:                
                if "TPitManS" in line:                    
                    print(self._replace(line, "TPitManS", time+0.2), end="")
                elif "TimGenOf" in line:
                    print(self._replace(line, "TimGenOf", time), end="")
                else:
                    print(line, end="")

    def _replace(self, string, keyword, value):
        position = string.find(keyword)
        substring = string[:position]
        # replace float number (e.g. 12.34; 12.; .34)
        newtime = re.sub('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', str(value), substring)
        newline = newtime + string[position:]
        return newline


    def _fast(self, silence=False):            
        with cd('~/Eolien/FAST'):
            # command = 'fast {}{}{}.fst'.format(self._fstPath, self._prefix, self.wind)
            command = './{0} {1}{2}{3}{4}.fst'.format(self._fastName, self._fstPath,
                      self._prefix, self.wind, self._suffix)

            # command = 'ls && echo TEST'
            if silence:
                print("|- Running FAST in silence mode ...")
                subprocess.check_output([command], shell=True)
            else:
                print("|- Running FAST ...")
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
        self.__outputPath = os.path.expanduser(
                                     '~/Eolien/Parameters/Python/DLC2.3/Output/DLC2.3')
        self._fstPath = os.path.expanduser('~/Eolien/Parameters/Python/DLC2.3')
        self._prefix = '/DLC2.3_'
        self.__servodyn = os.path.expanduser(
                            '~/Eolien/Parameters/Python/DLC2.3/WT/ServoDyn_DLC2.3.dat')

        self._suffix = '_'+str(gridLoss)
        self.__fst_copy = ''
        self.__servodyn_copy = ''

        self.make_copy()
       

    def make_copy(self):
        # ServoDyn.dat
        filename = self.__servodyn
        with open(filename, 'r') as f:
            data = f.readlines()            
            for index, line in enumerate(data):
                if 'TPitManS' in line:
                    data[index] = self._replace(line, 'TPitManS', self.time+0.2)
                elif 'TimGenOf' in line:
                    data[index] = self._replace(line, 'TPitManS', self.time)
        
        filename = self.__servodyn.rstrip('.dat')
        filename = filename+'_'+str(self.time)+'.dat'
        with open(filename, 'w') as f:
            f.writelines(data)
        self.__servodyn_copy = filename # update .dat file

        # .fst
        filename = self._fstPath+self._prefix+self.wind+'.fst'
        with open(filename, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'ServoFile')
        
        filename = self._fstPath+self._prefix+self.wind+'_'+str(self.time)+'.fst'
        with open(filename, 'w') as f:
            f.write(data)
        self.__fst_copy = filename # update .fst file

    def run(self):
        self._fast()

    def _change_string(self, text, keyword, new=""):
        if keyword == 'ServoFile':
            old = "WT/ServoDyn_DLC2.3.dat"
            new = "WT/ServoDyn_DLC2.3_{}.dat".format(self.time)
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

#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    TIK = time.time()
    timerange = [110, 140.5, 30]

    # simu1 = DLC(wind='EOGR-2.0', gridLossTime=timerange, outputFolder='/withoutTRD')
    simu0 = DLC_para(wind='EOGR', gridLoss=130.5, outputFolder='/withoutTRD')
    simu0.run()    

    # processPool = Pool() # define number of worker (= numbers of processor by default)
    # processPool.map(simu0.run_multiprocess, timerange)
    # processPool.close()
    # processPool.join()

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")

    # simu2 = DLC(wind='EOGR', gridLossTime=timerange, outputFolder='/withoutTRD')
    # print("========== {} ==========".format(simu2.wind))
    # simu2.run(loop=True, silence=False)
    # TIK = time.time()
    # print("|- Total time :", TIK-TOK, "s")

    # simu3 = DLC(wind='EOGR+2.0', gridLossTime=timerange, outputFolder='/withoutTRD')
    # print("========== {} ==========".format(simu3.wind))
    # simu3.run(loop=True, silence=True)
    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")

    # simu4 = DLC(wind='EOGO', gridLossTime=timerange, outputFolder='/withoutTRD')
    # print("========== {} ==========".format(simu4.wind))
    # simu4.run(loop=True, silence=True)
    # TIK = time.time()
    # print("|- Total time :", TIK-TOK, "s")



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
