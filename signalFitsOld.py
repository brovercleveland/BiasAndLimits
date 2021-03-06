#!/usr/bin/env python
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import os
import configLimits as cfl
from configLimits import AutoVivification
import argparse

gROOT.SetBatch()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()
gStyle.SetOptStat(0)

YR = cfl.YR
sigFit = cfl.sigFit
testPoint = cfl.testPoint
highMass = cfl.highMass

# rounding function for interpolation
def roundToN(x, N=5):
  return int(N* round(float(x)/N))

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

def getArgs():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v","--verbose",action = "store_true")
  group.add_argument("-q","--quiet",action = "store_true")
  parser.add_argument("--tev", help="CoM Energy", default = cfl.tevList[0], choices = ['7TeV','8TeV'] )
  parser.add_argument("--lepton", help="Lepton Flavor", default = cfl.leptonList[0], choices = ['mu','el'])
  parser.add_argument("--cat", help="Cat Number", default = cfl.catListSmall[0], type = int)
  parser.add_argument("--suffix", help="Specify suffix", default = cfl.suffix, type = str)
  parser.add_argument("--cores", help="Number of CPU cores for use (must be 1 for batch mode)", default = 12, type = int)
  args = parser.parse_args()
  return args

def SignalFitMaker(lep, tev, cat, suffix, cores):
  cpuNum = cores

  set_palette()

  massList = cfl.massListBig
  sigNameList = cfl.sigNameList

  rooWsFile = TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix+'.root')
  myWs = rooWsFile.Get('ws')
  #myWs.Print()
  narrow = ''
  if 'Narrow' in suffix: narrow = 'Narrow'

  RooRandom.randomGenerator().SetSeed(8675309)

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
    startingVals = []
    paramHists = [
        TH1F('meanGCBG', 'meanGCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('meanCBCBG', 'meanCBCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('sigmaGCBG', 'sigmaGCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('sigmaCBCBG', 'sigmaCBCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('alphaCBG', 'alphaCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('nCBG', 'nCBG', len(massList), float(massList[0]), float(massList[-1])),
        TH1F('fracCBG', 'fracCBG', len(massList), float(massList[0]), float(massList[-1])),
      ]
    for massString in massList:

      #############################################
      # Get the high and low mass references      #
      # If the point does not need interpolation, #
      # we just use it for high and low           #
      #############################################

      fitBuilder = FitBuilder(mzg,tev,lep,cat,sig=prod,mass=massString)

      mass = float(massString)
      if highMass:
        if mass%50.0 == 0.0:
          massHi = int(mass)
          massLow = int(mass)
        else:
          massRound = roundToN(massString,50)
          if mass<massRound:
            massHi = massRound
            massLow = massRound-50
          else:
            massHi = massRound+50
            massLow = massRound
      else:
        if mass%5.0 == 0.0:
          massHi = int(mass)
          massLow = int(mass)
        else:
          massRound = roundToN(massString)
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
          mzg.setRange('fitRegion1',int(massLow)*0.9,int(massLow)*1.1)
        else:
          mzg.setRange('fitRegion1',int(massLow)*0.92,int(massLow)*1.08)
        sigNameLow = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massLow)+narrow])
        #print sigNameLow
        sig_ds_Low = myWs.data(sigNameLow)
        #sig_ds_Low.Print()
        #sig_ds_Low = RooDataHist('dh'+sigNameLow[2:],'dh'+sigNameLow[2:],RooArgSet(mzg),sig_ds_Low)
        if massLow == massHi:
          dsList.append(sig_ds_Low)


        fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(massLow))

        #if len(startingVals) !=0:
        #  SigFit_Low,tempParams= fitBuilder.Build(sigFit, piece = 'Low',
        #      meanG = startingVals[0], meanCB = startingVals[1], sigmaG = startingVals[2], sigmaCB = startingVals[3],
        #      alpha = startingVals[4], n = startingVals[5], frac=startingVals[6])
        if highMass and narrow=='':
          SigFit_Low,tempParams= fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, sigmaG = massLow*0.08, sigmaCB = massLow*0.03)
        elif suffix == '09-3-14_Proper' and cat == '5' and lep == 'el':
          SigFit_Low,tempParams = fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, meanGLow = massLow*0.95, meanGHigh = massLow*1.05, meanCBLow = massLow*0.95, meanCBHigh = massLow*1.05)

        else:
          SigFit_Low,tempParams = fitBuilder.Build(sigFit, piece = 'Low', mean = massLow)

        SigFit_Low.fitTo(sig_ds_Low, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum))
        raw_input()
        startingVals = [x.getVal() for x in tempParams]


        ###### fit the hi mass point
        #if massHi<=125:
        if massHi<=100:
          mzg.setRange('fitRegion2',115,int(massHi)+15)
        elif massHi > 160:
          mzg.setRange('fitRegion2',int(massHi)*0.9,int(massHi)*1.1)
        else:
          mzg.setRange('fitRegion2',int(massHi)*0.92,int(massHi)*1.08)
          #mzg.setRange('fitRegion2',int(massHi)-15,int(massHi)+15)
        sigNameHi = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massHi)+narrow])
        #print sigNameHi
        sig_ds_Hi = myWs.data(sigNameHi)
        #sig_ds_Hi.Print()
        #sig_ds_Hi = RooDataHist('dh'+sigNameHi[2:],'dh'+sigNameHi[2:],RooArgSet(mzg),sig_ds_Hi)

        fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(massHi))
        #SigFit_Hi,tempParams = fitBuilder.Build(sigFit, piece = 'Hi',
        #    mean = massHi, sigmaG = startingVals[2], sigmaCB = startingVals[3],
        #    alpha = startingVals[4], n = startingVals[5], frac=startingVals[6])
        if highMass and narrow == '':
          SigFit_Hi = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, sigmaG = massHi*0.08, sigmaCB = massHi*0.03)[0]
        elif suffix == '09-3-14_Proper' and cat == '5' and lep == 'el':
          SigFit_Hi,tempParams = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, meanGLow = massHi*0.95, meanGHigh = massHi*1.05, meanCBLow = massHi*0.95, meanCBHigh = massHi*1.05)
        else:
          SigFit_Hi = fitBuilder.Build(sigFit,piece = 'Hi', mean = massHi)[0]

        SigFit_Hi.fitTo(sig_ds_Hi, RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum))
        raw_input()
        startingVals = [x.getVal() for x in tempParams]
        #for x in tempParams:
        #  print x.GetName(), x.getVal()
        #raw_input()

      ###### interpolate the two mass points
      if highMass:
        massDiff = (massHi - mass)/50.
      else:
        massDiff = (massHi - mass)/5.
      #if mass<=125:
      if mass<=100:
        mzg.setRange('fitRegion_'+massString,115,mass+15)
      elif mass > 160:
        mzg.setRange('fitRegion_'+massString,mass*0.9,mass*1.1)
      else:
        mzg.setRange('fitRegion_'+massString,mass*0.92,mass*1.08)
      beta = RooRealVar('beta','beta', 0.5, 0., 1.)
      if massHi == massLow:
        beta.setVal(1);
      else:
        beta.setVal(massDiff)

      if massDiff != 0.:
        #print 'lol'
        interp_pdf = RooIntegralMorph('interp_pdf', 'interp_pdf', SigFit_Low, SigFit_Hi, mzg, beta)
        #print 'lol'
        #interp_pdf.Print()
        #interp_ds = interp_pdf.generate(RooArgSet(mzg), (sig_ds_Hi.numEntries()+sig_ds_Low.numEntries())/2)
        interp_ds = interp_pdf.generate(RooArgSet(mzg), 10000)
        yieldNum = (sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))
        normList.append(yieldNum)
        yieldName = '_'.join([prod,'hzg','yield',lep,tev,'cat'+cat])
        yieldVar = RooRealVar(yieldName,yieldName,yieldNum)
      else:
        interp_ds = sig_ds_Low
        yieldNum = sig_ds_Low.sumEntries()
        normList.append(yieldNum)
        yieldName = '_'.join([prod,'hzg','yield',lep,tev,'cat'+cat])
        yieldVar = RooRealVar(yieldName,yieldName,yieldNum)

      sigNameInterp = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(mass)+narrow])

      fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(mass))
      if highMass and narrow == '':
        SigFit_Interp,paramList = fitBuilder.Build(sigFit, piece = 'Interp', mean = mass, sigmaG = mass*0.08, sigmaCB = mass*0.03)
      elif suffix == '09-3-14_Proper' and cat == '5' and lep == 'el':
        SigFit_Interp,paramList= fitBuilder.Build(sigFit, piece = 'Interp', mean = mass, meanGLow = mass*0.95, meanGHigh = mass*1.05, meanCBLow = mass*0.95, meanCBHigh = mass*1.05)
      else:
        SigFit_Interp,paramList = fitBuilder.Build(sigFit,piece = 'Interp', mean = mass)

      SigFit_Interp.fitTo(interp_ds, RooFit.Range('fitRegion_'+massString), RooFit.SumW2Error(kTRUE), RooFit.Strategy(1), RooFit.NumCPU(cpuNum))
      raw_input()

      for i,param in enumerate(paramList):
        param.setConstant(True)
        paramHists[i].SetBinContent(paramHists[i].FindBin(mass),param.getVal())
        paramHists[i].SetBinError(paramHists[i].FindBin(mass),param.getError())
      fitList.append(SigFit_Interp)


      getattr(cardDict[lep][tev][cat][str(mass)],'import')(SigFit_Interp)

      getattr(cardDict[lep][tev][cat][str(mass)],'import')(yieldVar)
      cardDict[lep][tev][cat][str(mass)].commitTransaction()

    c = TCanvas("c","c",0,0,500,400)
    c.cd()

    if highMass:
      testFrame = mzg.frame(float(massList[0])*0.9,float(massList[-1])*1.1)
      if narrow == '':
        c.SetLogy()
    else:
      testFrame = mzg.frame(float(massList[0])-15,float(massList[-1])+15)
    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-1]
      #fit.plotOn(testFrame)
      #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
      fit.plotOn(testFrame, RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
      fit.paramOn(testFrame)
    for i,signal in enumerate(dsList):
      signal.plotOn(testFrame, RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(80))
    if highMass: testFrame.SetMinimum(0.0005)
    testFrame.GetXaxis().SetTitle('m_{H} (GeV)')
    testFrame.GetYaxis().SetTitle('Normalized Yield')
    testFrame.GetYaxis().CenterTitle()
    testFrame.SetTitle('Interpolation Fits')
    testFrame.Draw()
    c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalFits/'+'_'.join(['OLDtest','sig','fit',sigFit,suffix,prod,lep,tev,'cat'+cat])+'.pdf')

    c.SetLogy(False)

    for hist in paramHists:
      hist.SetTitle(hist.GetName())
      hist.Draw('EP')
      c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalParams/'+'_'.join(['OLDtest',hist.GetName(),sigFit,suffix,prod,lep,tev,'cat'+cat])+'.pdf')


    if highMass:
      testFrame = mzg.frame(float(testPoint)*0.9, float(testPoint)*1.1)
    else:
      testFrame = mzg.frame(float(testPoint)-15, float(testPoint)+15)

    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-2]
      #fit.plotOn(testFrame)
      #fit.plotOn(testFrame, RooFit.NormRange('fitRegion_'+regionName))
      if regionName == testPoint:
        fit.plotOn(testFrame, RooFit.Name('model'),RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
        #fit.plotOn(testFrame)
        #fit.paramOn(testFrame,RooFit.ShowConstants(True),RooFit.Format("NEU",RooFit.FixedPrecision(5)))
        #testFrame.getAttText().SetTextSize(0.027)

    if float(testPoint)%5==0:
      for i,signal in enumerate(dsList):
        regionName = signal.GetName().split('_')[-1].rstrip('Narrow')
        if regionName == 'M'+testPoint[0:3]:
          signal.plotOn(testFrame, RooFit.Name('data'),RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(600))
      testFrame.Draw()

      ndof = 0
      if sigFit == 'TripG': ndof = 8
      else: ndof = 7
      chi2 = testFrame.chiSquare('model','data',ndof)
      txt = TText(0,0,'chi2/ndof: '+'{0:.3f}'.format(chi2))
      txt.SetNDC()
      txt.SetX(0.3)
      txt.SetY(0.2)
      txt.SetTextSize(0.04)
      testFrame.addObject(txt)
    testFrame.GetXaxis().SetTitle('m_{H} (GeV)')
    testFrame.GetYaxis().SetTitle('Normalized Yield')
    testFrame.GetYaxis().CenterTitle()
    testFrame.SetTitle('Fit for M'+testPoint)
    testFrame.Draw()
    c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalFits/'+'_'.join(['OLDtest','sig','fit',sigFit,'M'+testPoint,suffix,prod,lep,tev,'cat'+cat])+'.pdf')


  for prod in sigNameList:
    for mass in massList:
      fitBuilder = FitBuilder(mzg,tev,lep,cat,sig=prod,mass=mass)

      fitBuilder.SignalNameParamFixer(cardDict[lep][tev][cat][mass],sigFit)


     # if sigFit == 'TripG':
     #   #print 'nofix'
     #   SignalNameParamFixerTripGV2(tev,lep,cat,prod,mass,cardDict[lep][tev][cat][mass])
     # else:
     #   SignalNameParamFixerCBG(tev,lep,cat,prod,mass,cardDict[lep][tev][cat][mass])

  for mass in massList:
    fileName = '_'.join(['SignalOutput',lep,tev,'cat'+cat,mass])
    if not os.path.isdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass): os.mkdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass)
    cardDict[lep][tev][cat][mass].writeToFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'+fileName+'.root')


#signal = myWs.data('ds_sig_gg_el_2012_cat4_M125')
#SigFit = BuildCrystalBallGauss('2012','el','4','gg','125',mzg)
#SigFit.fitTo(signal, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))
#SigFit.fitTo(signal, RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1))

if __name__=="__main__":
  args = getArgs()
  SignalFitMaker(args.lepton, args.tev, str(args.cat), args.suffix, args.cores)
  '''
  print len(sys.argv)
  print sys.argv
  if len(sys.argv) == 1:
    SignalFitMaker(cfl.leptonList[0], cfl.tevList[0], cfl.catListSmall[0], cfl.suffix, True)
  elif len(sys.argv) == 6:
    SignalFitMaker(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))
  else:
    print 'usage: ./signalCBFits lepton tev cat suffix batch'
  '''

