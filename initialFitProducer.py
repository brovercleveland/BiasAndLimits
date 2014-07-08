#!/usr/bin/env python
import sys
sys.argv.append('-b')
import numpy as np
#import pdb
from signalCBFits import AutoVivification
from rooFitBuilder import *
from xsWeighterNew import *
from ROOT import *
import os
import configLimits as cfl

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

debugPlots = cfl.debugPlots

verbose = cfl.verbose

rootrace = cfl.rootrace

doMVA = cfl.doMVA

allBiasFits= cfl.allBiasFits# Turn on extra fits used in bias studies

suffix = cfl.suffix

YR = cfl.YR

sigFit = cfl.sigFit



# OK listen, we're gunna need to do some bullshit just to get a uniform RooRealVar name for our data objects.
# Because I named branches different than the trees, there's a lot of tree loops here
# So we'll loop through the Branch, set mzg to the event value (if it's in range), and add that to our RooDataSet.
# This way, we make a RooDataSet that uses our 'CMS_hzg_mass' variable.

TH1.SetDefaultSumw2(kTRUE)
if rootrace: RooTrace.active(kTRUE)
def doInitialFits():
  print 'loading up the files'

  dataDict = {'mu2012_4cat':TFile('inputFiles/m_llgFile_MuMu2012ABCD_'+suffix+'.root','r'),'el2012_4cat':TFile('inputFiles/m_llgFile_EE2012ABCD_'+suffix+'.root','r'),'mu2011_4cat':TFile('inputFiles/m_llgFile_MuMu2011ABCD_Proper.root','r'),'el2011_4cat':TFile('inputFiles/m_llgFile_EE2011ABCD_Proper.root','r'),'all2011_4cat':TFile('inputFiles/m_llgFile_All2011ABCD_Proper.root','r')}

  signalDict = dataDict

  leptonList = cfl.leptonList
  yearList = cfl.yearList
  catListBig = cfl.catListBig
  catListSmall = cfl.catListSmall
  massList = cfl.massList
  sigNameListInput = cfl.sigNameListInput
  sigNameListOutput = cfl.sigNameList

  yearToTeV = {'2011':'7TeV','2012':'8TeV'}

  weight  = RooRealVar('Weight','Weight',0,100)
  mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',100,190)
  mzg.setRange('fullRegion',100,190)
  mzg.setRange('oldRegion',115,190)
  mzg.setRange('MERegion',108,160)
  #mzg.setBins(360,'cache')
  mzg.setBins(360)

  c = TCanvas("c","c",0,0,500,400)
  c.cd()

  ws =RooWorkspace("ws")

