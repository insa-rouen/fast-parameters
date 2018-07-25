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
#     - 0.0: 
#
# Description:
# Combine wind condition EOG with loss of grid at different moment
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                        MODULES
#-----------------------------------------------------------------------------------------
#============================== Modules Communs ==============================
import os, re
import fileinput # iterate over lines from multiple input files
import subprocess # call a bash command e.g. 'ls'
from contextlib import contextmanager
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
    def __init__(self, wind='', gridLossTime=[], outputFolder='/', toLog=False):
        self.wind =  wind
        self.gridLossTime = {'start':gridLossTime[0], 'end':gridLossTime[1],
                             'step':gridLossTime[2]}
        self.outputFolder = outputFolder
        self.toLog = toLog
        # some fixed path
        self.__outputPath = os.path.expanduser(
                                     '~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC2.3')
        self.__fstPath = '../Parameters/NREL_5MW_Onshore/DLC2.3_'
        self.__servodyn = os.path.expanduser(
                            '~/Eolien/Parameters/NREL_5MW_Onshore/WT/ServoDyn_DLC2.3.dat')

    def run(self):
        with cd('~/Eolien/FAST/'):
            command = 'fast {}{}.fst'.format(self.__fstPath, self.wind)
            subprocess.call([os.getenv('SHELL'), '-i', '-c', command])

    def change_gridloss(self):
        time = 110.0
        # with open(self.__servodyn, 'r+') as f:
        with fileinput.input(self.__servodyn, inplace=True, backup='.bak') as f:
            for line in f:                
                if "TPitManS" in line:                    
                    print(self.__replace(line, "TPitManS", time+0.2), end="")
                elif "TimGenOf" in line:
                    print(self.__replace(line, "TimGenOf", time), end="")
                else:
                    print(line, end="")

    def __replace(self, string, keyword, value):
        position = string.find(keyword)
        substring = string[:position]
        newtime = re.sub('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', str(value), substring)
        newline = newtime + string[position:]
        return newline


                
#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    simu1 = DLC(wind='EOGR', gridLossTime=[110, 140.5, 10], outputFolder='/withoutTRD')
    # simu1.run()
    simu1.change_gridloss()


#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
