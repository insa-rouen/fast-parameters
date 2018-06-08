#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FATIGUE LIFE ASSESSMENT
# Calculate the fatigue life of wind turbin tower with a distribution of wind speed.
# 
#
#
# Authors: Hao BAI
# Date: 07/06/2018
#
# Version:
#   - 0.0:
#
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
import fatigue
#============================== Modules Communs ==============================
import pickle, time, math
from matplotlib import pyplot as plt

#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class life(object):
    """
    Calculate lifetime cumulative damage
    *ATTRIBUTES*
        
    """
    def __init__(self, needForSpeed=None, distribution=None):
        # self.filenameInput = file
        self.listOfSpeed = needForSpeed
        self.numberOfSpeed = len(needForSpeed)
        self.dlc = 'DLC1.2_NTM_'
        self.distribution = distribution
        self.propability = []
        self.damage = {}
        
        self.lifetime = 20 * 365*24*6 # designed lifetime of tower (per 10min)
        self.life = {}

        self.run()

    def run(self):
        print("Fatigue Lifge Assessment v0.0 (June 8 2018)")
        print("|- Loading data ...")
        self.load()
        print("|- Calculating fatigue life with "+self.distribution+" distribution ...")
        self.assess()


    def assess(self):
        if self.distribution == 'isoprobability':
            self.isoprobability()
        elif self.distribution == 'weibull':
            self.weibull()
        else:
            print("|- [Error] The distribution law is not supported !")
            exit()

        for key, value in self.life.items():
            self.life[key] = {'D_i':[], 'Dlife_i':[], 'Dlife':0.0}

            for i in self.listOfSpeed:
                
                D_i = self.damage[i][key]['Dtotal'] 
                index = self.listOfSpeed.index(i)
                propa = self.propability[index]
                Dlife_i = D_i * propa * self.lifetime

                self.life[key]['D_i'].append(D_i)
                self.life[key]['Dlife_i'].append(Dlife_i)

            self.life[key]['Dlife'] = sum(self.life[key]['Dlife_i'])
            print(" - Total damage for " + key + "during lifetime is " + \
                  str(self.life[key]['Dlife']))

    def isoprobability(self):
        self.propability = [1/float(self.numberOfSpeed)] * self.numberOfSpeed
 

    def weibull(self, k=2, lamb=13.0):
        # speedTry = [i/10. for i in range(251)]
        # print speedTry

        for speed in self.listOfSpeed:
            propability = (k/lamb) * (speed/lamb)**(k-1) * math.exp(-(speed/lamb)**k)
            self.propability.append(propability)

        # plt.plot(speedTry, self.propability)
        # plt.show()
        # exit()
    
    def plotDlife(self, listOfSpot):
        from matplotlib import pyplot as plt

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
            plt.plot(X, Y)
            # plt.xlabel("Wind speed (m/s)")
            plt.ylabel("Cumulative damage")

            # ================
            X = self.listOfSpeed
            Y = [100*i for i in self.propability]
            
            plt.subplot(2,1,2)
            plt.title("Probability of wind speed occurence")
            plt.plot(X, Y)
            plt.xlabel("Wind speed (m/s)")
            plt.ylabel("Probability (%) ")

            plt.suptitle('Fatigue assessment during lifetime for '+spot)
        
        plt.show()

    def load(self, filename=None):
        for i in self.listOfSpeed:
            filename = self.dlc + str(i) + "mps.damage"
            with open(filename,'rb') as f:
                self.damage[i] = pickle.load(f)
            print(" - "+filename)

        self.life = dict.fromkeys(self.damage[i].keys())
        print("|- [OK] "+str(self.numberOfSpeed)+" files of wind speed have been loaded !")
    

def main():
    TIK = time.time()
    
    # myLife = life(range(3,27,2), 'isoprobability')
    myLife = life(range(3,27,2), 'weibull')
    # print myLife.damage.keys()
    # myLife.plotDlife(['TwHt1@0   ', 'TwHt1@90  ', 'TwHt1@180 ', 'TwHt1@270 '])
    myLife.plotDlife(['TwHt1@0   '])

    TOK = time.time()
    print "Total Time(s) : ",TOK-TIK


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
