#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRD testing codes
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 24/10/2018
#
# Comments:
#     - 0.0: Mean wind speed fixed at cut-out and grid loss time fixed at 74.9s
#     
# Description:
#     - Combine wind condition EOG with loss of grid and induce Pitch-to-Feather 
#       and HSS brake shutdown
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                       MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
import sys, IPython # to colorize traceback errors in terminal
sys.excepthook = IPython.core.ultratb.ColorTB()
import DLC23
#*============================= Modules Communs ==============================
import time
import os
# import os, platform, 
import re
# import fileinput # iterate over lines from multiple input files
# import shutil # high-level file operations
# import subprocess # call a bash command e.g. 'ls'
# import multiprocessing # enable multiprocessing
# from contextlib import contextmanager # utilities for with-statement contexts



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------
class TRD(DLC23.DLC_para):
    """
    """
    def __init__(self, TRD_mode1, wind='', gridLoss=0.0, outputFolder='/', toLog=False):
        super(TRD, self).__init__(wind=wind, gridLoss=gridLoss, outputFolder=outputFolder, toLog=toLog)
        self.TRD_mode1 = TRD_mode1
        self.time = gridLoss
        # some fixed path
        self.__outputPath = os.path.expanduser(
                                        '~/Eolien/Parameters/Python/TRD/Output/DLC2.3')
        self._fstPath = os.path.expanduser('~/Eolien/Parameters/Python/TRD')
        self._prefix = '/DLC2.3_'
        self.__servodyn = os.path.expanduser(
                               '~/Eolien/Parameters/Python/TRD/WT/ServoDyn_DLC2.3.dat')
        self.__servodyn_trd = os.path.expanduser(
                               '~/Eolien/Parameters/Python/TRD/WT/ServoDyn_TRD.dat')
        self._suffix = '_'+str(gridLoss)
        self.__fst_copy = ''
        self.__servodyn_copy = ''

    def make_copy2(self):
        # ServoDyn_TRD.dat -----------------------------------------------------
        filename = self.__servodyn_trd
        with open(filename, 'r') as f:
            data = f.readlines()
            for index, line in enumerate(data):
                if 'TRD_K(1)' in line:
                    data[index] = self._replace(line, 'TRD_K(1)', self.TRD_mode1[0])
                if 'TRD_K(2)' in line:
                    data[index] = self._replace(line, 'TRD_K(2)', self.TRD_mode1[1])
                if 'TRD_L(1)' in line:
                    data[index] = self._replace(line, 'TRD_L(1)', self.TRD_mode1[2])
                if 'TRD_L(2)' in line:
                    data[index] = self._replace(line, 'TRD_L(2)', self.TRD_mode1[3])

        filename = self.__servodyn_trd.rstrip('.dat')
        filename = '{}_{}{}{}{}.dat'.format(filename, self.TRD_mode1[0], self.TRD_mode1[1], self.TRD_mode1[2], self.TRD_mode1[3])
        with open(filename, 'w') as f:
            f.writelines(data)
        self.__servodyn_trd = filename


        # ServoDyn.dat ---------------------------------------------------------
        filename = self.__servodyn
        with open(filename, 'r') as f:
            data = f.readlines()            
            for index, line in enumerate(data):
                if 'TPitManS' in line:
                    data[index] = self._replace(line, 'TPitManS', self.time+0.2)
                elif 'TimGenOf' in line:
                    data[index] = self._replace(line, 'TimGenOf', self.time)
                elif 'THSSBrDp' in line:
                    data[index] = self._replace(line, 'THSSBrDp', self.time+0.2+11.25)
                elif 'NTRDfile' in line:
                    data[index] = self._change_string(line, 'NTRDfile', self.__servodyn_trd)
        
        filename = self.__servodyn.rstrip('.dat')
        filename = filename+'_'+str(self.time)+'.dat'
        with open(filename, 'w') as f:
            f.writelines(data)
        self.__servodyn_copy = filename # update .dat file


        # .fst  ----------------------------------------------------------------
        filename = self._fstPath+self._prefix+self.wind+'.fst'
        with open(filename, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'ServoFile')
        
        filename = self._fstPath+self._prefix+self.wind+'_'+str(self.time)+'.fst'

        with open(filename, 'w') as f:
            f.write(data)
        self.__fst_copy = filename # update .fst file

    def run(self, silence=False):
        print("|- Calculating the case of", self.time, "...")
        self._fast(silence)

    def _change_string(self, text, keyword, new=""):
        if keyword == 'ServoFile':
            old = "WT/ServoDyn_DLC2.3.dat"
            new = "WT/ServoDyn_DLC2.3_{}.dat".format(self.time)
        if keyword == 'NTRDfile':
            old = "ServoDyn_TMD.dat"
        text = re.sub(old, new ,text)
        return text
    
    def _change_number(self, text, keyword, new):
        pass



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def run_multiprocess(wind, gridloss):
    simulation = TRD(wind=wind, gridLoss=gridloss, outputFolder='/withTRD/EOGO_74.9')
    simulation.make_copy2()
    simulation.run(True)
    simulation.move_and_rename(simulation.time)



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    # ----- Running on multi processor
    TIK = time.time()
    # timerange = frange(60, 90.5+0.01, 0.1)

    # wind = 'EOGO'
    # for wind in ['EOGR', 'EOGO', 'EOGR-2.0', 'EOGR+2.0']:
    #     print("========== {} ==========".format(wind))
    #     pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    #     [pool.apply_async(run_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    #     pool.close() # close: call .close only when never going to submit more work to the Pool instance
    #     pool.join() # join: wait for the worker processes to terminate

    # TOK = time.time()
    # print("|- Total time :", TOK-TIK, "s")


    # ----- Running on single processor
    # timerange = frange(110, 140.5+0.01, 30)

    simu2 = TRD(TRD_mode1=[290, 30, -90, -20], wind='EOGO', gridLoss=74.9, outputFolder='/withTRD/EOGO_74.9')
    simu2.make_copy2()
    print("========== {} ==========".format(simu2.wind))
    simu2.run(silence=False)

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")



#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
