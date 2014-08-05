#!/usr/bin/env python
import sys
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import os
import configLimits as cfl
from configLimits import AutoVivification

gROOT.SetBatch()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

YR = cfl.YR
sigFit = cfl.sigFit
testPoint = cfl.testPoint
highMass = cfl.highMass

# rounding function for interpolation
def roundTo5(x, base=5):
  return int(base * round(float(x)/base))

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
  if batch == 'True':
    cpuNum = 1
  else:
    cpuNum = 12

  set_palette()

  massList = cfl.massListBig
  sigNameList = cfl.sigNameList

  rooWsFile = TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix+'.root')
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
          mzg.setRange('fitRegion1',115,int(massLow)+15)
        elif massLow > 160:
          mzg.setRange('fitRegion1',int(massLow)-50,int(massLow)+50)
        else:
          mzg.setRange('fitRegion1',int(massLow)-15,int(massLow)+15)
        sigNameLow = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massLow)])
        sig_ds_Low = myWs.data(sigNameLow)
        #sig_ds_Low = RooDataHist('dh'+sigNameLow[2:],'dh'+sigNameLow[2:],RooArgSet(mzg),sig_ds_Low)
        if massLow == massHi:
          dsList.append(sig_ds_Low)

        if sigFit == 'TripG':
          SigFit_Low = BuildTripleGaussV2(tev,lep,cat,prod,str(massLow),'Low',mzg,mean1 = massLow)[0]
        else:
          SigFit_Low = BuildCrystalBallGauss(tev,lep,cat,prod,str(massLow),'Low',mzg,meanG = massLow, meanCB = massLow)[0]

        SigFit_Low.fitTo(sig_ds_Low, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))

        ###### fit the hi mass point
        #if massHi<=125:
        if massHi<=100:
          mzg.setRange('fitRegion2',115,int(massHi)+15)
        elif massHi > 160:
          mzg.setRange('fitRegion2',int(massHi)-50,int(massHi)+50)
        else:
          mzg.setRange('fitRegion2',int(massHi)-15,int(massHi)+15)
        sigNameHi = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massHi)])
        sig_ds_Hi = myWs.data(sigNameHi)
        #sig_ds_Hi = RooDataHist('dh'+sigNameHi[2:],'dh'+sigNameHi[2:],RooArgSet(mzg),sig_ds_Hi)

        if sigFit == 'TripG':
          SigFit_Hi = BuildTripleGaussV2(tev,lep,cat,prod,str(massHi),'Hi',mzg,mean1 = massHi)[0]
        else:
          SigFit_Hi = BuildCrystalBallGauss(tev,lep,cat,prod,str(massHi),'Hi',mzg,meanG = massHi, meanCB = massHi)[0]

        SigFit_Hi.fitTo(sig_ds_Hi, RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))

      ###### interpolate the two mass points
      massDiff = (massHi - mass)/5.
      #if mass<=125:
      if mass<=100:
        mzg.setRange('fitRegion_'+massString,115,mass+15)
      elif mass > 160:
        mzg.setRange('fitRegion_'+massString,mass-50,mass+50)
      else:
        mzg.setRange('fitRegion_'+massString,mass-15,mass+15)
      beta = RooRealVar('beta','beta', 0.5, 0., 1.)
      if massHi == massLow:
        beta.setVal(1);
      else:
        beta.setVal(massDiff)

      interp_pdf = RooIntegralMorph('interp_pdf', 'interp_pdf', SigFit_Low, SigFit_Hi, mzg, beta)
      interp_ds = interp_pdf.generate(RooArgSet(mzg), 10000)
      yieldNum = (sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))
      normList.append(yieldNum)
      yieldName = '_'.join([prod,'hzg','yield',lep,tev,'cat'+cat])
      yieldVar = RooRealVar(yieldName,yieldName,yieldNum)

      #print yieldName
      #print yieldNum, sig_ds_Low.sumEntries()
      #print
      #raw_input()


      sigNameInterp = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(mass)])

      if sigFit == 'TripG':
        SigFit_Interp,paramList = BuildTripleGaussV2(tev,lep,cat,prod,str(mass),'Interp',mzg,mean1 = mass)
      else:
        SigFit_Interp,paramList = BuildCrystalBallGauss(tev,lep,cat,prod,str(mass),'Interp',mzg,meanG = mass, meanCB = mass)

      SigFit_Interp.fitTo(interp_ds, RooFit.Range('fitRegion_'+massString), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum), RooFit.PrintLevel(-1))
      for param in paramList:
        param.setConstant(True)
      fitList.append(SigFit_Interp)

      #newFitName = '_'.join([prod,'hzg',lep,'cat'+cat,tev])
      #SigFit_Interp.SetName(newFitName)

      getattr(cardDict[lep][tev][cat][str(mass)],'import')(SigFit_Interp)

      getattr(cardDict[lep][tev][cat][str(mass)],'import')(yieldVar)
      cardDict[lep][tev][cat][str(mass)].commitTransaction()

    testFrame = mzg.frame(float(massList[0])-15,float(massList[-1])+5)
    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-1]
      #fit.plotOn(testFrame)
      #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
      fit.plotOn(testFrame, RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
      fit.paramOn(testFrame)
    for i,signal in enumerate(dsList):
      signal.plotOn(testFrame, RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(150))
    testFrame.Draw()
    c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/'+'_'.join(['test','sig','fit',sigFit,suffix,prod,lep,tev,'cat'+cat])+'.pdf')


    if highMass:
      testFrame = mzg.frame(float(testPoint)-50, float(testPoint)+50)
    else:
      testFrame = mzg.frame(float(testPoint)-15, float(testPoint)+15)
    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-2]
      #fit.plotOn(testFrame)
      #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
      if regionName == testPoint:
        fit.plotOn(testFrame, RooFit.Name('model'),RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
        fit.paramOn(testFrame)

    if float(testPoint)%5==0:
      for i,signal in enumerate(dsList):
        regionName = signal.GetName().split('_')[-1]
        if regionName == 'M'+testPoint[0:3]:
          signal.plotOn(testFrame, RooFit.Name('data'),RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(150))
      testFrame.Draw()

      ndof = 0
      if sigFit == 'TripG': ndof = 8
      else: ndof = 7
      chi2 = testFrame.chiSquare('model','data',ndof)
      txt = TText(0,0,'chi2/ndof: '+'{0:.3f}'.format(chi2))
      txt.SetNDC()
      txt.SetX(0.7)
      txt.SetY(0.7)
      txt.SetTextSize(0.04)
      testFrame.addObject(txt)
    testFrame.Draw()
    c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/'+'_'.join(['test','sig','fit',sigFit,'M'+testPoint,suffix,prod,lep,tev,'cat'+cat])+'.pdf')

  for prod in sigNameList:
    for mass in massList:
      if sigFit == 'TripG':
        #print 'nofix'
        SignalNameParamFixerTripGV2(tev,lep,cat,prod,mass,cardDict[lep][tev][cat][mass])
      else:
        SignalNameParamFixerCBG(tev,lep,cat,prod,mass,cardDict[lep][tev][cat][mass])

  for mass in massList:
    fileName = '_'.join(['SignalOutput',lep,tev,'cat'+cat,mass])
    if not os.path.isdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass): os.mkdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass)
    cardDict[lep][tev][cat][mass].writeToFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'+fileName+'.root')


#signal = myWs.data('ds_sig_gg_el_2012_cat4_M125')
#SigFit = BuildCrystalBallGauss('2012','el','4','gg','125',mzg)
#SigFit.fitTo(signal, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))
#SigFit.fitTo(signal, RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))

if __name__=="__main__":
  print len(sys.argv)
  print sys.argv
  if len(sys.argv) != 6:
    print 'usage: ./signalCBFits lepton tev cat suffix batch'
  else:
    SignalFitMaker(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))

