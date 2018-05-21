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
#   - 0.1: [20/05/2018] write stress in MPa, reform data class structure
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
import csv, math, numpy, time
from math import sin, cos, radians


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
    def __init__(self, file, startline, gageOutput, thetaStep=10, checkInfo=False):
        self.filenameInput = str(file)
        self.filenameOutput = ''
        self.fieldnamesInput = []
        self.fieldnamesOutput = []
        self.startline = startline
        self.gageOutput = gageOutput
        self.thetaStep = thetaStep
        self.listOfTheta = []
        self.checkInfo = checkInfo
        self.datareader = None
        self.datawriter = None
        self.dataInput = dict.fromkeys(self.gageOutput)
        self.resultField = dict.fromkeys(self.gageOutput)
        self.dataOutput = []
        self.section = dict.fromkeys(self.gageOutput)

        self.run()

    def run(self):
        print "Nominal stress v0.1 (May 20 2018)"
        self.__geometry()
        print "|- Importing "+self.filenameInput+" ..."
        self.open()
        print "|- Calculating the nominal stress ..."
        self.calculate(self.thetaStep)
        print "|- Saving data ..."
        self.save()

    def open(self, filename=None):
        if filename is not None: self.filenameInput = filename

        with open(self.filenameInput, 'rb') as f:
            [next(f) for i in range(self.startline-1)] # read the file from the title line                
            datareader = csv.DictReader(f, delimiter='\t')
            self.datareader = datareader

            next(datareader) # ignore the row with the unit
            for i in self.gageOutput:
                self.dataInput[i] = {'FLzt':[], 'MLxt':[], 'MLyt':[]}
            self.dataInput['Time'] = []

            for row in datareader:
                self.fieldnamesInput = row.keys() # save the titles of the talbe
                
                self.dataInput['Time'].append( float(row['Time      ']) ) # time steps

                for i in self.gageOutput:            
                    # force and moment on each node
                    forceZt = float(row['TwHt'+str(i)+'FLzt '])
                    momentXt = float(row['TwHt'+str(i)+'MLxt '])
                    momentYt = float(row['TwHt'+str(i)+'MLyt '])
                    self.dataInput[i]['FLzt'].append(forceZt)
                    self.dataInput[i]['MLxt'].append(momentXt)
                    self.dataInput[i]['MLyt'].append(momentYt)

        self.dataLength = len(self.dataInput[i]['FLzt'])

    def __geometry(self):
        self.NTwGages = 9
        self.TwrGagNd = [1,3,5,8,11,14,16,18,20] # import from Elastody.dat
        self.TwrNodes = 20
        self.TowerBsHt = 0.0 # [m]
        self.TwrDraft = 0.0 # [m]
        self.TwrElevation = [0.00, 8.76, 17.52, 26.28, 35.04, 43.80, 52.56, 61.32, 70.08,\
                            78.84, 87.60] # [m]
        self.TowerHt = self.TwrElevation[-1]
        self.outerDiameter = [6.0000, 5.7870, 5.5740, 5.3610, 5.1480, 4.9350, 4.7220, \
                              4.5090, 4.2960, 4.0830, 3.8700] # [m]
        self.thickness = [0.03510, 0.03406, 0.03302, 0.03198, 0.03094, 0.02990, 0.02886, \
                          0.02782, 0.02678, 0.02574, 0.02470]
        self.innerDiameter = [i[0]-2*i[1] for i in zip(self.outerDiameter,self.thickness)]

        for i in self.gageOutput:
            elevation, outerR, area, inertia, TwrNodeNo = self.property(i)
            self.section[i] = {'TwrNodeNo':TwrNodeNo, 'z':elevation, 'Re':outerR, \
                               'A':area, 'Igx':inertia, 'Igy':inertia}
        
        # print the geometry information of strain gages
        if self.checkInfo is True:
            print "   ===== Tower geometry and Cross section infomation =====   "
            print "Tower height : ", self.TowerHt, "m"
            print "Total tower nodes : ", self.TwrNodes
            print "Total strain gage locations : ", self.NTwGages
            print " Gage n° | Tower node n° | Elevation(m) | Outer Radius(m) |", \
                  "Area(m2) | 2nd moment of inertia(m4) "
            for i in self.gageOutput:
                print "{0:^9d}|{1:^15d}|{2:^14.2f}|{3:^17.4f}|{4:^10.4f}|{5:^27.4f}"\
                      .format(i, self.section[i]['TwrNodeNo'], self.section[i]['z'], \
                       self.section[i]['Re'],self.section[i]['A'],self.section[i]['Igx'],)

    def property(self, i):
        j = self.TwrGagNd[i-1]
        elevation = self.TowerBsHt + \
                    (j-0.5) * (self.TowerHt+self.TwrDraft-self.TowerBsHt)/self.TwrNodes

        outerD = numpy.interp(elevation, self.TwrElevation, self.outerDiameter)
        innerD = numpy.interp(elevation, self.TwrElevation, self.innerDiameter)
        outerR = outerD/2

        area = math.pi*(outerD**2-innerD**2)/4
        inertia = (outerD**4-innerD**4)*math.pi/64

        return elevation, outerR, area, inertia, j

    def stress(self, i, j, theta):
        """
        Calculate the stress

        *INPUT*
            i : the number of gage node
            j : the number of line in input file (time)
            theta : the stress location
        """
        x = self.section[i]['Re'] * cos(radians(theta))
        y = self.section[i]['Re'] * sin(radians(theta))

        stress = self.dataInput[i]['FLzt'][j] / self.section[i]['A'] \
                 - self.dataInput[i]['MLxt'][j]*y / self.section[i]['Igx'] \
                 + self.dataInput[i]['MLyt'][j]*x / self.section[i]['Igy']
        stress = stress / 1000. # convert stress into MPa

        return stress

    def __makeListOfTheta(self, thetaStep):
        self.listOfTheta = tuple(range(0, 360, thetaStep))

    def stressInPlane(self, i, j):
        # calculate the stress in plane
        for theta in self.listOfTheta:
            stress = self.stress(i,j,theta)
            
            self.resultField[i][j][theta] = stress

    def stressField(self):
        for i in self.gageOutput:            
            self.resultField[i] = dict.fromkeys(range(self.dataLength))
            for j in range(self.dataLength):
                self.resultField[i][j] = {}
                self.stressInPlane(i,j)

    def __writeToRow(self):
        # Prepare the row that will be written
        for j in range(self.dataLength):
            row = {}
            row['Time      '] = str("{:>10.4f}").format(self.dataInput['Time'][j])
            for i in self.gageOutput:
                for theta in self.listOfTheta:
                    header = str("TwHt{0}@{1:<4d}").format(i, theta)
                    row[header] = str("{:>10.3E}").format(self.resultField[i][j][theta])

            self.dataOutput.append(row)
    
    def calculate(self, thetaStep):
        self.__makeListOfTheta(thetaStep)
        self.stressField()
        self.__writeToRow()

    def save(self, filename=None):
        if filename is None: filename = self.filenameInput+'Stress' 

        # Create the title line
        self.fieldnamesOutput.append('Time      ')
        for i in self.gageOutput:
            for theta in self.listOfTheta:
                header = str("TwHt{0}@{1:<4d}").format(i, theta)
                self.fieldnamesOutput.append(header)

        # Create the unit line
        self.fieldunitsOutput = dict.fromkeys(self.fieldnamesOutput, "{:^10}"\
                                              .format("(MPa)"))
        self.fieldunitsOutput['Time      '] = "{:^10}".format("(s)")
        
        # Save result to the file
        with open(filename, 'wb') as f:
            self.filenameOutput = filename
            
            for i in range(self.startline-1):
                f.write("\n")

            datawriter=csv.DictWriter(f, delimiter='\t', fieldnames=self.fieldnamesOutput)
            self.datawriter = datawriter

            datawriter.writeheader() # channel titles

            datawriter.writerow(self.fieldunitsOutput) # channel units
            for row in self.dataOutput:
                datawriter.writerow(row)


def main():
    # mydata=data(file='DLC1.2_NTM_3mps.out', startline=7, gageOutput=[1,9], thetaStep=5,\
    #             checkInfo=True)
    
    for i in range(3,27,2):
        TIK = time.time()
        
        filename = 'DLC1.2_NTM_'+str(i)+'mps.out'
        mydata = data(filename, 7, [1,9])
        
        del mydata

        TOK = time.time()
        elapsedTime = TOK - TIK
        print "|- Finished! "+str("{:.2f}").format(elapsedTime)+"s used.\n"


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
