#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FATIGUE ANALYSIS
# Cumulative damage with Miner's Rule
# 
#
#
# Authors: Hao BAI
# Date: 04/06/2018
#
# Version:
#   - 0.0: combine Rainflow counting with S-N curves
#
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
import count, sn
#============================== Modules Communs ==============================
import time


#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class fatigue(object):
    """
    Calculate cumulative damage
    *ATTRIBUTES*
        
    """
    def __init__(self, file, startline, spotNames):
        self.spotNames = spotNames
        self.RFdata = count.counting(file, startline, self.spotNames)
        self.damage = dict.fromkeys(self.spotNames)

    def assess(self):
        for spot in self.spotNames:
            self.damage[spot] = {'n':[], 'N':[], 'D':[], 'Dtotal':0.0}
            self.damage[spot]['n'] = self.RFdata.rainflowData[spot]['Cycle']
            ranges = self.RFdata.rainflowData[spot]['Range']
            means = self.RFdata.rainflowData[spot]['Mean']
            length = len(ranges)

            for i in range(length):
                n = self.damage[spot]['n'][i]
                curve = sn.dnvgl('B1', Goodman=(True, means[i]))
                N = curve.sn(ranges[i])
                self.damage[spot]['N'].append(N)
                D = n/N
                self.damage[spot]['D'].append(D)
                self.damage[spot]['Dtotal'] = self.damage[spot]['Dtotal'] + D

            print spot
            print self.damage[spot]['Dtotal']


def main():
    TIK = time.time()
    analysis = fatigue('test', startline=7, spotNames=['TwHt1@0   ', 'TwHt1@10  ', \
                       'TwHt1@20  '])
    analysis.assess()
    TOK = time.time()
    print "Time(s) : ",TOK-TIK


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
