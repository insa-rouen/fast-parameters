#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: CONSTITUER LA MATRICE DE RAINFLOW
# 
# 
#
#
# Authors: Hao BAI
# Date: 01/06/2018
#
# Version:
#   - 0.0: 
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import csv, rainflow
import numpy as np

#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class counting(object):
    """
    I/O FAST result file .out
    
    *ATTRIBUTES*
        filename : the filename of stress history file
        startline : the number of the row which has the channel titles
    """
    def __init__(self, file, startline, spotOutput, binsNumber):
        self.filenameInput = str(file+'.outStress')
        self.filenameOutput = ''
        self.fieldnamesInput = []
        self.fieldnamesOutput = []
        self.startline = startline
        self.spotOutput = spotOutput
        self.binsNumber = binsNumber

        self.datareader = None
        self.dataInput = {}
        self.rainflowData = {}
        self.ranges = {}
        self.means = {}
        self.bins = {}
        self.binnedData = {}

        self.run()

    def run(self):
        print "Rainflow counting v0.0 (June 2 2018)"
        # self.__geometry()
        print "|- Importing "+self.filenameInput+" ..."
        self.open()
        print "|- Counting Rainflow cycles ..."
        self.count()
        print "|- Binning Rainflow counts ..."
        self.bin()
        print "|- Saving data ..."
        # self.save()

    def open(self, filename=None):
        if filename is not None: self.filenameInput = filename

        with open(self.filenameInput, 'rb') as f:
            [next(f) for i in range(self.startline-1)] # read the file from the title line                
            datareader = csv.DictReader(f, delimiter='\t')
            self.datareader = datareader

            next(datareader) # ignore the row with the unit
            for spotName in self.spotOutput:
                self.dataInput[spotName] = []
            self.dataInput['Time'] = []

            for row in datareader:
                self.fieldnamesInput = row.keys() # save the titles of the talbe
                
                self.dataInput['Time'].append( float(row['Time      ']) ) # time steps

                # save stress at this time slip for each spot
                for spotName in self.spotOutput:
                    self.dataInput[spotName].append(float(row[spotName]))

    # Rainflow counting
    def count(self):
        for spotName in self.spotOutput:
            self.rainflowData[spotName] = {'Cycle':[], 'Range':[], 'Mean':[]}
            for valley, peak, cycle in rainflow.extract_cycles(self.dataInput[spotName]):
                rangeValue = peak - valley
                meanValue = (peak+valley)/2
                self.rainflowData[spotName]['Cycle'].append(cycle)
                self.rainflowData[spotName]['Range'].append(rangeValue)
                self.rainflowData[spotName]['Mean'].append(meanValue)

    # Binning stress ranges
    def bin(self):
        for spotName in self.spotOutput:
            data = self.rainflowData[spotName]

            # Calculate range bins bounds
            mini = min(data['Range'])
            maxi = max(data['Range'])
            unitRange = (maxi - mini)/self.binsNumber

            startRange = mini
            temp = [startRange]
            for i in range(self.binsNumber):
                if i == self.binsNumber-1:
                    endRange = maxi
                else:
                    endRange = startRange + unitRange
                temp.append(endRange)
                startRange = endRange
            self.ranges[spotName] = temp
            print self.ranges[spotName]
            exit()

            mini = min(data['Mean'])
            maxi = max(data['Mean'])
            unitMean = (maxi - mini)/self.binsNumber
            self.means[spotName] = {'Mini':mini, 'Maxi':maxi, 'unitMean':unitMean}

            
            self.bins[spotName] = {}
            

                # Calculate mean bins bounds
            startMean = self.means[spotName]['Mean']['Mini']
            for j in range(self.binsNumber):
                if j == self.binsNumber-1:
                    endMean = self.means[spotName]['Mean']['Maxi']
                else:
                    endMean = startMean + self.means[spotName]['Mean']['unitMean']
                # 
                length = len(data['Range'])
                for k in range(length):
                    if startRange <= data['Range'][k] < endRange:
                        pass
                self.bins[spotName][i] = {'Start':start,'End':end,'Cycles':0.}

                startMean = endMean
            startRange = endRange

            # Binning Rainflow cycles
            residue = []
            for i in range(self.binsNumber):
                if i == self.binsNumber-1:
                    self.bins[spotName][i]['Cycles'] = len(data)
                else:
                    lowerBound = self.bins[spotName][i]['Start']
                    upperBound = self.bins[spotName][i]['End']
                    cycles = 0
                    length = len(data)
                    for j in range(length):
                        if lowerBound <= data[j] < upperBound:
                            cycles = cycles + 1
                        else:
                            residue.append(data[j])
                    self.bins[spotName][i]['Cycles'] = cycles
                    data = residue

    # Showing result table in screen
    def show(self):
        for spotName in self.spotOutput:
            print('========== '+spotName+' ==========')

            print(' ')





def main():
    myCount = counting('test', startline=7, spotOutput=['TwHt1@0   ', 'TwHt1@10  ', \
                    'TwHt1@20  '], binsNumber=10)
    print('|- OK')


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
