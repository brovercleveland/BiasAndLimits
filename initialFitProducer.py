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

debugPlots = True
verbose = False
rootrace = False
do4Cat = True
doVBF = False

# OK listen, we're gunna need to do some bullshit just to get a uniform RooRealVar name for our data objects.
# Because I named branches different than the trees, there's a lot of tree loops here
# So we'll loop through the Branch, set mzg to the event value (if it's in range), and add that to our RooDataSet.
# This way, we make a RooDataSet that uses our 'CMS_hzg_mass' variable.

TH1.SetDefaultSumw2(kTRUE)
if rootrace: RooTrace.active(kTRUE)
def doInitialFits():
  print 'loading up the files'

  dataDict = {'mu2012_4cat':TFile('inputFiles/data_Mu2012.root','r'),'el2012_4cat':TFile('inputFiles/data_El2012.root','r'),'mu2011_4cat':TFile('inputFiles/data_Mu2011.root','r'),'el2011_4cat':TFile('inputFiles/data_El2011.root','r')}
  signalDict = {'mu2012_4cat':TFile('inputFiles/signal_Mu2012_hi.root','r'),'el2012_4cat':TFile('inputFiles/signal_El2012_hi.root','r'),'mu2011_4cat':TFile('inputFiles/signal_Mu2011.root','r'),'el2011_4cat':TFile('inputFiles/signal_El2011.root','r')}

  '''
  leptonList = ['mu','el']
  yearList = ['2011','2012']
  catList = ['1','2','3','4']
  massList = ['120','125','130','135','140','145','150']
  sigNameList = ['gg','vbf','tth','wh','zh']
  '''

  leptonList = ['mu','el']
  yearList = ['2012']
  catList = ['0']
  massList = ['120','125','130','135','140','145','150','155','160']
  sigNameList = ['gg']

  weight  = RooRealVar('Weight','Weight',0,100)
  mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',100,190)
  mzg.setRange('fullRegion',100,190)
  mzg.setRange('oldRegion',115,190)
  mzg.setBins(50000,'cache')

  c = TCanvas("c","c",0,0,500,400)
  c.cd()

  ws =RooWorkspace("ws")

####################################
# start loop over all year/lep/cat #
####################################

  for year in yearList:
    for lepton in leptonList:
      for cat in catList:
        if rootrace:
          RooTrace.dump()
          raw_input()
        signalList = []
        signalListDH = []
        signalListPDF = []
        if verbose: print 'top of loop',year,lepton,cat

###################################################
# set up the signal histograms and the mzg ranges #
###################################################

        for prod in sigNameList:
          signalListDS = []
          for mass in massList:
          # store the unbinned signals for CB fitting
            signalTree = signalDict[lepton+year+'_4cat'].Get('m_llg_Signal'+year+prod+'M'+mass)
            sigName = '_'.join(['ds_sig',prod,lepton,year,'cat'+cat,'M'+mass])
            tmpSigMass= np.zeros(1,dtype = 'f')
            tmpSigWeight= np.zeros(1,dtype = 'f')
            tmpSigLumiXS= np.zeros(1,dtype = 'f')
            if cat is '0':
              signalTree.SetBranchAddress('m_llg_Signal'+year+prod+'M'+mass,tmpSigMass)
            else:
              signalTree.SetBranchAddress('m_llgCAT'+cat+'_Signal'+year+prod+'M'+mass,tmpSigMass)
            signalTree.SetBranchAddress('unBinnedWeight_Signal'+year+prod+'M'+mass,tmpSigWeight)
            signalTree.SetBranchAddress('unBinnedLumiXS_Signal'+year+prod+'M'+mass,tmpSigLumiXS)
            sig_argSW = RooArgSet(mzg,weight)
            sig_ds = RooDataSet(sigName,sigName,sig_argSW,'Weight')
            for i in range(0,signalTree.GetEntries()):
              signalTree.GetEntry(i)
              if tmpSigMass[0]> 100 and tmpSigMass[0]<190:
                mzg.setVal(tmpSigMass[0])
                if prod in ['wh','zh']:
                  sigWeight = tmpSigWeight[0]*tmpSigLumiXS[0]*(1/0.100974)
                else:
                  sigWeight = tmpSigWeight[0]*tmpSigLumiXS[0]
                sig_ds.add(sig_argSW, sigWeight)
                #sig_argSW.Print()

            signalListDS.append(sig_ds)
            getattr(ws,'import')(signalListDS[-1])
            signalTree.ResetBranchAddresses()