####################################
# start loop over all year/lep/cat #
####################################

  for year in yearList:
    for lepton in leptonList:
      if doMVA and year == '2012': catList = catListBig
      else: catList = catListSmall
      for cat in catList:
        if year is '2011' and cat is '5' and lepton is 'el': lepton = 'all'
        elif year is '2011' and cat is '5' and lepton is 'mu': continue
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

        for j,prod in enumerate(sigNameListOutput):
          signalListDS = []
          for mass in massList:
          # store the unbinned signals for CB fitting
            print 'm_llg_Signal'+year+sigNameListInput[j]+'M'+mass
            signalTree = signalDict[lepton+year+'_4cat'].Get('m_llg_Signal'+year+sigNameListInput[j]+'M'+mass)
            sigName = '_'.join(['ds',prod,'hzg',lepton,yearToTeV[year],'cat'+cat,'M'+mass])
            tmpSigMass= np.zeros(1,dtype = 'd')
            tmpSigWeight= np.zeros(1,dtype = 'd')
            tmpSigNumEvents = 0
            if cat is '0':
              signalTree.SetBranchAddress('m_llg_Signal'+year+sigNameListInput[j]+'M'+mass,tmpSigMass)
            else:
              signalTree.SetBranchAddress('m_llgCAT'+cat+'_Signal'+year+sigNameListInput[j]+'M'+mass,tmpSigMass)
            signalTree.SetBranchAddress('unBinnedWeight_Signal'+year+sigNameListInput[j]+'M'+mass,tmpSigWeight)
            tmpSigNumEvents = signalDict[lepton+year+'_4cat'].Get('unskimmedEventsTotal_Signal'+year+sigNameListInput[j]+'M'+mass).GetBinContent(1)
            sig_argSW = RooArgSet(mzg,weight)
            sig_ds = RooDataSet(sigName,sigName,sig_argSW,'Weight')
            for i in range(0,signalTree.GetEntries()):
              signalTree.GetEntry(i)
              if tmpSigMass[0]> int(mass)-10 and tmpSigMass[0]<int(mass)+10:
                if year is '2012' and mass is '160' and prod == 'ggH' and suffix == 'Proper':
                  mzg.setVal(tmpSigMass[0]+5)
                else:
                  mzg.setVal(tmpSigMass[0])

                if prod == 'WH' and (suffix == 'Proper' or year == '2011'):
                  sigWeight = LumiXSWeighter(year,lepton,prod,mass,tmpSigNumEvents*0.655,YR)
                elif prod == 'ZH' and (suffix == 'Proper' or year == '2011'):
                  sigWeight = LumiXSWeighter(year,lepton,prod,mass,tmpSigNumEvents*0.345,YR)
                elif prod in ['WH','ZH','ttH'] and suffix != 'Proper' and year == '2012':
                  sigWeight = LumiXSWeighter(year,lepton,prod,mass,tmpSigNumEvents,YR,alt=True)
                else:
                  sigWeight = LumiXSWeighter(year,lepton,prod,mass,tmpSigNumEvents,YR)

                #if i == 0:
                #  print year,lepton,prod,mass
                #  print sigWeight
                #  print
                #  raw_input()
                #if prod == 'ggH' and year == '2012' and mass == '125' and lepton == 'mu':
                #  print sigWeight
                #  raw_input()

                sigWeight = tmpSigWeight[0]*sigWeight
                sig_ds.add(sig_argSW, sigWeight)
                #sig_argSW.Print()

            signalListDS.append(sig_ds)
            getattr(ws,'import')(signalListDS[-1])
            signalTree.ResetBranchAddresses()
# do some histogramming for gg signal for bias study
# we don't need or use unbinned signal or complicated fits
# but this is mostly for compatibility, we may change to unbinned
# during a future iteration
            if prod == 'ggH':
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

              if year is '2012' and mass is '160' and suffix == 'Proper':
                if cat is '0':
                  signalTree.Draw('m_llg_Signal'+year+'ggM'+mass+'+5.0>>'+histName,'unBinnedWeight_Signal'+year+'ggM'+mass)
                else:
                  signalTree.Draw('m_llgCAT'+cat+'_Signal'+year+'ggM'+mass+'+5.0>>'+histName,'unBinnedWeight_Signal'+year+'ggM'+mass)
              else:
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

            '''
            if debugPlots and prod is 'gg':
              testFrame = mzg.frame()
              for i,signal in enumerate(signalListPDF):
                signalListDH[i].plotOn(testFrame)
                signal.plotOn(testFrame)
              testFrame.Draw()
              c.Print('debugPlots/'+'_'.join(['test','signals',suffix,year,lepton,'cat'+cat])+'.pdf')
            if debugPlots:
              testFrame = mzg.frame()
              for signal in signalListDS:
                signal.plotOn(testFrame, RooFit.DrawOption('pl'))
              testFrame.Draw()
              c.Print('debugPlots/'+'_'.join(['test','ds','sig',suffix,prod,year,lepton,'cat'+cat])+'.pdf')
            '''
            del signalTree


################
# get the data #
################
        if verbose: print 'starting data section'


        dataName = '_'.join(['data',lepton,yearToTeV[year],'cat'+cat])
        dataTree = dataDict[lepton+year+'_4cat'].Get('m_llg_DATA')
        #tmpMassEventOld = np.zeros(1,dtype = 'f')
        tmpMassEventOld = np.zeros(1,dtype = 'd')
        if cat is '0':
          dataTree.SetBranchAddress('m_llg_DATA',tmpMassEventOld)
        else:
          dataTree.SetBranchAddress('m_llgCAT'+cat+'_DATA',tmpMassEventOld)
        data_argS = RooArgSet(mzg)
        if cat == '5':
          data_ds = RooDataSet(dataName,dataName,data_argS)
        else:
          data_ds = RooDataHist(dataName,dataName,data_argS)
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
        '''
        if debugPlots:
          testFrame = mzg.frame()
          data_ds.plotOn(testFrame,RooFit.Binning(45))
          testFrame.Draw()
          c.Print('debugPlots/'+'_'.join(['test','data',year,lepton,'cat'+cat])+'.pdf')
        '''
        getattr(ws,'import')(data_ds)



