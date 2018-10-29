#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - Analayse de fatigue
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 29/10/2018
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
from tools import utils
from pyturbsim import turb
from pylife import meca, life
#============================== Modules Communs ==============================
import json
import time
import math
import collections
# import fileinput # iterate over lines from multiple input files
# import shutil # high-level file operations
# import subprocess # call a bash command e.g. 'ls'
# import multiprocessing # enable multiprocessing
# from contextlib import contextmanager # utilities for with-statement contexts
from matplotlib import pyplot as plt



#-----------------------------------------------------------------------------------------
#                                    CLASS DEFINITION
#-----------------------------------------------------------------------------------------
class Life(object):
    """
    Calculate lifetime cumulative damage
    *ATTRIBUTES*
    """
    def __init__(self, seeds, speed_range=None, distribution=None):
        # self.filenameInput = file
        self.seeds = seeds
        self.listOfSpeed = speed_range
        self.numberOfSpeed = len(speed_range)
        self.distribution = distribution # probability distribution
        # internal attributes
        self.propability = [] # probability for each mean wind speed
        self.allDamages = collections.OrderedDict()
        
        self.lifetime = 20 * 365*24*6 # designed lifetime of tower (per 10min)
        self.life = collections.OrderedDict()

        self.run()

    def run(self):
        print("Fatigue Lifge Assessment v0.0 (June 8 2018)")
        print("|- Loading data ...")
        self.load()
        # print("|- Calculating fatigue life with "+self.distribution+" distribution ...")
        # self.assess()
        print("|- Evaluating fatigue life with {} distribution ...".format(self.distribution))
        self.evaluate()
        # print("|- Sorting data ...")
        # self.sort()


    def assess(self, info=False):
        if self.distribution == 'Uniform':
            self.Uniform()
        elif self.distribution == 'Weibull':
            self.Weibull()
        else:
            print("|- [Error] The distribution law is not supported !")
            exit()

        for key, value in self.life.items():
            self.life[key] = collections.OrderedDict()
            self.life[key] = {'D_i':[], 'Dlife_i':[], 'Dlife':0.0}

            for i in self.listOfSpeed:
                D_i = self.allDamages[i][key]['Dtotal'] 
                index = self.listOfSpeed.index(i)
                propa = self.propability[index]
                Dlife_i = D_i * propa * self.lifetime

                self.life[key]['D_i'].append(D_i)
                self.life[key]['Dlife_i'].append(Dlife_i)

            self.life[key]['Dlife'] = sum(self.life[key]['Dlife_i'])
            if info: print(" - Total damage for " + key + "during lifetime is " + \
                           str(self.life[key]['Dlife']))

    def evaluate(self):
        if self.distribution == 'Uniform':
            self.Uniform()
        elif self.distribution == 'Weibull':
            self.Weibull()
        else:
            raise Exception("|- [ERROR] The distribution law is not supported !")
        

        for (index, speed) in enumerate(self.listOfSpeed):
            propa = self.propability[index]
            for file in self.allDamages[str(speed)]:
                for value in file.values():
                    value['Dlife'] = value['Dtotal'] * propa * self.lifetime

    def Uniform(self):
        self.propability = [1/float(self.numberOfSpeed)] * self.numberOfSpeed

    def Weibull(self, k=2, lamb=13.0):
        for speed in self.listOfSpeed:
            propability = (k/lamb) * (speed/lamb)**(k-1) * math.exp(-(speed/lamb)**k)
            self.propability.append(propability)
    
    def sort(self, damageDisplay=3):
        sortedList = sorted(self.life.items(), key=lambda x:x[1]['Dlife'], reverse=True)
        self.life = collections.OrderedDict()

        print(" - Top "+str(damageDisplay)+" dangerous spots:")
        i = 1
        for elem in sortedList:
            self.life[elem[0]] = elem[1]

            if elem[1]['Dlife'] >= 1:
                print(" - "+elem[0]+" : "+str(elem[1]['Dlife']))
            elif i <= damageDisplay:
                print(" - "+elem[0]+" : "+str(elem[1]['Dlife']))
                i = i + 1

    def plotALL(self):
        # fig, ax = plt.subplots()
        plt.subplot(2,1,1)
        X = collections.deque()
        Y = collections.deque()
        for speed in self.listOfSpeed:
            X.extend([speed]*100*9*12)
            for file in self.allDamages[str(speed)]:
                for value in file.values():
                    Y.append(value['Dlife'])

        plt.plot(X, Y, '.')
        plt.title('Fatigue assessment during lifetime (20 yeas)')
        plt.grid()
        plt.xticks(range(3,27,2))
        plt.ylabel("Cumulative damage")

        # ================
        X = self.listOfSpeed
        Y = [100*i for i in self.propability]
        
        plt.subplot(2,1,2)
        plt.title("Probability of wind speed occurence")
        plt.plot(X, Y, 'go-')
        plt.xlabel("Wind speed (m/s)")
        plt.xticks(X)
        plt.ylabel("Probability (%) ")
        plt.grid()

        plt.show()

    def plotDlife(self, listOfSpot):
        for spot in listOfSpot:            
            # X = range(self.numberOfSpeed)
            # X = [i*self.lifetime for i in X]
            # print X
            # exit()
            X = self.listOfSpeed
            Y = self.life[spot]['Dlife_i']

            plt.figure()

            plt.subplot(2,1,1)
            plt.title("Fatigue life at each wind speed")
            plt.plot(X, Y,'o-')
            # plt.xlabel("Wind speed (m/s)")
            plt.xticks(X)
            plt.ylabel("Cumulative damage")
            plt.grid()

            # ================
            X = self.listOfSpeed
            Y = [100*i for i in self.propability]
            
            plt.subplot(2,1,2)
            plt.title("Probability of wind speed occurence")
            plt.plot(X, Y, 'go-')
            plt.xlabel("Wind speed (m/s)")
            plt.xticks(X)
            plt.ylabel("Probability (%) ")
            plt.grid()

            plt.suptitle('Fatigue assessment during lifetime for '+spot)
        
        plt.show()

    def load(self):
        for v in self.listOfSpeed:
            self.allDamages[str(v)] = collections.deque()
        # read data
        for s in self.seeds:
            with open('{}_{}mps_{}.dam'.format(s[0], s[1], s[2]),'r') as f:
                self.allDamages[s[1]].append(json.loads(f.read()))
        print("|- {} files of wind speed have been loaded !".format(len(self.seeds)))



