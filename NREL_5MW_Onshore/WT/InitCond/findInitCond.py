#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Using matplotlib to produce publication quality graphics
#
# Authors: Hao BAI
# Date: 19/06/2018
#
# Comments:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import collections, numpy, pickle, csv
import time


#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
def find_initial_condition():
    dataAggregated = collections.namedtuple('condition', 'velocity, Time, TipDxc1, TipDyc1, PtchPMzc1, PtchPMzc2, PtchPMzc3, Azimuth, RotSpeed, NacYaw, YawBrTDxt, YawBrTDyt')

    # 103  TipDxc1     (m)
    # 104  TipDyc1     (m)
    # 109  PtchPMzc1   (deg)
    # 110  PtchPMzc2   (deg)
    # 111  PtchPMzc3   (deg)
    # 112  Azimuth     (deg)
    # 113  RotSpeed    (rpm)
    # 114  NacYaw      (deg)
    #  92  YawBrTDxt   (m)
    #  93  YawBrTDyt   (m)
    columns = (1, 103, 104, 109, 110, 111, 112, 113, 114, 92, 93)

    root = '/Users/hbai/Eolien/Parameters/NREL_5MW_Onshore/Output/DLC0.1/DLC0.1_CST_'
    files = ('3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25')

    allConditions = []
    for file in files:
        data = read_by_pandas_readcsv(root+file+'.out')
        temp = [file]
        [temp.append(data[col]['Records'][-1]) for col in columns]
        d1 = dataAggregated._make(temp)
        allConditions.append(d1)
    
    # save to CSV file
    with open('new_InitialCondition', 'wt') as f:
        datawriter = csv.DictWriter(f, delimiter='\t', fieldnames=d1._fields)
        datawriter.writeheader()
        for cond in allConditions:
            row = cond._asdict()
            datawriter.writerow(row)


def read_by_pandas_readcsv(filename):
    TIK = time.time()
    data = collections.OrderedDict()

    import pandas
    dataframe = pandas.read_csv(filename, delimiter='\t', encoding='ISO-8859-1', header=6,
                                skip_blank_lines=False) # low_memory=False, dtype=str => slow
    dataframe.drop([0], inplace=True) # delete the unit line

    for i in range(dataframe.columns.size):
        name = dataframe.columns[i] # get the column head
        records = dataframe.iloc[:,i].values.astype('float') # get column values in float
        data[i+1] = {'Title':name, 'Records':list(records)}

    TOK = time.time()
    print(filename, "loaded :", TOK-TIK, "s")

    return data


def main():
    find_initial_condition()
    

#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()