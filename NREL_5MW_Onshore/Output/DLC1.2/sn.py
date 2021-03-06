#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# S-N CURVES WITH GOODMAN CORRECTION
# An implementation of DNVGL-RP-C203 (April 2016) S-N curves. This work is inspired by
# https://github.com/iamlikeme/sncurves.
#
#
# Authors: Hao BAI
# Date: 03/06/2018
#
# Version:
#   - 0.0: 
# Comments:
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#-----------------------------------------------------------------------------------------
#                                           MODULES PRÉREQUIS
#-----------------------------------------------------------------------------------------
#============================== Modules Personnels ==============================

#============================== Modules Communs ==============================
from collections import namedtuple
from math import log10
#-----------------------------------------------------------------------------------------
#                                          PROGRAMME PRINCIPALE
#-----------------------------------------------------------------------------------------
class dnvgl(object):
    """
    DNVGL-RP-C203 << Recommended Practice - Fatigue design of offshore steel structures >>
    (Edition April 2016)

    *ATTRIBUTES*
        SNcurve : DNVGL notation of S-N curve
        air : S-N curves in air (True[default]: in air; False: in seawater)
        cp : cathodic protection (only valide in seawater, False[default])
        Goodman : Goodman correction (False[default])
    """
    def __init__(self, SNcurve, air=True, cp=False, Goodman=(False, 0.0), material=''):
        self.SNcurve = SNcurve
        self.air = air
        self.cp = cp
        self.Goodman = Goodman
        self.material = material

        self.__curves = dict.fromkeys(('B1', 'B2', 'C', 'C1', 'C2', 'D', 'E', 'F', 'F1',
                                       'F3','G','W1', 'W2', 'W3'))
        self.__materials = dict.fromkeys(('C','C-Mn'))

        # print "S-N curve v0.0 (June 3 2018)"
        self.__build()
        self.__choose()

    def __build(self):
        """
        Build database
        """
        # §1.2.1 steel forgings in air, page 9
        # Table D-1 Design S-N curves for steel forgings in air, page 168
        # Rm : ultimate tensile strength = résistance à la traction (MPa)
        # Re : yield strength = limite d'élasticité (MPa)
        record = namedtuple('Material', 'Rm_air, Re_air, Rm_sea, Re_sea')
        self.__materials['C'] = record(862, 724, 793, 689)
        self.__materials['C-Mn'] = record(None, 960, None, 690)

        # Table 2-1 S-N curves in air, page 23
        # m : negative inverse slope of S-N curve
        # a : intercept of log N-axis by S-N curve
        # N : number of cycles to failure at fatigue limite = 10^7
        # Sf : fatigue limite at 10^7 cycles (MPa)
        record = namedtuple('SNcurve', ('air, cp, m1, a1, m2, a2, N, Sf, k, SCF'))
        self.__curves['B1'] = record(True, None, 4.0, 15.117, 5.0, 17.146, 1e7, 106.97, 0.00, None)
        self.__curves['B2'] = record(True, None, 4.0, 14.885, 5.0, 16.856, 1e7,  93.59, 0.00, None)
        self.__curves['C']  = record(True, None, 3.0, 12.592, 5.0, 16.320, 1e7,  73.10, 0.05, None)
        self.__curves['C1'] = record(True, None, 3.0, 12.449, 5.0, 16.081, 1e7,  65.50, 0.10, None)
        self.__curves['C2'] = record(True, None, 3.0, 12.301, 5.0, 15.835, 1e7,  58.48, 0.15, None)
        self.__curves['D']  = record(True, None, 3.0, 12.164, 5.0, 15.606, 1e7,  52.63, 0.20, 1.00)
        self.__curves['E']  = record(True, None, 3.0, 12.010, 5.0, 15.350, 1e7,  46.78, 0.20, 1.13)
        self.__curves['F']  = record(True, None, 3.0, 11.855, 5.0, 15.091, 1e7,  41.52, 0.25, 1.27)
        self.__curves['F1'] = record(True, None, 3.0, 11.699, 5.0, 14.832, 1e7,  36.84, 0.25, 1.43)
        self.__curves['F3'] = record(True, None, 3.0, 11.546, 5.0, 14.576, 1e7,  32.75, 0.25, 1.61)
        self.__curves['G']  = record(True, None, 3.0, 11.398, 5.0, 14.330, 1e7,  29.24, 0.25, 1.80)
        self.__curves['W1'] = record(True, None, 3.0, 11.261, 5.0, 14.101, 1e7,  26.32, 0.25, 2.00)
        self.__curves['W2'] = record(True, None, 3.0, 11.107, 5.0, 13.845, 1e7,  23.39, 0.25, 2.25)
        self.__curves['W3'] = record(True, None, 3.0, 10.970, 5.0, 13.617, 1e7,  21.05, 0.25, 2.50)


    def __choose(self):
        # Without Goodman correction
        curve = self.__curves.get(self.SNcurve)
        if curve is None:
            print("[Error] No such S-N curve !")
            exit()
        else:
            self.curveRef = curve

        # With Goodman correction: by using ultimate tensile strength
        if self.Goodman[0] is True:
            # Get material
            if self.material is '':
                material=self.__materials.get('C') # default material
            else:
                material=self.__materials.get(self.material)
                if material is None:
                    print("[Error] No such material !")
                    exit()
            # Sfa : alternating stress (MPa)
            if self.air is True:
                Sfa = curve.Sf * (1 - self.Goodman[1]/material.Rm_air)
            else:
                Sfa = curve.Sf * (1 - self.Goodman[1]/material.Rm_sea)
            # Change a1 and a2
            a1 = log10(curve.N) + curve.m1*log10(Sfa)
            a2 = log10(curve.N) + curve.m2*log10(Sfa)
            self.curveGoodman = curve._replace(a1=a1, a2=a2, Sf=Sfa)

    def whichSN(self, stressRange, curveConf):
        if stressRange >= curveConf.Sf:
            N = 10.0**(curveConf.a1 - curveConf.m1*log10(stressRange))
        elif stressRange < curveConf.Sf:
            N = 10.0**(curveConf.a2 - curveConf.m2*log10(stressRange))
        return N

    def sn(self, stressRange):
        if self.Goodman[0] is True:
            return self.whichSN(stressRange, self.curveGoodman)
        else:
            return self.whichSN(stressRange, self.curveRef)
    
    def whichNS(self, cycle, curveConf):
        if cycle <= curveConf.N:
            stressRange = 10.0**((curveConf.a1-log10(cycle))/curveConf.m1)
        elif cycle > curveConf.N:
            stressRange = 10.0**((curveConf.a2-log10(cycle))/curveConf.m2)
        return stressRange

    def ns(self, cycle):
        if self.Goodman[0] is True:
            return self.whichNS(cycle, self.curveGoodman)
        else:
            return self.whichNS(cycle, self.curveRef)

    def plotSN(self):
        """
        Plot S-N curve
        """
        from matplotlib import pyplot as plt

        X = range(int(1e4), int(1e8+1), int(1e6))
        Y = []
        [Y.append(self.whichNS(x, self.curveRef)) for x in X]
        plt.loglog(X,Y, 'b', label="S-N curve") # Plot S-N curve
        x_reversal = self.curveRef.N
        y_reversal = self.whichNS(self.curveRef.N, self.curveRef)
        plt.plot(x_reversal, y_reversal, 'b*') # Plot reversal point at 10^7
        coordinates = r"$(10^{0:.0f},{1:.2f})$".format(log10(x_reversal), y_reversal)
        plt.text(x_reversal, y_reversal, coordinates, color='b')

        # Plot S-N curve with Goodman correction
        if self.Goodman[0] is True:
            Y = []
            [Y.append(self.whichNS(x, self.curveGoodman)) for x in X]
            plt.loglog(X,Y, 'r', label="S-N curve with Goodman") # Plot S-N curve
            x_reversal = self.curveGoodman.N
            y_reversal = self.whichNS(self.curveGoodman.N, self.curveGoodman)
            plt.plot(x_reversal, y_reversal, 'r*') # Plot reversal point at 10^7
            coordinates = r"$(10^{0:.0f},{1:.2f})$".format(log10(x_reversal), y_reversal)
            plt.text(x_reversal, y_reversal, coordinates, verticalalignment='top', \
                     horizontalalignment='right', color='r', )

        # Make title, legend, label and so on
        if self.air is True:
            title = "S-N curve : "+self.SNcurve+" in air"
        elif self.cp is True:
            title = "S-N curve : "+self.SNcurve+" in seawater with cathodic protection"
        else:
            title = "S-N curve : "+self.SNcurve+" in seawater without cathodic protection"
        plt.title(title)
        plt.legend()
        plt.xlabel("Number of cycles")
        plt.ylabel("Stress range (MPa)")
        plt.axis([1e4, 1e8, 1e1, 1e3]) # plt.xlim(1e4, 1e8)
        plt.grid(True, which='both') # show 'major', 'minor' or 'both' tick grids
        plt.show()


def main():
    curve = dnvgl('B1', Goodman=(True, 20.0))
    print(curve.sn(curve.ns(1e7)))
    curve.plotSN()
    print('|- OK')


#-----------------------------------------------------------------------------------------
#                                               EXÉCUTION
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
