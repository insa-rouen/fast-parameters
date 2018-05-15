#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST-TRAITEMENT: CALCUL DU CHAMP DE CONTRAINTE
# Sortir l'état de contrainte à partir de résultats obtenus sous FAST, puis réécrire les
# contraintes dans le fichier .out
#
#
# Authors: Hao BAI
# Date: 24/04/2018
#
# Version:
#   - 0.0: only applicable to a annulus secion (that is to say Igx=Igy)
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
import csv, math, numpy


#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class data(object):
    """
    I/O FAST result file .out
    
    *ATTRIBUTES*
        filename : the filename of FAST output file
        startline : the number of the row which has the channel titles
    """
    def __init__(self, startline, gagelist):
        self.filenameInput = ''
        self.filenameOutput = ''
        self.fieldnamesInput = []
        self.fieldnamesOutput = []
        self.startline = startline
        self.gagelist = gagelist
        self.datareader = None
        self.datawriter = None
        self.dataInput = dict.fromkeys(self.gagelist)
        self.resultField = dict.fromkeys(self.gagelist)
        self.dataOutput = []
        self.section = dict.fromkeys(self.gagelist)
        self.__geometry()


    def open(self, filename):
        with open(filename, 'rb') as f:
            self.filenameInput = filename
            [next(f) for i in range(self.startline-1)] # read the file from the title line                
            datareader = csv.DictReader(f, delimiter='\t')
            self.datareader = datareader

            next(datareader) # ignore the row with the unit
            for i in self.gagelist:
                self.dataInput[i] = {'FLzt':[], 'MLxt':[], 'MLyt':[]}
            self.dataInput['Time'] = []

            for row in datareader:
                self.fieldnamesInput = row.keys() # save the titles of the talbe
                
                self.dataInput['Time'].append( float(row['Time      ']) ) # time steps

                for i in self.gagelist:            
                    # force and moment on each node
                    forceZt = float(row['TwHt'+str(i)+'FLzt '])
                    momentXt = float(row['TwHt'+str(i)+'MLxt '])
                    momentYt = float(row['TwHt'+str(i)+'MLyt '])
                    self.dataInput[i]['FLzt'].append(forceZt)
                    self.dataInput[i]['MLxt'].append(momentXt)
                    self.dataInput[i]['MLyt'].append(momentYt)

        self.dataLength = len(self.dataInput[i]['FLzt'])

    def __geometry(self):
        self.twrNodes = 9
        self.twrElevation = [0.00, 8.76, 17.52, 26.28, 35.04, 43.80, 52.56, 61.32, 70.08,\
                            78.84, 87.60]
        self.twrHt = self.twrElevation[-1]
        self.outerDiameter = [6.0000, 5.7870, 5.5740, 5.3610, 5.1480, 4.9350, 4.7220, \
                              4.5090, 4.2960, 4.0830, 3.8700]
        self.thickness = [0.03510, 0.03406, 0.03302, 0.03198, 0.03094, 0.02990, 0.02886, \
                          0.02782, 0.02678, 0.02574, 0.02470]
        self.innerDiameter = [i[0]-2*i[1] for i in zip(self.outerDiameter,self.thickness)]

        for i in self.gagelist:
            elevation, outerR, area, inertia = self.property(i)
            self.section[i] = {'z':elevation, 'Re':outerR, 'A':area, 'Igx':inertia, \
                               'Igy':inertia}

    def property(self, i):
        elevation = (i-0.5)*self.twrHt/self.twrNodes

        outerD = numpy.interp(elevation, self.twrElevation, self.outerDiameter)
        innerD = numpy.interp(elevation, self.twrElevation, self.innerDiameter)
        outerR = outerD/2

        area = math.pi*(outerD**2-innerD**2)/4
        inertia = (outerD**4-innerD**4)*math.pi/64

        return elevation, outerR, area, inertia

    def stressField(self):
        for i in self.gagelist:
            self.resultField[i] = {'SigmaMax':None}
            self.resultField[i]['SigmaMax'] = self.stress(i)

    def stress(self, i):
        """
        Calculate the stress

        *INPUT*
            i : the number of gage node
        """
        x = math.sqrt(2) * self.section[i]['Re']
        y = math.sqrt(2) * self.section[i]['Re']

        stress = []
        for j in range(self.dataLength):
            result = self.dataInput[i]['FLzt'][j] / self.section[i]['A'] \
                     - self.dataInput[i]['MLxt'][j]*y / self.section[i]['Igx'] \
                     + self.dataInput[i]['MLyt'][j]*x / self.section[i]['Igy']
            stress.append(result)
        return stress

    def __writeToRow(self):
        # Prepare the row that will be written


        
        for j in range(self.dataLength):
            row = {}
            row['Time      '] = str("{:>10.4f}").format(self.dataInput['Time'][j])
            for i in self.gagelist:
                row['TwHt'+str(i)+'FLzt'] = str("{:>10.3E}").format(self.dataInput[i]['FLzt'][j])
                row['TwHt'+str(i)+'MLxt'] = str("{:>10.3E}").format(self.dataInput[i]['MLxt'][j])
                row['TwHt'+str(i)+'MLyt'] = str("{:>10.3E}").format(self.dataInput[i]['MLyt'][j])

                row['TwHt'+str(i)+'Sigzt'] = str("{:>10.3E}").format(self.resultField[i]['SigmaMax'][j])

            self.dataOutput.append(row)
    
    def calculate(self):
        self.stressField()
        self.__writeToRow()

    def save(self,filename):
        # Create the title line
        self.fieldnamesOutput.append('Time      ')
        for i in self.gagelist:
            self.fieldnamesOutput.append('TwHt'+str(i)+'FLzt')
            self.fieldnamesOutput.append('TwHt'+str(i)+'MLxt')
            self.fieldnamesOutput.append('TwHt'+str(i)+'MLyt')
            self.fieldnamesOutput.append('TwHt'+str(i)+'Sigzt')

        with open(filename, 'wb') as f:
            self.filenameOutput = filename
            
            for i in range(self.startline-1):
                f.write("\n")

            datawriter=csv.DictWriter(f, delimiter='\t', fieldnames=self.fieldnamesOutput)
            self.datawriter = datawriter
            # [datawriter.writerow(" ") for i in range(self.startline-1)]
            datawriter.writeheader()

            for row in self.dataOutput:
                datawriter.writerow(row)


def main():
    mydata = data(startline=7, gagelist=[1,9])
    mydata.open('DLC1.2_NTM_3mps.out')

    # mydata.open('test.out')
    mydata.calculate()
    mydata.save('testStress.out')
    # print mydata.dataInput
    # print mydata.section




#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
