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
    def __init__(self, seed, case='DLC1.1', outputFolder='/', toLog=False):
        self.seed =  seed
        self.case = case
        self.outputFolder = outputFolder
        self.toLog = toLog
        # Get OS platform name
        self._system = {'Linux':'FAST_glin64', 'Darwin':'fast.sh'}
        self._fastName = self._system.get(platform.system())
        # some fixed path
        self.outputPath = os.path.expanduser(
                            '~/Eolien/Parameters/Python/{0}/Output/{0}'.format(self.case))
        self.inputPath = os.path.expanduser('~/Eolien/Parameters/Python/{}'.format(
                                                                               self.case))
        self.prefix = '/{}_'.format(self.case)
        # self.servodyn = ''

        self.inflowFile = '{}{}_{}mps.IW.dat'.format(self.prefix, self.seed[0],
                                                     self.seed[1])
        self.fastFile = '{}{}_{}mps.fst'.format(self.prefix, self.seed[0], self.seed[1])

    def run(self, silence=False, ignore=False):
        print("|- Calculating {} at {} m/s with seed ID {} ...".format(self.seed[0],
                                                              self.seed[1], self.seed[2]))
        self.change_wind_profil()
        self._fast(silence, ignore)
        self.move()

    def move(self):
        ''' Move FAST output file (.out) to output folder
        '''
        source = self.inputPath+'{}{}_{}mps_{}.out'.format(self.prefix, self.seed[0],
                                                           self.seed[1], self.seed[2])
        destination = self.outputPath+self.outputFolder+'{}_{}mps_{}.out'.format(
                                                 self.seed[0], self.seed[1], self.seed[2])
        shutil.move(source, destination)

    def change_wind_profil(self):
        # InflowWind input script --------------------------------------------------------
        with open(self.inputPath+self.inflowFile, 'r') as f:
            data = f.read()
            data = self._change_string(data, 'Filename')

        filename = '{}{}_{}mps_{}.IW.dat'.format(self.prefix, self.seed[0], self.seed[1], 
                                                 self.seed[2])
        with open(self.inputPath+filename, 'w') as f:
            f.write(data)
        self.inflowFile = filename # update Inflow .dat file

        # FAST input script --------------------------------------------------------------
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
            old = "{}/{}_{}mps.bts".format(self.case, self.seed[0], self.seed[1])
            new = "{}/{}_{}mps_{}.bts".format(self.case, self.seed[0], self.seed[1],
                                              self.seed[2])
            text = re.sub(old, new ,text)

        if keyword == 'InflowFile':
            old = "{}_{}_{}mps.IW.dat".format(self.case, self.seed[0], self.seed[1])
            new = "{}_{}_{}mps_{}.IW.dat".format(self.case, self.seed[0], self.seed[1],
                                                 self.seed[2])
            text = re.sub(old, new ,text)
        return text

    def _fast(self, silence=False, ignore=False):
        ''' Call FAST program
        '''
        with utils.cd('~/Eolien/FAST'):
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
        # if an error occurs during execution, write output message to file
        if ignore and debug:
            directory = self.inputPath + '/log'
            if not os.path.exists(directory): # create new folder if non-exist
                os.makedirs(directory)
            with open(directory+'/'+self.seed[2]+'.bug', 'wb') as f:
                f.write(errorMessage)
            print("|- [ERROR] FAST has an error for simulation {},".format(self.seed),
                  "please see report in {}".format(directory))



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
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('6seeds.json', 'r') as f:
            seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "NTM"]
    seeds = liste[:1]

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
    simu2 = DLC(seed=seeds[0])
    simu2.run(silence=False, ignore=True)


#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
