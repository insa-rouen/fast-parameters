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
        if isinstance(spotNames[0], str):
            self.RFdata = count.counting(file, startline, spotNames)
            self.spotNames = self.RFdata.rainflowData.keys()
            self.damage = dict.fromkeys(self.spotNames)
        elif isinstance(spotNames[0], int):
            self.fatigueStress = count.finding(file, startline, spotNames)
            self.RFdata = count.counting(self.fatigueStress)
            self.spotNames = self.RFdata.rainflowData.keys()
            self.damage = dict.fromkeys(self.spotNames)
        else:
            print("[Error] Wrong spot index name or gage node nubmer !")
            exit()
        
        self.lifetime = 20*365*24*6 # Wind tower's designed lifetime per 10min
        self.run()

    def run(self):
        print("Fatigue anlaysis v0.0 (June 4 2018)")
        print("|- Analysising ...")
        self.assess()
        print("|- [OK] Analysis completed !")

    def assess(self):
        for spot in self.spotNames:
            self.damage[spot] = {'n':[], 'N':[], 'D':[], 'Dtotal':0.0, 'Dlife':0.0}
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

            self.damage[spot]['Dlife'] = self.damage[spot]['Dtotal'] * self.lifetime
            print spot, " : ", self.damage[spot]['Dtotal'], ", ", self.damage[spot]['Dlife']



def main():
    TIK = time.time()
    # analysis = fatigue('DLC1.2_NTM_25mps', startline=7, spotNames=['TwHt1@0   ', 'TwHt1@90  ', \
    #                    'TwHt1@180 ', 'TwHt1@270 ', 'TwHt9@0   ', 'TwHt9@90  ', 'TwHt9@180 ', 'TwHt9@270 '])
    analysis = fatigue('DLC1.2_NTM_25mps', 7, [1,5,9])
    TOK = time.time()
    print "Total Time(s) : ",TOK-TIK


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