#############
# make fits #
#############
        if verbose: 'starting fits'

        if cat is not '5':
          GaussExp = BuildGaussExp(yearToTeV[year], lepton, cat, mzg)
          #if lepton == 'mu': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg, sigma = 5, beta = 5)
          #if lepton == 'mu' and cat == '1': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg, alpha = 116)
          #elif lepton == 'mu': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg)
          #elif lepton == 'el' and cat == '3' and yearToTeV[year] == '2011': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg, alpha = 116)
          #elif lepton == 'el' and cat in ['0','4'] and yearToTeV[year] == '2012': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg, sigma =5, beta = 5)
          #elif lepton == 'mu' and cat == '3' and yearToTeV[year] == '2012': GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg,sigma = 2, beta = 6,alpha = 105)
          GaussPow = BuildGaussPow(yearToTeV[year], lepton, cat, mzg, sigma = 2, beta = 6,alpha = 105)
          SechExp = BuildSechExp(yearToTeV[year], lepton, cat, mzg)
          SechPow = BuildSechPow(yearToTeV[year], lepton, cat, mzg)
          #GaussBern3 = BuildGaussStepBern3(yearToTeV[year], lepton, cat, mzg)
          GaussBern3 = BuildGaussStepBern3(yearToTeV[year], lepton, cat, mzg, step = 117, sigma = 3)
          GaussBern4 = BuildGaussStepBern4(yearToTeV[year], lepton, cat, mzg)
          GaussBern5 = BuildGaussStepBern5(yearToTeV[year], lepton, cat, mzg)
          GaussBern6 = BuildGaussStepBern6(yearToTeV[year], lepton, cat, mzg)
          #GaussBern4 = BuildGaussStepBern4(yearToTeV[year], lepton, cat, mzg, step = 105, stepLow = 100, stepHigh = 150, sigma = 2.5)
          #GaussBern5 = BuildGaussStepBern5(yearToTeV[year], lepton, cat, mzg, step = 105, stepLow = 100, stepHigh = 150, sigma = 2.5)
          #GaussBern6 = BuildGaussStepBern6(yearToTeV[year], lepton, cat, mzg, step = 105, stepLow = 100, stepHigh = 150, sigma = 2.5)
          #SechBern3 = BuildSechStepBern3(yearToTeV[year], lepton, cat, mzg)
          SechBern3 = BuildSechStepBern3(yearToTeV[year], lepton, cat, mzg, sigma = 10)
          if lepton == 'mu' and cat == '3': SechBern4 = BuildSechStepBern4(yearToTeV[year], lepton, cat, mzg,sigma=2)
          else: SechBern4 = BuildSechStepBern4(yearToTeV[year], lepton, cat, mzg)
          if lepton == 'mu' and cat == '3': SechBern5 = BuildSechStepBern5(yearToTeV[year], lepton, cat, mzg,sigma=2)
          else: SechBern5 = BuildSechStepBern5(yearToTeV[year], lepton, cat, mzg)

          gauss = BuildRooGaussian(yearToTeV[year], lepton, cat, mzg)
          BetaFunc = BuildBetaFunc(yearToTeV[year], lepton, cat, mzg, 'MERegion')
          Kumaraswamy = BuildKumaraswamy(yearToTeV[year], lepton, cat, mzg, 'MERegion')
          Bern5 = BuildBern5(yearToTeV[year], lepton, cat, mzg)
          BB = BuildBetaAndBern(yearToTeV[year], lepton, cat, mzg, 'MERegion')
          GB = BuildGaussAndBern(yearToTeV[year], lepton, cat, mzg, 'MERegion')

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

          if allBiasFits:
            GaussExp.fitTo(data_ds,RooFit.Range('fullRegion'))
            GaussPow.fitTo(data_ds,RooFit.Range('fullRegion'))
            SechExp.fitTo(data_ds,RooFit.Range('fullRegion'))
            SechPow.fitTo(data_ds,RooFit.Range('fullRegion'))
            GaussBern3.fitTo(data_ds,RooFit.Range('fullRegion'))
            GaussBern4.fitTo(data_ds,RooFit.Range('fullRegion'))
            GaussBern5.fitTo(data_ds,RooFit.Range('fullRegion'))
            #GaussBern4.fitTo(data_ds,RooFit.Range('MERegion'), RooFit.Strategy(1))
            #GaussBern5.fitTo(data_ds,RooFit.Range('MERegion'), RooFit.Strategy(1))
            #GaussBern6.fitTo(data_ds,RooFit.Range('MERegion'), RooFit.Strategy(1))
            #GaussBern6.fitTo(data_ds,RooFit.Range('fullRegion'))
            SechBern3.fitTo(data_ds,RooFit.Range('fullRegion'))
            SechBern4.fitTo(data_ds,RooFit.Range('fullRegion'))
            SechBern5.fitTo(data_ds,RooFit.Range('fullRegion'))
            #gauss.fitTo(data_ds,RooFit.Range('MERegion'))
            #BetaFunc.fitTo(data_ds,RooFit.Range('MERegion'))
            #Kumaraswamy.fitTo(data_ds,RooFit.Range('MERegion'))
            #Bern5.fitTo(data_ds,RooFit.Range('MERegion'))
            #BB.fitTo(data_ds,RooFit.Range('MERegion'))
            #GB.fitTo(data_ds,RooFit.Range('MERegion'))
          else:
            # only do the limit fits
            if cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
              GaussBern4.fitTo(data_ds,RooFit.Range('fullRegion'))
            else:
              GaussBern5.fitTo(data_ds,RooFit.Range('fullRegion'))

          if debugPlots:
            leg  = TLegend(0.7,0.7,1.0,1.0)
            leg.SetFillColor(0)
            leg.SetShadowColor(0)
            leg.SetBorderSize(1)
            leg.SetHeader('_'.join(['test','fits',year,lepton,'cat'+cat]))
            testFrame = mzg.frame()
            data_ds.plotOn(testFrame,RooFit.Binning(45))
            #data_ds.plotOn(testFrame)
            if allBiasFits:
              GaussExp.plotOn(testFrame,RooFit.Name('GaussExp'))
              GaussPow.plotOn(testFrame,RooFit.LineColor(kCyan),RooFit.Name('GaussPow'))
              SechExp.plotOn(testFrame,RooFit.LineColor(kRed),RooFit.Name('SechExp'))
              SechPow.plotOn(testFrame,RooFit.LineColor(kYellow),RooFit.Name('SechPow'))
              GaussBern3.plotOn(testFrame,RooFit.LineColor(kViolet),RooFit.Name('GaussBern3'))
              GaussBern4.plotOn(testFrame,RooFit.LineColor(kPink),RooFit.Name('GaussBern4'))
              GaussBern5.plotOn(testFrame,RooFit.LineColor(kGray),RooFit.Name('GaussBern5'))
              #GaussBern6.plotOn(testFrame,RooFit.LineColor(kGreen+2))
              SechBern3.plotOn(testFrame,RooFit.LineColor(kMagenta),RooFit.Name('SechBern3'))
              SechBern4.plotOn(testFrame,RooFit.LineColor(kBlack),RooFit.Name('SechBern4'))
              SechBern5.plotOn(testFrame,RooFit.LineColor(kGreen),RooFit.Name('SechBern5'))
              #gauss.plotOn(testFrame,RooFit.LineColor(kBlue), RooFit.Name('Gauss'))
              #BetaFunc.plotOn(testFrame,RooFit.LineColor(kBlack), RooFit.Name('Beta'))
              #Kumaraswamy.plotOn(testFrame,RooFit.LineColor(kCyan), RooFit.Name('Kumaraswamy'))
              #Bern5.plotOn(testFrame,RooFit.LineColor(kRed), RooFit.Name('Bern5'))
              #BB.plotOn(testFrame,RooFit.LineColor(kViolet), RooFit.Name('Beta+Bern4'))
              #GB.plotOn(testFrame,RooFit.LineColor(kGreen), RooFit.Name('Gauss+Bern3'))
            else:
              # only do the limit fits
              if cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
                GaussBern4.plotOn(testFrame,RooFit.LineColor(kPink),RooFit.Name('GaussBern4'))
              else:
                GaussBern5.plotOn(testFrame,RooFit.LineColor(kGray),RooFit.Name('GaussBern5'))
            testFrame.Draw()
            if allBiasFits:
              #leg.AddEntry(testFrame.findObject('Beta'),'Beta','l')
              #leg.AddEntry(testFrame.findObject('Kumaraswamy'),'Kumaraswamy','l')
              #leg.AddEntry(testFrame.findObject('Bern5'),'Bern5','l')
              #leg.AddEntry(testFrame.findObject('Beta+Bern4'),'Beta+Bern4','l')
              #leg.AddEntry(testFrame.findObject('Gauss'),'Gauss','l')
              #leg.AddEntry(testFrame.findObject('Gauss+Bern3'),'Gauss+Bern3','l')
              leg.AddEntry(testFrame.findObject('GaussExp'),'GaussExp','l')
              leg.AddEntry(testFrame.findObject('GaussPow'),'GaussPow','l')
              leg.AddEntry(testFrame.findObject('SechExp'),'SechExp','l')
              leg.AddEntry(testFrame.findObject('SechPow'),'SechPow','l')
              leg.AddEntry(testFrame.findObject('GaussBern3'),'GaussBern3','l')
              leg.AddEntry(testFrame.findObject('GaussBern4'),'GaussBern4','l')
              leg.AddEntry(testFrame.findObject('GaussBern5'),'GaussBern5','l')
              leg.AddEntry(testFrame.findObject('SechBern3'),'SechBern3','l')
              leg.AddEntry(testFrame.findObject('SechBern4'),'SechBern4','l')
              leg.AddEntry(testFrame.findObject('SechBern5'),'SechBern5','l')
            else:
              # only do the limit fits
              if cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
                leg.AddEntry(testFrame.findObject('GaussBern4'),'GaussBern4','l')
              else:
                leg.AddEntry(testFrame.findObject('GaussBern5'),'GaussBern5','l')
            leg.Draw()
            c.Print('debugPlots/'+'_'.join(['test','fits',suffix,year,lepton,'cat'+cat])+'.pdf')

          #raw_input()
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

        else:
          Exp = BuildExp(yearToTeV[year], lepton, cat, mzg)
          Pow = BuildPow(yearToTeV[year], lepton, cat, mzg)
          Bern2 = BuildBern2(yearToTeV[year], lepton, cat, mzg)
          Bern3 = BuildBern3(yearToTeV[year], lepton, cat, mzg)
          Bern4 = BuildBern4(yearToTeV[year], lepton, cat, mzg)

          if verbose:
            Exp.Print()
            Pow.Print()
            Bern2.Print()
            Bern3.Print()
            Bern4.Print()

          if allBiasFits:
            Exp.fitTo(data_ds,RooFit.Range('fullRegion'))
            Pow.fitTo(data_ds,RooFit.Range('fullRegion'))
            Bern2.fitTo(data_ds,RooFit.Range('fullRegion'))
            Bern3.fitTo(data_ds,RooFit.Range('fullRegion'))
            Bern4.fitTo(data_ds,RooFit.Range('fullRegion'))
          else:
            Bern3.fitTo(data_ds,RooFit.Range('fullRegion'))

          if debugPlots:
            testFrame = mzg.frame()
            data_ds.plotOn(testFrame,RooFit.Binning(45))
            if allBiasFits:
              Exp.plotOn(testFrame)
              Pow.plotOn(testFrame,RooFit.LineColor(kCyan))
              Bern2.plotOn(testFrame,RooFit.LineColor(kViolet))
              Bern3.plotOn(testFrame,RooFit.LineColor(kPink))
              Bern4.plotOn(testFrame,RooFit.LineColor(kGray))
            else:
              Bern3.plotOn(testFrame,RooFit.LineColor(kPink))
            testFrame.Draw()
            c.Print('debugPlots/'+'_'.join(['test','fits',suffix,year,lepton,'cat'+cat])+'.pdf')

          getattr(ws,'import')(Exp)
          getattr(ws,'import')(Pow)
          getattr(ws,'import')(Bern2)
          getattr(ws,'import')(Bern3)
          getattr(ws,'import')(Bern4)
        ws.commitTransaction()
        print 'commited'
  if not os.path.isdir('outputDir/'+suffix+'_'+YR+'_'+sigFit): os.mkdir('outputDir/'+suffix+'_'+YR+'_'+sigFit)
  print 'writing'
  ws.writeToFile('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix.rstrip('_Cut')+'.root')
  #ws.writeToFile('wtf.root')


  print 'we did it!'



if __name__=="__main__":
  doInitialFits()