# do some histogramming for gg signal for bias study
# we don't need or use unbinned signal or complicated fits
# but this is mostly for compatibility, we may change to unbinned
# during a future iteration
            if prod is 'gg':
              if verbose: print 'signal mass loop', mass
              histName = '_'.join(['sig',lepton,year,'cat'+cat,'M'+mass])
              rangeName = '_'.join(['range',lepton,year,'cat'+cat,'M'+mass])

              signalList.append(TH1F(histName, histName, 90, 100, 190))
              signalList[-1].SetLineColor(kRed)
              signalTree = signalDict[lepton+year+'_4cat'].Get('m_llg_Signal'+year+'ggM'+mass)

              if verbose:
                print histName
                signalTree.Print()
                print

              if cat is '0':
                signalTree.Draw('m_llg_Signal'+year+'ggM'+mass+'>>'+histName,'unBinnedWeight_Signal'+year+'ggM'+mass)
              else:
                signalTree.Draw('m_llgCAT'+cat+'_Signal'+year+'ggM'+mass+'>>'+histName,'unBinnedWeight_Signal'+year+'ggM'+mass)
              signalList[-1].Scale(1/signalList[-1].Integral())
              signalList[-1].Smooth(2)

              # range is +/- 1 RMS centered around signal peak
              rangeLow = signalList[-1].GetMean()-1.0*signalList[-1].GetRMS()
              rangeHi = signalList[-1].GetMean()+1.0*signalList[-1].GetRMS()
              mzg.setRange(rangeName,rangeLow,rangeHi)

              mzg_argL = RooArgList(mzg)
              mzg_argS = RooArgSet(mzg)
              signalListDH.append(RooDataHist('dh_'+histName,'dh_'+histName,mzg_argL,signalList[-1]))
              signalListPDF.append(RooHistPdf('pdf_'+histName,'pdf_'+histName,mzg_argS,signalListDH[-1],2))
              getattr(ws,'import')(signalListPDF[-1])
              if verbose: print 'finshed one mass', mass

            if debugPlots and prod is 'gg':
              testFrame = mzg.frame()
              for i,signal in enumerate(signalListPDF):
                signalListDH[i].plotOn(testFrame)
                signal.plotOn(testFrame)
              testFrame.Draw()
              c.Print('debugPlots/'+'_'.join(['test','signals',year,lepton,'cat'+cat])+'.pdf')
            if debugPlots:
              testFrame = mzg.frame()
              for signal in signalListDS:
                signal.plotOn(testFrame)
              testFrame.Draw()
              c.Print('debugPlots/'+'_'.join(['test','ds','sig',prod,year,lepton,'cat'+cat])+'.pdf')
            del signalTree


################
# get the data #
################
        if verbose: print 'starting data section'

        dataName = '_'.join(['data',lepton,year,'cat'+cat])
        dataTree = dataDict[lepton+year+'_4cat'].Get('m_llg_DATA')
        tmpMassEventOld = np.zeros(1,dtype = float)
        if cat is '0':
          dataTree.SetBranchAddress('m_llg_DATA',tmpMassEventOld)
        else:
          dataTree.SetBranchAddress('m_llgCAT'+cat+'_DATA',tmpMassEventOld)
        data_argS = RooArgSet(mzg)
        data_ds = RooDataSet(dataName,dataName,data_argS)
        for i in range(0,dataTree.GetEntries()):
          dataTree.GetEntry(i)
          if tmpMassEventOld[0]> 100 and tmpMassEventOld[0]<190:
            mzg.setVal(tmpMassEventOld[0])
            data_ds.add(data_argS)
        dataTree.ResetBranchAddresses()

        if verbose:
          print dataName
          data_ds.Print()
          print
        if debugPlots:
          testFrame = mzg.frame()
          data_ds.plotOn(testFrame)
          testFrame.Draw()
          c.Print('debugPlots/'+'_'.join(['test','data',year,lepton,'cat'+cat])+'.pdf')
        getattr(ws,'import')(data_ds)