#-----------------------------------------------------------------------------------------
#                                  FUNCTION DEFINITION
#-----------------------------------------------------------------------------------------

    

#-----------------------------------------------------------------------------------------
#                                     MAIN FUNCTION
#-----------------------------------------------------------------------------------------
@utils.timer
def main():
    # Load seeds
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind'):
        with open('100seeds.json', 'r') as f:
            seeds = json.loads(f.read())

    liste = []
    [liste.append(s) for s in seeds if s[0] == "NTM"]
    seeds = liste

    temp = Life(seeds, range(3,27,2), 'Uniform')
    temp.plotALL()


    # ----- Running on multi processor
    # pool = multiprocessing.Pool() # define number of worker (= numbers of processor by default)
    # # [pool.apply_async(runTurbSimFAST_multiprocess, args=(wind, t)) for t in timerange] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    # pool.map(runFAST_multiprocess, seeds)
    # pool.close() # close: call .close only when never going to submit more work to the Pool instance
    # pool.join() # join: wait for the worker processes to terminate


    # ----- Running on single processor
    # simu2 = DLC1_1.DLC(seed=seeds[0])
    # simu2.run(silence=False)


    #* POST-PROCESSING
    # runStress_multiprocess(seeds)
    # runFatigue_multiprocess(seeds)



#-----------------------------------------------------------------------------------------
#                                      RUNNING TEST
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
