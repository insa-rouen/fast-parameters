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
from pyOpt import Optimization
from pyOpt import ALPSO
from mpi4py import MPI
comm = MPI.COMM_WORLD
myrank = comm.Get_rank()

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
    ref_deflX = (0.5529, -0.8429, 0.495, -0.6029, 0.5595, -0.5398, 0.5607, -0.5233, 0.5454, -0.5063) # extremum deflection
    
    # get peak and valley
    data = utils.readcsv(filename='./Output/'+filename, header=7, datarow=6009)
    deflX = data.get("YawBrTDxt")["Records"]
    trd_deflX = [deflX[i] for i in ref_index]
    # calculate difference
    diff = sum([abs(x)-abs(y) for x, y in zip(trd_deflX, ref_deflX)])
    return diff

def optiObj(optiVar):
    """ Optimization problem: objective function
    """

    # update objective function
    file = run_TRD(mode1=optiVar, gridloss=['EOG', 'O'], outputFolder='',
                   silence=1, echo=0)
    f = get_peak_valley(file)
    return f, g, fail

def optiInequalConstraint(parameter_list):
    """ Optimization problem: inequality constraints
    """
    pass

def optiEqualConstraint(parameter_list):
    """ Optimization problem: equality constraints
    """
    pass
#!------------------------------------------------------------------------------
#!                                MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    # file = run_TRD(mode1=[277.8, 26.7, -86.712, -17.0222], gridloss=['EOG', 'O'],
    #                outputFolder='', silence=1, echo=1)
    # get_peak_valley("EOG_O_277.826.7-86.712-17.0222.out")

    optiProb = Optimization('OptiTRD', optiObj)


#!------------------------------------------------------------------------------
#!                                 DEBUG TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
