#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import os

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

def set_palette(name='palette', ncontours=999):
  """Set a color palette from a given RGB list
  stops, red, green and blue should all be lists of the same length
  see set_decent_colors for an example"""

  if name == "gray" or name == "grayscale":
      stops = [0.00, 0.34, 0.61, 0.84, 1.00]
      red   = [1.00, 0.84, 0.61, 0.34, 0.00]
      green = [1.00, 0.84, 0.61, 0.34, 0.00]
      blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
  # elif name == "whatever":
      # (define more palettes)
  else:
      # default palette, looks cool
      stops = [0.00, 0.34, 0.61, 0.84, 1.00]
      red   = [0.00, 0.00, 0.87, 1.00, 0.51]
      green = [0.00, 0.81, 1.00, 0.20, 0.00]
      blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

  s = np.array(stops, 'd')
  r = np.array(red, 'd')
  g = np.array(green, 'd')
  b = np.array(blue, 'd')

  npoints = len(s)
  TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
  gStyle.SetNumberContours(ncontours)


def SignalFitMaker(lep, tev, cat, suffix, batch = False):
  if batch:
    cpuNum = 1
  else:
    cpuNum = 12

  set_palette()

  massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
   '124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
   '125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
   '127.0','127.5','128.0','128.5','129.0','129.5','130.0',
   '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
   '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
   '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
   '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
  #massList = ['125.0']
  #massList = ['130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
  # '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0']
  sigNameList = ['ggH','qqH','ttH','WH','ZH']
  #sigNameList = ['gg']

  rooWsFile = TFile('outputDir/'+suffix+'/initRooFitOut_'+suffix+'.root')
  myWs = rooWsFile.Get('ws')
#myWs.Print()

  RooRandom.randomGenerator().SetSeed(8675309)

  c = TCanvas("c","c",0,0,500,400)
  c.cd()
  mzg = myWs.var('CMS_hzg_mass')
  cardDict = AutoVivification()
  for mass in massList:
    cardDict[lep][tev][cat][mass] = RooWorkspace('ws_card')


# we need crystal ball + gaussian fits for all mass points, and for all production methods.
# we also need to interpolate the distributions for 0.5 mass bins, so we use some tricks
# in order to create new fits out of the existing 5GeV steps

###################
# Start the Loop! #
###################

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
        sigNameLow = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massLow)])
        sig_ds_Low = myWs.data(sigNameLow)
        if massLow == massHi:
          dsList.append(sig_ds_Low)
          print sig_ds_Low.GetName()
          #raw_input()

        CBG_Low = BuildCrystalBallGauss(tev,lep,cat,prod,str(massLow),'Low',mzg,meanG = massLow, meanCB = massLow)[0]

        CBG_Low.fitTo(sig_ds_Low, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))

        ###### fit the hi mass point
        #if massHi<=125:
        if massHi<=100:
          mzg.setRange('fitRegion2',115,int(massHi)+10)
        else:
          mzg.setRange('fitRegion2',int(massHi)-15,int(massHi)+10)
        sigNameHi = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massHi)])
        sig_ds_Hi = myWs.data(sigNameHi)

        CBG_Hi = BuildCrystalBallGauss(tev,lep,cat,prod,str(massHi),'Hi',mzg,meanG = massHi, meanCB = massHi)[0]

        CBG_Hi.fitTo(sig_ds_Hi, RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))

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
      yieldName = '_'.join([prod,'hzg','yield',lep,tev,'cat'+cat])
      yieldVar = RooRealVar(yieldName,yieldName,sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))


      sigNameInterp = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(mass)])

      CBG_Interp,paramList = BuildCrystalBallGauss(tev,lep,cat,prod,str(mass),'Interp',mzg,meanG = mass, meanCB = mass)

      CBG_Interp.fitTo(interp_ds, RooFit.Range('fitRegion_'+massString), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))
      for param in paramList:
        param.setConstant(True)
      fitList.append(CBG_Interp)
      getattr(cardDict[lep][tev][cat][str(mass)],'import')(CBG_Interp)
      getattr(cardDict[lep][tev][cat][str(mass)],'import')(yieldVar)
      cardDict[lep][tev][cat][str(mass)].commitTransaction()

    testFrame = mzg.frame(float(massList[0])-10,float(massList[-1])+5)
    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-1]
      #fit.plotOn(testFrame)
      #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
      fit.plotOn(testFrame, RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
      fit.paramOn(testFrame)
    for i,signal in enumerate(dsList):
      signal.plotOn(testFrame, RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1))
    testFrame.Draw()
    c.Print('debugPlots/'+'_'.join(['test','sig','fit',prod,lep,tev,'cat'+cat])+'.pdf')

  for prod in sigNameList:
    for mass in massList:
      SignalNameParamFixer(tev,lep,cat,prod,mass,cardDict[lep][tev][cat][mass])

  for mass in massList:
    fileName = '_'.join(['SignalOutput',lep,tev,'cat'+cat,mass])
    if not os.path.isdir('outputDir/'+suffix+'/'+mass): os.mkdir('outputDir/'+suffix+'/'+mass)
    cardDict[lep][tev][cat][mass].writeToFile('outputDir/'+suffix+'/'+mass+'/'+fileName+'.root')


#signal = myWs.data('ds_sig_gg_el_2012_cat4_M125')
#CBG = BuildCrystalBallGauss('2012','el','4','gg','125',mzg)
#CBG.fitTo(signal, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))
#CBG.fitTo(signal, RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))

if __name__=="__main__":
  print len(sys.argv)
  print sys.argv
  if len(sys.argv) != 6:
    print 'usage: ./signalCBFits lepton tev cat'
  else:
    SignalFitMaker(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))

