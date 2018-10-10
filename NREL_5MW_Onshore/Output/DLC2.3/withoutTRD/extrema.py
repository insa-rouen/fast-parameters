#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
#   
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import csv, copy, os
import numpy, json
import pandas, time, collections
from scipy import signal
from contextlib import contextmanager
import numpy as np
import multiprocessing

#-----------------------------------------------------------------------------------------
#                                          CLASS
#-----------------------------------------------------------------------------------------
@contextmanager
def cd(newdir):
    prevdir = os.getcwd() # save current working path
    os.chdir(os.path.expanduser(newdir)) # change directory
    try:
        yield
    finally:
        os.chdir(prevdir) # revert to the origin workinng path


class finder(object):
    """
    Find extrema in .out file
    
    *ATTRIBUTES*
        filename : the filename of stress history file
        header : the number of the row which has the channel titles
    """
    def __init__(self, file, header, datarow, startline, parameters):
        self.file = file
        self.header = header-1 # in pandas.read_csv, the n° row starts from 0
        self.datarow = datarow-1
        self.startline = startline
        self.parameters = parameters

        self.fieldunitsOutput = {}
        self.datareader = None
        self.dataInput = {}
        self.stressFilter = {}

    def run(self, toScreen=True):
        print("Extrema finder v0.0 (October 2 2018)")
        if toScreen: print("|- Importing "+self.file+" ...")
        self.dataInput = self.read_by_pandas_readcsv(filename=self.file+'.out', header=self.header, datarow=self.datarow, toScreen=toScreen)
        
        for para in self.parameters:
            if toScreen: print("|- Searching maximum and minimum of {}...".format(para))
            dataOutput = self.find(para)

            if toScreen: print("|- Saving data ...")
            self.save(para, dataOutput)

        print("|- All parameters {} in {} are realized !".format(self.parameters, self.file))
    
    def read_by_pandas_readcsv(self, filename="", delimiter='\t', header=6, datarow=8, toScreen=True):
        TIK = time.time()
        data = collections.OrderedDict()

        dataframe = pandas.read_csv(filename, delimiter=delimiter, encoding='ISO-8859-1',
                                    header=header, skip_blank_lines=False) # low_memory=False, dtype=str => slow
        if datarow-header >= 2:
            endIndex = (datarow-header)-1
            dataframe.drop(list(range(endIndex)), inplace=True) # delete the unit line

        for i in range(dataframe.columns.size):
            name = dataframe.columns[i] # get the column head
            records = dataframe.iloc[:,i].values.astype('float') # get column values in float
            data[i+1] = {'Title':name, 'Records':list(records)}

        TOK = time.time()
        if toScreen: print("|-", filename, "loaded :", TOK-TIK, "s")

        return data

    def find(self, parameter):
        dataOutput = []
        timeseries = numpy.array(self.dataInput[1]['Records'])

        for key, value in self.dataInput.items():
            if parameter in value['Title']:
                data = numpy.array(value['Records'])
                maxima = signal.argrelextrema(data, numpy.greater_equal, order=10) # find maxima
                result = list(data[maxima[0]])
                timestep = list(timeseries[maxima[0]])
                for i in range(len(result)):
                    dataOutput.append( {'Time      ':"{:^10}".format(timestep[i]), 'Maxi/Mini ':"{:^10.3E}".format(result[i])} )

                minima = signal.argrelextrema(data, numpy.less_equal, order=10) # find minima
                result = list(data[minima[0]])
                timestep = list(timeseries[minima[0]])
                for i in range(len(result)):
                    dataOutput.append( {'Time      ':"{:^10}".format(timestep[i]), 'Maxi/Mini ':"{:^10.3E}".format(result[i])} )
        # sort restuls in the order of time increasing
        dataOutput.sort(key=lambda x:float(x['Time      ']), reverse=False)
        return dataOutput

    def save(self, parameter, dataOutput):
        filename = self.file+'_'+parameter+'.ext'

        # Create the title line
        fieldnamesOutput = []
        fieldnamesOutput.append('Time      ')
        fieldnamesOutput.append('Maxi/Mini ')

        # Create the unit line
        fieldunitsOutput = {}
        fieldunitsOutput['Time      '] = "{:^10}".format("(s)")
        fieldunitsOutput['Maxi/Mini '] = "{:^10}".format("(-)")
        
        # Save result to the file
        with open(filename, 'wt') as f:            
            for i in range(self.startline-1): # skip empty lines
                f.write("\n")

            datawriter=csv.DictWriter(f, delimiter='\t', fieldnames=fieldnamesOutput)
            self.datawriter = datawriter

            datawriter.writeheader() # channel titles

            datawriter.writerow(self.fieldunitsOutput) # channel units
            for row in dataOutput:
                datawriter.writerow(row)



#-----------------------------------------------------------------------------------------
#                                       FUNCTIONS
#-----------------------------------------------------------------------------------------
def run_multiprocess(file, parameters):
    myfinder = finder(file=file, header=7, datarow=6009, startline=12, parameters=parameters)
    myfinder.run(toScreen=False)

def frange(start, stop=None, step=1, precision=None):
    if precision is None:
        fois = 1e7
    else:
        fois = 10**precision
    
    new_start = int(start * fois)
    new_stop = int(stop * fois)
    new_step = int(step * fois)
    r = range(new_start, new_stop, new_step)
    
    l = [i/fois for i in r]
    return l

#-----------------------------------------------------------------------------------------
#                                      MAIN FUNCTION
#-----------------------------------------------------------------------------------------
def main():
    # bande of grid loss
    filelist = [str(t) for t in frange(74.0, 76.1, 0.1)]

    parameters = ["YawBrTDxt", "YawBrTDyt", "YawBrFxp", "YawBrFyp", "TwHt4FLxt", "TwHt4FLyt", "TwrBsFxt", "TwrBsFyt", "TwrBsMxt", "TwrBsMyt"]
    TIK = time.time()  

    # # ----- Running on single processor
    # for file in filelist:
    #     for para in parameters:
    #         myfind = finder(file=file, header=7, datarow=6009, startline=12, parameters=para)
    #         print(file, para, "OK !!!")

    # ----- Running on multi processor
    pool = multiprocessing.Pool(6) # define number of worker (= numbers of processor by default)
    [pool.apply_async(run_multiprocess, args=(file, parameters)) for file in filelist] # map/apply_async: submit all processes at once and retrieve the results as soon as they are finished
    # pool.map(run_multiprocess, seeds)
    pool.close() # close: call .close only when never going to submit more work to the Pool instance
    pool.join() # join: wait for the worker processes to terminate

    TOK = time.time()
    print("|- Total time :", TOK-TIK, "s")

    # ----- Testing
    # finder(file="ETM_25mps_2028409674", header=7, datarow=6009, startline=12, parameters="YawBrTDyt")
    # run_multiprocess("ETM_25mps_2028409674", parameters)



#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
