#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate RandSeed1 for TurbSim input file
#
# Authors: Hao BAI
# Date: 20/07/2017
#
# Comments:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import random
import json


#-----------------------------------------------------------------------------------------
#                                          FONCTIONS
#-----------------------------------------------------------------------------------------
def manual():
    while True:
        caseName = raw_input("Enter the DLC filename: ")
        seed = random.randint(-2147483648, 2147483647)
        print("The random seed is: "+str(seed))

        with open('usedRandSeed', 'a+') as f:
            f.write(str(seed)+" : "+caseName+"\n")

        flag = raw_input("Exit ? (y/n): ")
        if flag == "y" or flag == "Y":
            break

def auto(numberOfSeeds):
    data = []
    temp = []
    for key in ('NTM', 'ETM'):
        for v in range(3, 27, 2):
            for i in range(numberOfSeeds):
                while True:
                    seed = random.randint(-2147483648, 2147483647)
                    if seed in temp:
                        print("[ALERT] Random number repeat !")
                    else:
                        break
                temp.append(seed)
                data.append((key, str(v), str(seed)))

    # print(data)
    encode = json.dumps(data, indent=4)
    with open(str(numberOfSeeds)+'seeds.json','w') as f:
        f.write(encode)


#-----------------------------------------------------------------------------------------
#                                     PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
def main():
    auto()


#-----------------------------------------------------------------------------------------
#                                          EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()