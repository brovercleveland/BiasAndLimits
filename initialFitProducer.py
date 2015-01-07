#!/usr/bin/env python
import sys
sys.argv.append('-b')
import numpy as np
#import pdb
from configLimits import AutoVivification
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


YR = cfl.YR

sigFit = cfl.sigFit

highMass = cfl.highMass

blind = cfl.blind



# OK listen, we're gunna need to do some bullshit just to get a uniform RooRealVar name for our data objects.
# Because I named branches different than the trees, there's a lot of tree loops here
# So we'll loop through the Branch, set mzg to the event value (if it's in range), and add that to our RooDataSet.
# This way, we make a RooDataSet that uses our 'CMS_hzg_mass' variable.

TH1.SetDefaultSumw2(kTRUE)
if rootrace: RooTrace.active(kTRUE)
def doInitialFits():
  print 'loading up the files'
  suffix = cfl.suffix

  dataDict = {'mu2012_4cat':TFile('inputFiles/m_llgFile_MuMu2012ABCD_'+suffix+'.root','r'),'el2012_4cat':TFile('inputFiles/m_llgFile_EE2012ABCD_'+suffix+'.root','r'),'mu2011_4cat':TFile('inputFiles/m_llgFile_MuMu2011ABCD_Proper.root','r'),'el2011_4cat':TFile('inputFiles/m_llgFile_EE2011ABCD_Proper.root','r'),'all2011_4cat':TFile('inputFiles/m_llgFile_All2011ABCD_Proper.root','r')}

  signalDict = dataDict
  suffix = cfl.suffixPostFix

  leptonList = cfl.leptonList
  yearList = cfl.yearList
  catListBig = cfl.catListBig
  catListSmall = cfl.catListSmall
  massList = cfl.massList
  sigNameListInput = cfl.sigNameListInput
  sigNameListOutput = cfl.sigNameList

  yearToTeV = {'2011':'7TeV','2012':'8TeV'}

  weight  = RooRealVar('Weight','Weight',0,100)

  xmax = cfl.bgRange[1]
  xmin = cfl.bgRange[0]
  if highMass:
    binning = (xmax-xmin)/4
  else:
    binning = (xmax-xmin)/2

  print 'high!!!!!!!!!!!!!!!!!!'
  mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',xmin,xmax)
  mzg.setRange('full',xmin,xmax)
  mzg.setRange('Blind1',xmin,cfl.blindRange[0])
  mzg.setRange('Blind2',cfl.blindRange[1],xmax)
  mzg.setBins((xmax-xmin)*4)
  mzg.setBins(50000,'cache')

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
            narrow = ''
            if 'Narrow' in suffix: narrow = 'Narrow'
            print 'm_llg_Signal'+year+sigNameListInput[j]+'M'+mass+narrow
            signalTree = signalDict[lepton+year+'_4cat'].Get('m_llg_Signal'+year+sigNameListInput[j]+'M'+mass+narrow)
            sigName = '_'.join(['ds',prod,'hzg',lepton,yearToTeV[year],'cat'+cat,'M'+mass+narrow])
            tmpSigMass= np.zeros(1,dtype = 'd')
            tmpSigWeight= np.zeros(1,dtype = 'd')
            tmpSigNumEvents = 0
            if cat is '0':
              signalTree.SetBranchAddress('m_llg_Signal'+year+sigNameListInput[j]+'M'+mass+narrow,tmpSigMass)
            else:
              signalTree.SetBranchAddress('m_llgCAT'+cat+'_Signal'+year+sigNameListInput[j]+'M'+mass+narrow,tmpSigMass)
            signalTree.SetBranchAddress('unBinnedWeight_Signal'+year+sigNameListInput[j]+'M'+mass+narrow,tmpSigWeight)
            tmpSigNumEvents = signalDict[lepton+year+'_4cat'].Get('unskimmedEventsTotal_Signal'+year+sigNameListInput[j]+'M'+mass+narrow).GetBinContent(1)
            sig_argSW = RooArgSet(mzg,weight)
            sig_ds = RooDataSet(sigName,sigName,sig_argSW,'Weight')
            for i in range(0,signalTree.GetEntries()):
              signalTree.GetEntry(i)

              if highMass and narrow == '':
                low = int(mass)*0.4
                high = int(mass)*1.6
              elif highMass:
                low = int(mass)*0.92
                high = int(mass)*1.08
              else:
                low = int(mass)-10
                high = int(mass)+10

              if tmpSigMass[0]> low and tmpSigMass[0]<high:
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
              histName = '_'.join(['sig',lepton,yearToTeV[year],'cat'+cat,'M'+mass])
              rangeName = '_'.join(['range',lepton,yearToTeV[year],'cat'+cat,'M'+mass])

              signalList.append(TH1F(histName, histName, xmax-xmin, xmin, xmax))

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

            #if debugPlots and prod is 'gg':
            #  testFrame = mzg.frame()
            #  for i,signal in enumerate(signalListPDF):
            #    signalListDH[i].plotOn(testFrame)
            #    signal.plotOn(testFrame)
            #  testFrame.Draw()
            #  c.Print('debugPlots/'+'_'.join(['test','signals',suffix,year,lepton,'cat'+cat])+'.pdf')
            if debugPlots:
              testFrame = mzg.frame()
              for signal in signalListDS:
                signal.plotOn(testFrame, RooFit.DrawOption('pl'))
              testFrame.Draw()
              c.Print('debugPlots/initialFits/'+'_'.join(['test','ds','sig',suffix,prod,year,lepton,'cat'+cat])+'.png')
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
        if cat == '5' or highMass:
          data_ds = RooDataSet(dataName,dataName,data_argS)
        else:
          data_ds = RooDataHist(dataName,dataName,data_argS)
        for i in range(0,dataTree.GetEntries()):
          dataTree.GetEntry(i)
          if tmpMassEventOld[0]> xmin and tmpMassEventOld[0]<xmax:
            mzg.setVal(tmpMassEventOld[0])
            data_ds.add(data_argS)

        dataTree.ResetBranchAddresses()

        if verbose:
          print dataName
          data_ds.Print()
          print
        #if debugPlots:
        #  testFrame = mzg.frame()
        #  if highMass:
        #    #data_ds.plotOn(testFrame,RooFit.Binning(175))
        #    data_ds.plotOn(testFrame,RooFit.Binning(125))
        #  else:
        #    data_ds.plotOn(testFrame,RooFit.Binning(45))
        #  testFrame.Draw()
        #  c.Print('debugPlots/'+'_'.join(['test','data',year,lepton,'cat'+cat])+'.pdf')
        getattr(ws,'import')(data_ds)



