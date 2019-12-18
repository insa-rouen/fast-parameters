#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate RandSeed1 for TurbSim input file
#
# Authors: Hao BAI
# Date: 20/07/2017
#
# Comments:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-------------------------------------------------------------------------------
# ============================ Modules Personnels =============================
from pywind import seed
from tools import utils
# ============================== Modules Communs ==============================



#-------------------------------------------------------------------------------
#                                          FONCTIONS
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
#                                     PROGRAMME PRINCIPALE
#-------------------------------------------------------------------------------
def main():
    # seed.auto(1000, speedRange=range(3, 27, 2), allowDuplicate=False) # give the number of seeds per speed
    # seed.auto(10000, speedRange=range(3, 27, 2), allowDuplicate=False) # give the number of seeds per speed
    seed.auto(10000, speedRange=range(4, 26, 2), keys=("NTM",), 
        allowDuplicate=False, reuseSeed=False)

    # seed.auto(100, speedRange=utils.frange(3.0, 25.1, 0.1))
    # seed.auto(10, speedRange=utils.frange(3.0, 25.1, 0.1), allowDuplicate=True,
    #     reuseSeed=True)
    # seed.auto(1000, speedRange=utils.frange(3.0, 25.1, 1.0), 
        # allowDuplicate=False, reuseSeed=False)


#-------------------------------------------------------------------------------
#                                          EXÉCUTION
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
