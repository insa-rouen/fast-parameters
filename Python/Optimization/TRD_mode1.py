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
#     - 0.1: [18/12/2019] Replace wind condition to uniform constant @ 25 m/s
# Description:
# An fatal error is found in DLC2.3 gust wind condition, NaN values may be
# found in .out file. See the bug report for more information:
# https://gitlab.insa-rouen.fr/lmn-eolien/fast-parameters/issues/2
# 
# An other error is found considering TRD under the unifor constant wind, see:
# https://gitlab.insa-rouen.fr/lmn-eolien/fast-parameters/issues/3
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                   MODULES
#!------------------------------------------------------------------------------
#*         ==================== Modules Personnels ====================
from pyopti import DLC
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
def run_TRD(mode1, gridloss, case="DLC2.3", outputFolder="", silence=False,
            echo=False):
    temp = DLC.TRD(mode1=mode1,gridloss=gridloss,case=case,
                   outputFolder=outputFolder, echo=echo)
    # set path
    temp.workPath = "~/Eolien/Parameters/Python/Optimization"
    temp.outputPath = "~/Eolien/Parameters/Python/Optimization/Output"
    temp.windPath = "~/Eolien/Parameters/Python/Optimization/Wind"
    temp.wtPath = "~/Eolien/Parameters/Python/Optimization/WT"
    temp.logPath = "~/Eolien/Parameters/Python/Optimization/log"
    temp.tmpPath = "~/Eolien/Parameters/Python/Optimization/tmp"
    # run calculation
    temp.run(silence)
    return temp.outputFilename

def get_peak_valley(filename):
    # Reference data
    # --- for DLC2.3@cut-out
    # ref_time = (75.20, 77.33, 78.94, 80.48, 82.04, 83.56, 85.1, 86.64, 88.17,
    #              89.7) # time that occurs extremum deflection
    # ref_deflX = (0.5529, -0.8429, 0.495, -0.6029, 0.5595, -0.5398, 0.5607, -0.5233, 0.5454, -0.5063) # extremum deflection
    # ref_index = (1520, 1733, 1894, 2048, 2204, 2356, 2510, 2664, 2817, 2970) # index of time in list of time
    # --- for DLC0.1@25m/s
    # ref_time = (75.09, 77.36, 79.02, 80.54, 82.11, 83.61, 85.15, 86.69, 88.23,
    #     89.76,)
    ref_index = (1509, 1736, 1902, 2054, 2211, 2361, 2515, 2669, 2823, 2976)

    # get peak and valley
    data = utils.readcsv(filename="./Output/"+filename, header=7, datarow=6009,
                         echo=False)
    deflX = data.get("YawBrTDxt")["Records"]
    trd_deflX = [deflX[i] for i in ref_index]
    # norme des amplitutes: valeurs à minimiser
    # "Frobenius Norm" is equivalent to the vector's length
    result = np.linalg.norm(trd_deflX) 
    # result = np.sum(np.absolute(trd_deflX))
    return result

def get_amplitude(filename, N, echo):
    # with utils.cd("~/Eolien/Parameters/Python/Optimization"):
    filebase = "./Output/" + filename.replace(".out", "")
    amp.find_peak_valley(filebase, header=7, startline=12,
                        datarow=6009, channels=['YawBrTDxt', ], echo=echo)
    amplX = amp.Amplitude.calculate_p2p_amplitude(filebase+"_YawBrTDxt.ext",)
    trd_amplX = [value[-1] for value in amplX[:N]]
    result = np.linalg.norm(trd_amplX)
    return result



def optiObj(optiVar):
    """ Optimization problem: objective function
    """
    # update objective function
    try:
        file = run_TRD(mode1=optiVar, gridloss=['CST', '25.0mps'], 
            outputFolder='', silence=1, echo=0)
    except KeyboardInterrupt as e:
        raise e
    except:
        fail = 1
        print("[{}] ❌ Optimal variables: {}; FAST fails in calculation !".format(myrank, optiVar))
        f = None
    else:
        # f = get_peak_valley(file)
        f = get_amplitude(file, N=10, echo=False)
        if np.isnan(f):
            fail = 1
            print("[{}] ⚠️ Optimal variables: {}; Objectif function returns: {} !".format(
                myrank, optiVar, f))
        else:
            fail = 0
            print("[{}] ✅ Optimal variables: {}; Objectif function value: {}".format(myrank, optiVar, f))
    g = [] # constraints
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
    """ Optimization problem: gather all features
    """
    optiProb = Optimization('OptiTour',optiObj) # def problem
    # add groups of var
    optiProb.addVar('K1', type='c', value=446.60, lower=1., upper=600.)
    optiProb.addVar('K2', type='c', value=261.38,  lower=1., upper=270.)
    optiProb.addVar('L1', type='c', value=-181.81, lower=-220., upper=-1.)
    optiProb.addVar('L2', type='c', value=-99.76, lower=-1., upper=-220.)

    # add name of objectif function
    optiProb.addObj('f')
    # configuration of ALPSO
    optiDriv=ALPSO(pll_type='SPM')
    optiDriv.setOption('SwarmSize', 40) # default: 40
    optiDriv.setOption('dynInnerIter',1) # deafault: 0
    optiDriv.setOption('maxInnerIter',10) # default: 6
    optiDriv.setOption('maxOuterIter',100) # default: 200
    optiDriv.setOption('printOuterIters',5) # default: 0
    optiDriv.setOption('fileout',3) # summary+print
    optiDriv.setOption('dtol',0.001)
    # rerun
    optiDriv(optiProb, store_hst=True)
    # parallize calculation
    if myrank == 0 :
        fsol = open('ALPSO_solution.txt', 'w')
        fsol.write(str(optiProb.solution(0)))
#        fsol.write(optProb.solution(1))
        fsol.close()



#!------------------------------------------------------------------------------
#!                                MAIN FUNCTION
#!------------------------------------------------------------------------------
def main():
    runCode = 2

    if runCode == 1: # for testing
        file = run_TRD(mode1=[277.8, 26.7, -86.712, -17.0222],
                       gridloss=['EOG', 'O'], outputFolder='', silence=0, 
                       echo=1)
        
        # norme_value = get_peak_valley(file)
        norme_value = get_amplitude(file, N=10, echo=True)
        print(norme_value)

    if runCode == 2: # for optimization
        optiProblem()


#!------------------------------------------------------------------------------
#!                                 DEBUG TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