#############
# make fits #
#############
        if verbose: 'starting fits'
        fitBuilder = FitBuilder(mzg, yearToTeV[year], lepton, cat)

        if allBiasFits:
          if cat == '5': bgFitList = cfl.bgFitListVBF
          elif highMass: bgFitList = cfl.bgFitListHighMass
          else: bgFitList = cfl.bgFitListTurnOn
        else:
          bgFitList = [cfl.bgLimitDict[highMass][yearToTeV[year]][lepton][cat]]

        leg  = TLegend(0.7,0.7,1.0,1.0)
        leg.SetFillColor(0)
        leg.SetShadowColor(0)
        leg.SetBorderSize(1)
        leg.SetHeader(', '.join([year,lepton,'cat'+cat]))

        testFrame = mzg.frame()
        #data_ds.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.CutRange('Blind1'))
        #data_ds.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.CutRange('Blind2'))
        if blind:
          data_ds.plotOn(testFrame,RooFit.Binning(6,xmin,cfl.blindRange[0]),RooFit.Name('data'))
          data_ds.plotOn(testFrame,RooFit.Binning(10,cfl.blindRange[1],xmax),RooFit.Name('data'))
          data_ds.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.Invisible())
        else:
          data_ds.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'))

        realFit = None
        fit_result = None
        for fitName in bgFitList:

          color = fitBuilder.FitColorDict[fitName]
          ndof = fitBuilder.FitNdofDict[fitName]
          if highMass and fitName == 'TripExpSum' and cfl.bgRange[1] == 700 and lepton == 'mu':
            fit = fitBuilder.Build(fitName, p3 = 0.01)
          else:
            fit = fitBuilder.Build(fitName)
          if type(fit) == tuple: fit = fit[0]
          if verbose: fit.Print()
          if highMass and fitName in ['TripExpSum']:
            fit.fitTo(data_ds, RooFit.Strategy(2), RooFit.Minos(True))
          else:
            fit.fitTo(data_ds, RooFit.Strategy(1))

          fit.plotOn(testFrame, RooFit.LineColor(color), RooFit.Name(fitName))
          testFrame.Draw()
          chi2 = testFrame.chiSquare(fitName,'data',ndof)
          leg.AddEntry(testFrame.findObject(fitName),fitName+' #chi2 = {0:.3f}'.format(chi2),'l')
          getattr(ws,'import')(fit)

        leg.Draw()
        c.Print('debugPlots/initialFits/'+'_'.join(['test','fits',suffix,year,lepton,'cat'+cat])+'.pdf')

        ws.commitTransaction()
        print 'commited'

  if not os.path.isdir('outputDir/'+suffix+'_'+YR+'_'+sigFit): os.mkdir('outputDir/'+suffix+'_'+YR+'_'+sigFit)
  print 'writing'
  ws.writeToFile('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix.rstrip('_Cut')+'.root')
  #ws.writeToFile('wtf.root')


  print 'we did it!'




if __name__=="__main__":
  doInitialFits()
