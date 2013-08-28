#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

# rounding function for interpolation
def roundTo5(x, base=5):
  return int(base * round(float(x)/base))

# class for multi-layered nested dictionaries, pretty cool
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

'''
leptonList = ['mu','el']
yearList = ['2012','2011']
catList = ['1','2','3','4']
massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0']
#massList = ['120.0','120.5','121.0']
#massList = ['120','125','130','135','140','145','150']
sigNameList = ['gg','vbf','tth','wh','zh']
'''
leptonList = ['mu']
yearList = ['2012']
catList = ['1']
massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0',
 '125.5','126.0','126.5','127.0','127.5','128.0','128.5','129.0','129.5','130.0']
#massList = ['120.0','120.5','121.0']
#massList = ['138.0']
#massList = ['120','125','130','135','140','145','150']
sigNameList = ['gg','vbf','tth','wh','zh']
#sigNameList = ['zh']

rooWsFile = TFile('testRooFitOut.root')
myWs = rooWsFile.Get('ws')
#myWs.Print()

RooRandom.randomGenerator().SetSeed(8675309)

c = TCanvas("c","c",0,0,500,400)
c.cd()
mzg = myWs.var('CMS_hzg_mass')
cardDict = AutoVivification()
for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      for mass in massList:
        cardDict[lepton][year][cat][mass] = RooWorkspace('ws_card')


# we need crystal ball + gaussian fits for all mass points, and for all production methods.
# we also need to interpolate the distributions for 0.5 mass bins, so we use some tricks
# in order to create new fits out of the existing 5GeV steps

###################
# Start the Loop! #
###################

for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      for prod in sigNameList:
        dsList = []
        fitList = []
        normList = []
        oldMassHi = oldMassLow = 0
        for massString in massList:

#############################################
# Get the high and low mass references      #
# If the point does not need interpolation, #
# we just use it for high and low           #
#############################################

          mass = float(massString)
          if mass%5.0 == 0.0:
            massHi = int(mass)
            massLow = int(mass)
          else:
            massRound = roundTo5(massString)
            if mass<massRound:
              massHi = massRound
              massLow = massRound-5
            else:
              massHi = massRound+5
              massLow = massRound
          ###### only calc the low and high points if they change
          if not(oldMassLow == massLow and oldMassHi == massHi):
            oldMassLow = massLow
            oldMassHi = massHi

            ###### fit the low mass point
            #if massLow<=125:
            if massLow<=100:
              mzg.setRange('fitRegion1',115,int(massLow)+10)
            else:
              mzg.setRange('fitRegion1',int(massLow)-15,int(massLow)+10)
            sigNameLow = '_'.join(['ds','sig',prod,lepton,year,'cat'+cat,'M'+str(massLow)])
            sig_ds_Low = myWs.data(sigNameLow)
            if massLow == massHi: dsList.append(sig_ds_Low)

            if prod is 'zh':
              CBG_Low = BuildCrystalBallGauss(year,lepton,cat,prod,str(massLow),'Low',mzg,mean = massLow, sigmaCB = 1.65, sigmaG = 2, alpha  = 0.7)[0]
            else:
              CBG_Low = BuildCrystalBallGauss(year,lepton,cat,prod,str(massLow),'Low',mzg,mean = massLow)[0]

            CBG_Low.fitTo(sig_ds_Low, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(4), RooFit.PrintLevel(-1))

            ###### fit the hi mass point
            #if massHi<=125:
            if massHi<=100:
              mzg.setRange('fitRegion2',115,int(massHi)+10)
            else:
              mzg.setRange('fitRegion2',int(massHi)-15,int(massHi)+10)
            sigNameHi = '_'.join(['ds','sig',prod,lepton,year,'cat'+cat,'M'+str(massHi)])
            sig_ds_Hi = myWs.data(sigNameHi)

            if prod is 'zh':
              CBG_Hi = BuildCrystalBallGauss(year,lepton,cat,prod,str(massHi),'Hi',mzg,mean = massHi, sigmaCB = 1.65, sigmaG = 2, alpha = 0.7)[0]
            else:
              CBG_Hi = BuildCrystalBallGauss(year,lepton,cat,prod,str(massHi),'Hi',mzg,mean = massHi)[0]

            CBG_Hi.fitTo(sig_ds_Hi, RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(4), RooFit.PrintLevel(-1))

          ###### interpolate the two mass points
          massDiff = (massHi - mass)/5.
          #if mass<=125:
          if mass<=100:
            mzg.setRange('fitRegion_'+massString,115,mass+10)
          else:
            mzg.setRange('fitRegion_'+massString,mass-15,mass+10)
          beta = RooRealVar('beta','beta', 0.5, 0., 1.)
          if massHi == massLow:
            beta.setVal(1);
          else:
            beta.setVal(massDiff)

          interp_pdf = RooIntegralMorph('interp_pdf', 'interp_pdf', CBG_Low, CBG_Hi, mzg, beta)
          interp_ds = interp_pdf.generate(RooArgSet(mzg), 10000)
          normList.append(sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))
          yieldName = '_'.join(['sig',prod,'yield',lepton,year,'cat'+cat])
          yieldVar = RooRealVar(yieldName,yieldName,sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))


          sigNameInterp = '_'.join(['ds','sig',prod,lepton,year,'cat'+cat,'M'+str(mass)])

          if prod is 'zh':
            CBG_Interp,paramList = BuildCrystalBallGauss(year,lepton,cat,prod,str(mass),'Interp',mzg,mean = mass, sigmaCB = 1.65, sigmaG = 2.0, alpha = 0.7)
          else:
            CBG_Interp,paramList = BuildCrystalBallGauss(year,lepton,cat,prod,str(mass),'Interp',mzg,mean = mass)

          CBG_Interp.fitTo(interp_ds, RooFit.Range('fitRegion_'+massString), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(4), RooFit.PrintLevel(-1))
          for param in paramList:
            param.setConstant(True)
          fitList.append(CBG_Interp)
          getattr(cardDict[lepton][year][cat][str(mass)],'import')(CBG_Interp)
          getattr(cardDict[lepton][year][cat][str(mass)],'import')(yieldVar)
          cardDict[lepton][year][cat][str(mass)].commitTransaction()

        testFrame = mzg.frame(float(massList[0])-10,float(massList[-1])+5)
        for i,fit in enumerate(fitList):
          regionName = fit.GetName().split('_')[-1]
          #fit.plotOn(testFrame)
          #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
          fit.plotOn(testFrame, RooFit.Normalization(normList[i],RooAbsReal.NumEvent))
        for signal in dsList:
          signal.plotOn(testFrame)
        testFrame.Draw()
        c.Print('debugPlots/'+'_'.join(['test','sig','fit',prod,lepton,year,'cat'+cat])+'.pdf')

for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      for prod in sigNameList:
        for mass in massList:
          SignalNameParamFixer(year,lepton,cat,prod,mass,cardDict[lepton][year][cat][mass])

for year in yearList:
  for lep in leptonList:
    for cat in catList:
      for mass in massList:
        fileName = '_'.join(['SignalOutput',lep,year,'cat'+cat,mass])
        cardDict[lep][year][cat][mass].writeToFile('testCards/'+fileName+'.root')


#signal = myWs.data('ds_sig_gg_el_2012_cat4_M125')
#CBG = BuildCrystalBallGauss('2012','el','4','gg','125',mzg)
#CBG.fitTo(signal, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))
#CBG.fitTo(signal, RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))

