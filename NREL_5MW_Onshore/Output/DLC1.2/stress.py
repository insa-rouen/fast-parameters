#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: CALCUL DU CHAMP DE CONTRAINTE
# Sortir l'état de contrainte à partir de résultats obtenus sous FAST, puis réécrire les
# contraintes dans le fichier .out
#
#
# Authors: Hao BAI
# Version: 0.0
# Date: 24/04/2018
#
#
# Description:
#
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================
# import colored_traceback.always # Commenter cette ligne si vous n'avez pas installé "colored_traceback"


#============================== Modules Communs ==============================
import csv


#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class data(object):
    """
    I/O data
    
    *ATTRIBUTES*
        filename : the filename of FAST output file
        startline : the number of the headline
        width : The width of terminal
    """
    def __init__(self, filename, startline):
        self.filename = filename
        self.startline = startline

    def open(self):
        with open(self.filename, 'rb') as f:
            [next(f) for i in range(self.startline-1)]
                
            datareader = csv.DictReader(f, delimiter='\t')
            for row in datareader:
                print row
                # print row['Time']



def main():
    mydata = data('test.out', 7)
    mydata.open()




#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