#############
# make fits #
#############
        if verbose: 'starting fits'

        GaussExp = BuildGaussExp(year, lepton, cat, mzg)
        if lepton == 'mu': GaussPow = BuildGaussPow(year, lepton, cat, mzg, sigma = 5, beta = 5)
        elif lepton == 'el' and cat == '3' and year == '2011': GaussPow = BuildGaussPow(year, lepton, cat, mzg, alpha = 116)
        elif lepton == 'el' and cat == '0' and year == '2012': GaussPow = BuildGaussPow(year, lepton, cat, mzg, sigma =5, beta = 5)
        else: GaussPow = BuildGaussPow(year, lepton, cat, mzg)
        SechExp = BuildSechExp(year, lepton, cat, mzg)
        SechPow = BuildSechPow(year, lepton, cat, mzg)
        GaussBern3 = BuildGaussStepBern3(year, lepton, cat, mzg)
        GaussBern4 = BuildGaussStepBern4(year, lepton, cat, mzg)
        GaussBern5 = BuildGaussStepBern5(year, lepton, cat, mzg)
        GaussBern6 = BuildGaussStepBern6(year, lepton, cat, mzg)
        SechBern3 = BuildSechStepBern3(year, lepton, cat, mzg)
        if lepton == 'mu' and cat == '3': SechBern4 = BuildSechStepBern4(year, lepton, cat, mzg,sigma=2)
        else: SechBern4 = BuildSechStepBern4(year, lepton, cat, mzg)
        if lepton == 'mu' and cat == '3': SechBern5 = BuildSechStepBern5(year, lepton, cat, mzg,sigma=2)
        else: SechBern5 = BuildSechStepBern5(year, lepton, cat, mzg)

        if verbose:
          GaussExp.Print()
          GaussPow.Print()
          SechExp.Print()
          SechPow.Print()
          GaussBern3.Print()
          GaussBern4.Print()
          GaussBern5.Print()
          GaussBern6.Print()
          SechBern3.Print()
          SechBern4.Print()
          SechBern5.Print()

        GaussExp.fitTo(data_ds,RooFit.Range('fullRegion'))
        GaussPow.fitTo(data_ds,RooFit.Range('fullRegion'))
        SechExp.fitTo(data_ds,RooFit.Range('fullRegion'))
        SechPow.fitTo(data_ds,RooFit.Range('fullRegion'))
        GaussBern3.fitTo(data_ds,RooFit.Range('fullRegion'))
        GaussBern4.fitTo(data_ds,RooFit.Range('fullRegion'))
        GaussBern5.fitTo(data_ds,RooFit.Range('fullRegion'))
        GaussBern6.fitTo(data_ds,RooFit.Range('fullRegion'))
        SechBern3.fitTo(data_ds,RooFit.Range('fullRegion'))
        SechBern4.fitTo(data_ds,RooFit.Range('fullRegion'))
        SechBern5.fitTo(data_ds,RooFit.Range('fullRegion'))

        if debugPlots:
          testFrame = mzg.frame()
          data_ds.plotOn(testFrame)
          GaussExp.plotOn(testFrame)
          GaussPow.plotOn(testFrame,RooFit.LineColor(kCyan))
          SechExp.plotOn(testFrame,RooFit.LineColor(kRed))
          SechPow.plotOn(testFrame,RooFit.LineColor(kYellow))
          GaussBern3.plotOn(testFrame,RooFit.LineColor(kViolet))
          GaussBern4.plotOn(testFrame,RooFit.LineColor(kPink))
          GaussBern5.plotOn(testFrame,RooFit.LineColor(kGray))
          GaussBern6.plotOn(testFrame,RooFit.LineColor(kGreen+2))
          SechBern3.plotOn(testFrame,RooFit.LineColor(kMagenta))
          SechBern4.plotOn(testFrame,RooFit.LineColor(kBlack))
          SechBern5.plotOn(testFrame,RooFit.LineColor(kGreen))
          testFrame.Draw()
          c.Print('debugPlots/'+'_'.join(['test','fits',year,lepton,'cat'+cat])+'.pdf')

        getattr(ws,'import')(GaussExp)
        getattr(ws,'import')(GaussPow)
        getattr(ws,'import')(SechExp)
        getattr(ws,'import')(SechPow)
        getattr(ws,'import')(GaussBern3)
        getattr(ws,'import')(GaussBern4)
        getattr(ws,'import')(GaussBern5)
        getattr(ws,'import')(GaussBern6)
        getattr(ws,'import')(SechBern3)
        getattr(ws,'import')(SechBern4)
        getattr(ws,'import')(SechBern5)

        ws.commitTransaction()
  ws.writeToFile('testRooFitOut_noCatBias.root')


  print 'we did it!'



if __name__=="__main__":
  doInitialFits()
