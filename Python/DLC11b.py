#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DLC1.1 - run 12*100 times simulation over all wind speed
#
# Authors: Hao BAI (hao.bai@insa-rouen.fr)
# Version: 0.0
# Date: 22/10/2018
#
# Comments:
#     - 0.0: Init version
#     - 0.1: Apply to distributed computers
#     - 0.2: Run 10 000 simulation at wind speed 25 m/s
#     - 0.3: Run 10 000 simulation at wind speed 23 m/s
#     - 0.4: [09/12/18] Run 10 000 simulations at wind speed 17 m/s
#     - 0.5: [15/12/18] Run 10 000 simulations at wind speed 13 m/s
#     - 0.6: [20/12/18] Run 10 000 simulations at wind speed 9 m/s
#     - 0.7: [23/12/18] Run 10 000 simulations at wind speed 5 m/s
#     - 0.8: [25/12/18] Run 10 000 simulations at wind speed 3 m/s
#     - 1.0: [25/04/19] Run 10 simulations for wind speed [3, 3.1, 3.2, ..., 25]
#     - 2.0: [27/09/20] Get statistical info of wind speeds
# Description:
# 
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                        MODULES
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from tools import utils, distribute, gmail
from pywind import turb
from pylife import meca, life
from pyfast import DLC
#* ============================= Modules Communs ==============================
import json
import time
import datetime
import platform
import multiprocessing
import os
from pathlib import Path
import numpy as np



#!------------------------------------------------------------------------------
#!                                   CLASS DEFINITION
#!------------------------------------------------------------------------------
CORES = int( os.cpu_count() )
PLATFORM = platform.node()



#!------------------------------------------------------------------------------
#!                                 FUNCTION DEFINITION
#!------------------------------------------------------------------------------
def runTurbSim_multiprocess(seeds, logpath='', silence=False, echo=True):
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/'):
        turb.get_turbulence_multiprocess(seeds, logpath=logpath,
                                         silence=silence, echo=echo)

def runFAST_multiprocess(seeds, silence=False, echo=True):
    DLC.get_DLC11_multiprocess(seeds, outputFolder='',silence=silence,echo=echo)

def runStress_multiprocess(seeds, thetaStep=30, echo=True):
    # generate file names
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    # run stress calculation
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        meca.get_stress_multiprocess(list_filebase, datarow=6009,
                                     gages=[1,2,3,4,5,6,7,8,9],
                                     thetaStep=thetaStep,
                                     saveToDisk=True, echo=echo)

def runFatigue_multiprocess(seeds, echo=True):
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_fatigue_multiprocess(list_filebase, gages=[1,2,3,4,5,6,7,8,9], lifetime=20*365*24*6, echo=echo)

def runStressFatigue_multiprocess(seeds, thetaStep, echo=True):
    ''' Run Stress and Fatigue in same time
    '''
    list_filebase = ['{}_{}mps_{}'.format(s[0], s[1], s[2]) for s in seeds]
    with utils.cd('~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/'):
        life.get_stress_fatigue_multiprocess(list_filebase, datarow=6009,
                                             gages=[1,2,3,4,5,6,7,8,9], thetaStep=thetaStep,
                                             lifetime=20*365*24*6,echo=echo)

def runALL(seed, thetaStep, outputFolder="", compress=False, silence=False,
           echo=True):
    try:
        logpath = "~/Eolien/Parameters/Python/DLC1.1/log"
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/"):
            turb.get_turbulence(seed, logpath, silence, echo) # generate TurbSim
        DLC.get_DLC11(seed, outputFolder, silence, echo) # run FAST
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/"):
            filebase = "{}_{}mps_{}".format(seed[0], seed[1], seed[2])
            life.get_stress_fatigue(filebase, datarow=6009,
                                    gages=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    thetaStep=thetaStep, lifetime=20*365*24*6,
                                    echo=echo) # calculate Stress and Fatigue
    except:
        raise
    else:
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/"):
            if compress:
                utils.compress(filename=filebase+".out", removeSource=True)
        return seed

def runALL_multiprocess(seeds, thetaStep, outputFolder="", compress=True,
                        silence=True, echo=False):
    print('All-In-One: TurbSim + FAST + Stress + Fatigue v0.1 (December 10 2018)')
    print('========== Multiprocessing Mode ==========')
    # prepare a callback function
    length = len(seeds)
    print('[INFO] {} tasks is submitted'.format(length))
    completed = []
    def printer(seed):
        pos = seeds.index(seed) + 1
        completed.append(seed)
        rest = length - len(completed)
        hour, minute = time.strftime("%H,%M").split(',')
        print('|- [{}/{}] {} at {} m/s with seed ID {} is finished at {}:{}. '
              '{} tasks waiting to be completed ...'.format(pos, length,seed[0],
              seed[1], seed[2], hour, minute, rest))
    # begin multiprocessing
    pool = multiprocessing.Pool(CORES)
    [pool.apply_async(runALL, args=(seed, thetaStep, outputFolder, compress,
     silence,  echo), callback=printer, error_callback=utils.handle_error) for
     seed in seeds]
    pool.close()
    pool.join()


