#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: FIND MAXIMA AND MINIMA
# 
# 
#
#
# Authors: Hao BAI
# Date: 10/10/2018
#
# Version:
#   - 0.0: Initial version, enable multiprocessing
#   - 0.1: Use personlized packages
#   - 0.2: Add new study: grid search on wind speed and gridloss time
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#!------------------------------------------------------------------------------
#!                                          MODULES PRÉREQUIS
#!------------------------------------------------------------------------------
#*============================= Modules Personnels =============================
from tools import utils
from pycrunch import amplitude as amp
#* ============================= Modules Communs ==============================
import time
import multiprocessing


#!------------------------------------------------------------------------------
#!                                         CLASS
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                      FUNCTIONS
#!------------------------------------------------------------------------------



#!------------------------------------------------------------------------------
#!                                     MAIN FUNCTION
#!------------------------------------------------------------------------------
@utils.timer
def main():
    testCase = 5
    if testCase == 1: # simple case
        with utils.cd("~/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC2.3/withoutTRD/EOGO"):
            # bande of grid loss
            filelist = [str(t) for t in utils.frange(74.0, 76.1, 0.1)]

            channels = ['YawBrTDxt','YawBrTDyt', 'YawBrFxp','YawBrFyp',
                        'TwHt4FLxt', 'TwHt4FLyt', 'TwrBsFxt', 'TwrBsFyt',
                        'TwrBsMxt', 'TwrBsMyt']

            # # ----- Running on single processor
            # for file in filelist:
            #     amplitude.find_peak_valley(file, header=7, datarow=6009,
            #                                startline=12, channels=channels)

            # ----- Running on multi processor
            amp.find_peak_valley_multiprocess(filelist, 7, 6009, 12, channels)

    wind = 'EOG'
    speedRange = utils.frange(3.0, 25.1, 0.1) # wind speed [m/s]   
    timeRange = utils.frange(70.0, 80.1, 0.1) # grid loss time [s]
    channels = ['YawBrTDxt',]
    if testCase == 2: # complex case
        with utils.cd("~/Eolien/Parameters/Python/DLC2.3/Output/DLC2.3"):
            # find peak and valley
            filelist = ["{}_{}_{}".format(wind, v, t) for v in speedRange
                        for t in timeRange]
            amp.find_peak_valley_multiprocess(list_filebase=filelist,
                        header=7, datarow=6009, startline=12, channels=channels)
            # find maximum amplitude
            all_files = []
            for v in speedRange:
                temp = ["{}_{}_{}".format(wind, v, t) for t in timeRange]
                all_files.append(temp)
            
            all_results = []
            for f in all_files:
                resu = amp.Amplitude.max_p2p_amplitude(f,channels,'.ext',True)
                all_results.extend(resu)
            # save to file/print to screen
            output = amp.Amplitude.print(all_results, channels,
                                         'max_amplitude.amp')
            # compress files
            output_files = [elem["File"]+".out" for elem in output[channels[0]]]
            pool = multiprocessing.Pool()
            [pool.apply_async(utils.compress, args=(filename, True),
             error_callback=utils.handle_error) for filename in output_files]
            pool.close()
            pool.join()

    # get maxi amplitude for all time range and all speed
    if testCase == 3:
        with utils.cd("~/lofims/Output/DLC2.3"):
            all_files = ["{}_{}_{}".format(wind, v, t) for v in speedRange for t
                         in timeRange]
            all_results = []
            for f in all_files:
                resu = amp.Amplitude.max_p2p_amplitude(f, channels, '.ext',True)
                all_results.extend(resu)
            output = amp.Amplitude.print(all_results, channels,
                                        'max_amplitude_ALL.amp')

    # For testing ...
    if testCase == 4:
        with utils.cd("~/Eolien/Parameters/Python/DLC2.3/Output/DLC2.3"):
            # find peak and valley
            filelist = ["{}_O_{}".format(wind, t) for t in timeRange]
            amp.find_peak_valley_multiprocess(list_filebase=filelist,
                        header=7, datarow=6009, startline=12, channels=channels)
            # find maximum amplitude
            all_files = []
            all_files.append(filelist)
            
            all_results = []
            for f in all_files:
                resu = amp.Amplitude.max_p2p_amplitude(f,channels,'.ext',False)
                all_results.extend(resu)
            # save to file/print to screen
            output = amp.Amplitude.print(all_results, channels,
                                         'max_amplitudeO.amp')

    # To verifiy if .out file contains NaN
    if testCase == 5:
        files = utils.find(".", "*.out")
        [utils.readcsv("./"+f+".out") for f in files]

#!------------------------------------------------------------------------------
#!                                              EXÉCUTION
#!------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
