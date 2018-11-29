#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Optimization: TRD mode 1 parameters
# 
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
#
# Comments:
#     - 0.0: [20/11/2018] Initial version
#
# Description:
#     
# 
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                   MODULES
#!------------------------------------------------------------------------------
#*         ==================== Modules Personnels ====================
from pyfast import DLC
from tools import utils
from pycrunch import amplitude as amp
#*           ==================== Modules Communs ====================
import sys
import numpy as np
from pyOpt import Optimization
from pyOpt import ALPSO

try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
except:
    raise ImportError('mpi4py is required for parallelization')



#!------------------------------------------------------------------------------
#!                               CLASS DEFINITION
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                             FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def run_TRD(mode1, gridloss, case='DLC2.3', outputFolder='', silence=False,
            echo=False):
    temp = DLC.TRD(mode1=mode1,gridloss=gridloss,case=case,outputFolder=outputFolder, 
               echo=echo)
    # set path
    temp.workPath = "~/Eolien/Parameters/Python/Optimization"
    temp.outputPath = "~/Eolien/Parameters/Python/Optimization/Output"
    temp.windPath = "~/Eolien/Parameters/Python/Optimization/Wind"
    temp.wtPath = "~/Eolien/Parameters/Python/Optimization/WT"
    temp.logPath = "~/Eolien/Parameters/Python/Optimization/log"
    # run calculation
    temp.run(silence)
    return temp.outputFilename

def get_peak_valley(filename):
    # Reference data
    # ref_time = (75.20, 77.33, 78.94, 80.48, 82.04, 83.56, 85.1, 86.64, 88.17,
    #              89.7) # time that occurs extremum deflection
    ref_index = (1520, 1733, 1894, 2048, 2204, 2356, 2510, 2664, 2817, 2970) # index of time in list of time
    # ref_deflX = (0.5529, -0.8429, 0.495, -0.6029, 0.5595, -0.5398, 0.5607, -0.5233, 0.5454, -0.5063) # extremum deflection
    
    # get peak and valley
    data = utils.readcsv(filename='./Output/'+filename, header=7, datarow=6009)
    deflX = data.get("YawBrTDxt")["Records"]
    trd_deflX = [deflX[i] for i in ref_index]
    # norme des amplitutes: valeurs à minimiser
    norme = np.linalg.norm(trd_deflX)
    return norme

def optiObj(optiVar):
    """ Optimization problem: objective function
    """
    # update objective function
    file = run_TRD(mode1=optiVar, gridloss=['EOG', 'O'], outputFolder='',
                   silence=1, echo=0)
    f = get_peak_valley(file)
    g = []
    fail = 0
    print("[{}] Optimal variables: {}, Objectif function value: {}".format(myrank, optiVar, f))
    sys.stdout.flush()
    return f, g, fail

def optiInequalConstraint(parameter_list):
    """ Optimization problem: inequality constraints
    """
    pass

def optiEqualConstraint(parameter_list):
    """ Optimization problem: equality constraints
    """
    pass

def optiProblem():
    optiProb = Optimization('OptiTour',optiObj) # def problem
    
    # add groups of var
    optiProb.addVarGroup('K',2,type='c',value=250., lower=0., upper=500.)
    optiProb.addVarGroup('L',2,type='c',value=-250., lower=-500., upper=0.)
    
    # add name of objectif function
    optiProb.addObj('f')

    # configuration of ALPSO
    optiDriv=ALPSO(pll_type='SPM')
    optiDriv.setOption('dynInnerIter',1)
    optiDriv.setOption('maxInnerIter',10)
    optiDriv.setOption('maxOuterIter',200)
    optiDriv.setOption('fileout',3) # summary+print
    optiDriv.setOption('dtol',0.001)

    # rerun
    optiDriv(optiProb, store_hst=True)
    # parallize calculation
    if myrank==0 :
        fsol = open('ALPSO_solution.txt', 'w')
        fsol.write(str(optiProb.solution(0)))
#        fsol.write(optProb.solution(1))
        fsol.close()


#!------------------------------------------------------------------------------
#!                                MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    file = run_TRD(mode1=[277.8, 26.7, -86.712, -17.0222], gridloss=['EOG', 'O'],
                   outputFolder='', silence=1, echo=1)
    get_peak_valley(file)

    # optiProblem()


#!------------------------------------------------------------------------------
#!                                 DEBUG TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