def runTurbSim_FAST(seed, outputFolder="", compress=False, silence=False, 
    echo=True):
    try:
        logpath = "~/Eolien/Parameters/Python/DLC1.1/log"
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1/"):
            turb.get_turbulence(seed, logpath, silence,echo)  # generate TurbSim
        DLC.get_DLC11(seed, outputFolder, silence, echo)  # run FAST
    except:
        raise
    else:
        return seed


def runTurbSim_FAST_multiprocess(seeds, outputFolder="", compress=True, 
    sendmail=True, silence=True, echo=False):
    tik = time.time()
    print('Wind & FAST: TurbSim + FAST v0.1 (September 26 2020)')
    print('Run TurbSim and calculate statistical values of wind speed at HH')
    print('========== Multiprocessing Mode ==========')
    
    ## prepare a callback function
    length = len(seeds)
    print('[INFO] {} tasks is submitted'.format(length))
    completed = []
    def printer(seed):
        pos = seeds.index(seed) + 1
        completed.append(seed)
        rest = length - len(completed)
        hour, minute = time.strftime("%H,%M").split(',')
        print('|- [{}/{}] {} at {} m/s with seed ID {} is finished at {}:{}. '
            '{} tasks waiting to be completed ...'.format(pos, length, seed[0],
            seed[1], seed[2], hour, minute, rest))
    # begin multiprocessing
    pool = multiprocessing.Pool(CORES)
    [pool.apply_async(runTurbSim_FAST,
        args=(seed, outputFolder, compress, silence,  echo), 
        callback=printer, error_callback=utils.handle_error) 
        for seed in seeds]
    pool.close()
    pool.join()
    
    ## Post-process
    print("|- Post-processing ...")
    with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/"):
        # get .out files
        out_list = utils.find(path=".", pattern="{}_{}mps_*.out".format(
            seeds[0][0], seeds[0][1]))
        if len(out_list) != len(seeds):
            raise RuntimeError("The number of .out files ({}) doesn't match the"
                " number of seeds ({})".format(len(out_list), len(seeds)))
        # make subfolder
        output_dir = Path("lmn-cs_out@{}mps".format(seeds[0][1]))
        if not output_dir.exists():
            output_dir.mkdir()
        # move files
        for filebase in out_list:
            f = Path(filebase+".out")
            destination = output_dir.joinpath(f)
            f.replace(destination)
        # compress folder
        if compress == True:
            utils.compress(filebase=str(output_dir)+".out", source=output_dir,
                remove_source=False)
        # calculate statistical values
        output = {}
        for s in seeds:
            statistic = {}
            filename = output_dir.joinpath("{}_{}mps_{}.out".format(
                s[0], s[1], s[2]))
            data = utils.readcsv(filename=filename, datarow=6009,
                checkNaN=False, echo=echo)
            speedx = np.array(data.get("Wind1VelX")["Records"])
            speedy = np.array(data.get("Wind1VelY")["Records"])
            speedz = np.array(data.get("Wind1VelZ")["Records"])
            # speed in X direction
            statistic["X_mean"] = speedx.mean()
            statistic["X_std"] = speedx.std()
            statistic["X_25"] = np.percentile(speedx, 25)
            statistic["X_50"] = np.percentile(speedx, 50)
            statistic["X_75"] = np.percentile(speedx, 75)
            # speed in Y direction
            statistic["Y_mean"] = speedy.mean()
            statistic["Y_std"] = speedy.std()
            statistic["Y_25"] = np.percentile(speedy, 25)
            statistic["Y_50"] = np.percentile(speedy, 50)
            statistic["Y_75"] = np.percentile(speedy, 75)
            # speed in Z direction
            statistic["Z_mean"] = speedz.mean()
            statistic["Z_std"] = speedz.std()
            statistic["Z_25"] = np.percentile(speedz, 25)
            statistic["Z_50"] = np.percentile(speedz, 50)
            statistic["Z_75"] = np.percentile(speedz, 75)
            output[s[2]] = statistic
        attach = Path(output_dir.stem+".json").absolute()
        utils.save_json(output, attach, True)
    tok = time.time()
    duration = datetime.timedelta(seconds=round(tok-tik))

    ## send e-mail
    print("|- Sending notification to user ...", end="\n ")
    subject = "[{}] {} is terminated, elapsed time: {}".format(
        PLATFORM.split(".")[0], output_dir.stem, duration)
    data = {"name": "Hao",
            "address": ["hao.bai@insa-rouen.fr", ],
            "subject": subject,
            "message": "",
            "attachment": attach,
            "list_of_files": [attach.stem, ]
            }
    gmail.send(data=data, by="gmail", debug=0)


