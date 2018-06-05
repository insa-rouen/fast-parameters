#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: FIND FATIGUE STRESS AND RUN RAINFLOW COUNTING
# 
# 
#
#
# Authors: Hao BAI
# Date: 01/06/2018
#
# Version:
#   - 0.0: Enable Rainflow counting on serval stress histories
#   - 0.1: [04/06/2018] Find fatigue stress history from a huge amount of stress histories
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import csv, rainflow
import copy
import numpy as np

#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class finding(object):
    """docstring for  finding"""
    def __init__(self, file, startline, gageOutput):
        self.filenameInput = str(file+'.outStress')
        self.startline = startline
        self.gageOutput = gageOutput

        self.datareader = None
        self.dataInput = {}
        self.stressFilter = {}
        self.dataOutput = {}

        self.run()

    def run(self):
        print("Fatigue stress finder v0.0 (June 4 2018)")
        print("|- Importing "+self.filenameInput+" ...")
        self.open()
        print("|- Filtering stress histories ...")
        self.filter()
        print("|- [OK] Fatigue stress history found !")
        # print "|- Saving data ..."
        # self.save()
    
    def open(self, filename=None):
        if filename is not None: self.filenameInput = filename

        with open(self.filenameInput, 'rb') as f:
            [next(f) for i in range(self.startline-1)] # read the file from the title line                
            datareader = csv.DictReader(f, delimiter='\t')
            self.datareader = datareader
            self.fieldnamesInput = datareader.fieldnames # save the titles of the talbe

            for key in self.fieldnamesInput:
                self.dataInput[key] = []

            next(datareader) # ignore the row with the unit
            for row in datareader:
                for key in self.dataInput.keys():
                    self.dataInput[key].append( float(row[key]) )

    def filter(self):
        keys = self.fieldnamesInput
        keys.pop(0)
        
        # Count total occurrence of tension/compression on each spot
        for i in self.gageOutput:
            allN = []
            allKeys = []
            for key in keys:
                if i == int(key[4]):
                    self.stressFilter[key] = {'Ntension':0, 'Ncompression':0}
                    Ntension = 0
                    Ncompression = 0
                    for stress in self.dataInput[key]:
                        if stress >= 0.0:
                            Ntension = Ntension + 1
                        else:
                            Ncompression = Ncompression + 1
                    self.stressFilter[key]['Ntension'] = Ntension
                    self.stressFilter[key]['Ncompression'] = Ncompression
                    allN.append(Ntension)
                    allKeys.append(key)
                else:
                    pass

        # Extract only one fatigue stress for one tower gage node
            if allN != []:
                self.dataOutput[i] = {'index':None, 'fatigueStress':None}
                key_max = allKeys[allN.index(max(allN))]
                self.dataOutput[i]['index'] = key_max
                self.dataOutput[i]['N_stress'] = self.stressFilter[key_max]
                self.dataOutput[i]['fatigueStressHistory'] = self.dataInput[key_max]
            else:
                print("|- [ALERT] There is no data for gage node "+"TwHt"+str(i))

class counting(object):
    """
    I/O FAST result file .out
    
    *ATTRIBUTES*
        filename : the filename of stress history file
        startline : the number of the row which has the channel titles
    """
    def __init__(self, file, startline=None, spotNames=None):
        if isinstance(file, str): # read data from file
            self.filenameInput = str(file+'.outStress')
            self.filenameOutput = ''
            self.fieldnamesInput = []
            self.fieldnamesOutput = []
            self.startline = startline
            self.spotNames = spotNames
            self.dataInput = {}
            self.runFlag = 0 # read data from <class finding> instance
        elif isinstance(file, finding):
            self.spotNames = []
            self.dataInput = file.dataOutput
            self.runFlag = 1
        else:
            print("|- [Error] Wrong input filename or <class finding> instance !")
            exit()

        self.datareader = None
        self.rainflowData = {}
        self.ranges = {}
        self.means = {}
        self.bins = {}
        self.binnedData = {}

        self.run()

    def run(self):
        print("Rainflow counting v0.0 (June 2 2018)")
        if self.runFlag == 0:
            print("|- Importing "+self.filenameInput+" ...")
            self.open()
            print("|- Counting Rainflow cycles ...")
            self.count()
        elif self.runFlag == 1:
            print("|- Importing from <class finding> instance ...")
            self.adapt()
            print("|- Counting Rainflow cycles ...")
            self.count()
        # self.show()
        print "|- [OK] Rainflow count finished !"
        # self.save()

    # runFlag = 0: read data from file
    def open(self, filename=None):
        if filename is not None: self.filenameInput = filename

        with open(self.filenameInput, 'rb') as f:
            [next(f) for i in range(self.startline-1)] # read the file from the title line                
            datareader = csv.DictReader(f, delimiter='\t')
            self.datareader = datareader

            next(datareader) # ignore the row with the unit
            for spot in self.spotNames:
                self.dataInput[spot] = []
            self.dataInput['Time'] = []

            for row in datareader:
                self.fieldnamesInput = row.keys() # save the titles of the talbe
                
                self.dataInput['Time'].append( float(row['Time      ']) ) # time steps

                # save stress at this time slip for each spot
                for spot in self.spotNames:
                    self.dataInput[spot].append(float(row[spot]))

    # runFlag = 1: read data from <class finding> instance
    def adapt(self):
        temp = {}
        for elem in self.dataInput.items():
            key = elem[1]['index']
            self.spotNames.append( key )
            temp[key] = elem[1]['fatigueStressHistory']

        self.dataInput = temp
    # Rainflow counting
    def count(self):
        for spot in self.spotNames:
            self.rainflowData[spot] = {'Cycle':[], 'Range':[], 'Mean':[]}
            for valley, peak, cycle in rainflow.extract_cycles(self.dataInput[spot]):
                rangeValue = peak - valley
                meanValue = (peak+valley)/2
                self.rainflowData[spot]['Cycle'].append(cycle)
                self.rainflowData[spot]['Range'].append(rangeValue)
                self.rainflowData[spot]['Mean'].append(meanValue)

    # Showing result table in screen
    def show(self):
        for spot in self.spotNames:
            data = self.rainflowData[spot]
            length = len(data['Cycle'])
            print('========== '+spot+' ==========')
            print('Num. of Cycles','Stress Range (MPa)','Stess Mean (MPa)')
            for i in range(length):
                print(data['Cycle'][i], data['Range'][i], data['Mean'][i])
            print(' ')


def main():
    myFinding = finding('test', startline=7, gageOutput=[1,5,9])
    # myCount = counting('test', startline=7, spotNames=['TwHt1@0   ', 'TwHt1@10  ', \
    #                 'TwHt1@20  '])
    myCount2 = counting(myFinding)
    # myCount2.show()
    print('OK !!!')


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
