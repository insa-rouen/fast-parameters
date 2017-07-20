# A little script to generate RandSeed1 for TurbSim input file
# Created by: Hao BAI
# Date: 20/07/2017

import random
while True:
    pass
    caseName = raw_input("Enter the DLC filename: ")
    seed = random.randint(-2147483648, 2147483647)
    print "The random seed is: "+str(seed)

    with open('usedRandSeed', 'a+') as f:
        f.write(str(seed)+" : "+caseName+"\n")

    flag = raw_input("Exit ? (y/n): ")
    if flag == "y" or flag == "Y":
        break