def check_seeds():
    DIR_HOME = Path("~/Eolien/Parameters/NREL_5MW_Onshore").expanduser()
    DIR11 = Path(
        "~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1/damages10000/lmn-cs"
        ).expanduser()
    # seeds file
    seeds_odd = utils.load_json(DIR_HOME.joinpath("Wind", "10000seeds.json"))
    seeds_even = utils.load_json(DIR_HOME.joinpath("Wind", "10000seeds2.json"))
    seeds = seeds_odd + seeds_even
    seeds = [s for s in seeds if s[0] == "NTM"]
    # dam file
    dam_list = utils.find(path=DIR11, pattern="*.dam")
    for v in np.arange(3.0, 26.0, 1.0):
        temp_seeds = [s for s in seeds if s[1] == str(v)]
        temp_dams = [d for d in dam_list if "NTM_{}mps".format(v) in d]
        print("Checking {} m/s for {} seeds and {} dams ...".format(
            v, len(temp_seeds), len(temp_dams)))
        for i, s in enumerate(temp_seeds):
            for dam in temp_dams:
                if "_"+s[-1] in dam:
                    try:
                        seeds.remove(s)
                        dam_list.remove(dam)
                    except:
                        print("Seed number:", s)
                        raise
                    break
        print("Remaining seeds: {}, dams: {}".format(len(seeds), len(dam_list)))
    print("Unfound seeds:", seeds)
    print("Unfound dam files:", dam_list)



#!------------------------------------------------------------------------------
#!                                    MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    # Load Seeds ===============================================================
    # Initiation
    seed_path = Path("~/aster1/Wind").expanduser()
    seed_path = Path("~/Eolien/Parameters/NREL_5MW_Onshore/Wind").expanduser()
    # seeds file
    seeds_odd = utils.load_json(seed_path.joinpath("10000seeds.json"))
    seeds_even = utils.load_json(seed_path.joinpath("10000seeds2.json"))
    seeds = seeds_odd + seeds_even
    seeds = [s for s in seeds if s[0] == "NTM" and s[1] == "3.0"]
    # liste = [s for s in seeds if s[0] == "NTM"]
    # seeds = liste

    # Re-run
    # with utils.cd('~/aster1/Wind'):
    #     with open('failedRunsFAST.json', 'r') as f:
    #         seeds1 = json.loads(f.read())
    #     with open('failedRunsStress.json', 'r') as f:
    #         seeds2 = json.loads(f.read())
        # with open('recomputeALL.json', 'r') as f:
        #     seeds3 = json.loads(f.read())
    #     with open('recomputeTurbSim.json', 'r') as f:
    #         seeds4 = json.loads(f.read())
    # ----- Rerun failed cases
    # seeds1.extend(seeds2)
    # seeds = seeds1
    # ----- Rerun recomputed cases
    # seeds = seeds3
    # seeds = seeds4
    # seeds = [['NTM', '3', '-544599383'], ['NTM', '5', '1571779345']]
    # seeds = [["NTM", "21", "-800757005"], ]
    # Some Tests ===============================================================
    # DLC.get_DLC11(['NTM', '4.0', '1879136045'], outputFolder='', silence=False, 
    #                echo=True)
    
    runTurbSim_FAST_multiprocess(seeds[:3], sendmail=1, silence=1, echo=1)
    # runTurbSim_multiprocess(seeds, silence=1, echo=1)
    # runFAST_multiprocess(seeds, silence=0, echo=1)
    # # runStress_multiprocess(seeds, echo=0)
    # # runFatigue_multiprocess(seeds, echo=0)
    # runStressFatigue_multiprocess(seeds, 10, echo=0)
    return
    

    # Initiate/Resume Tasks ====================================================
    # Distribute tasks ---------------------------------------------------------
    computers = distribute.LMN(
        windPath='~/Eolien/Parameters/NREL_5MW_Onshore/Wind/DLC1.1',
        outputPath='~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC1.1')
    computers.deactivate("PC-LMN-9020")  # Shubiao WANG
    computers.deactivate("PC-LMN-9020A")
    computers.deactivate("PC-LMN-7040") # 1TB
    # computers.setEqually(seeds)
    computers.setAutomatically(seeds)
    # computers.show()
    
    # TurbSim ------------------------------------------------------------------
    # computers.resume('TurbSim', outputFileSize=70*1024**2)
    computers.run(runTurbSim_multiprocess,
                  "~/Eolien/Parameters/Python/DLC1.1/log",
                  True, False)  # logpath="...", silence=True, echo=False

    # FAST ---------------------------------------------------------------------
    computers.run(runFAST_multiprocess, True, False) #silence=True, echo=False

    # Stress -------------------------------------------------------------------
    # computers.run(runStress_multiprocess)

    # Fatigue ------------------------------------------------------------------
    # computers.run(runFatigue_multiprocess)

    # Stress + Fatigue ---------------------------------------------------------
    # computers.resume('Fatigue', outputFileSize=20*1024)
    computers.run(runStressFatigue_multiprocess, 10, False) # thetaStep, echo


#!------------------------------------------------------------------------------
#!                                     RUNNING TEST
#!------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
        # check_seeds()
