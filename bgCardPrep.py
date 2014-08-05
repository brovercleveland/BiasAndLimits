#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import configLimits as cfl

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

doMVA = cfl.doMVA
doExt = cfl.doExt
suffixCard = cfl.suffix

leptonList = cfl.leptonList
tevList = cfl.tevList
catListSmall = cfl.catListSmall
catListBig = cfl.catListBig

YR = cfl.YR
sigFit = cfl.sigFit
highMass = cfl.highMass


#rooWsFile = TFile('testRooFitOut_Poter.root')
rooWsFile = TFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffixCard+'.root')
myWs = rooWsFile.Get('ws')
card_ws = RooWorkspace('ws_card')
#card_ws.autoImportClassCode(True)

c = TCanvas("c","c",0,0,500,400)
c.cd()
mzg = myWs.var('CMS_hzg_mass')
mzg.setRange('signal',120,130)

########################################
# prep the background and data card    #
# we're going to the extend the bg pdf #
# and rename the parameters to work    #
# with the higgs combination tool      #
########################################


for tev in tevList:
  for lepton in leptonList:
    if tev == '8TeV' and doMVA: catList = catListBig
    else: catList = catListSmall
    for cat in catList:
      if cat is '5' and tev is '7TeV' and lepton is 'mu': continue
      elif cat is '5' and tev is '7TeV' and lepton is 'el': lepton = 'all'

      dataName = '_'.join(['data',lepton,tev,'cat'+cat])
      suffix = '_'.join([tev,lepton,'cat'+cat])

      fitNameHeader = cfl.bgLimitDict[highMass][tev][lepton][cat]
      fitName = fitNameHeader+'_'+suffix
      normName = 'norm'+fitName

      data = myWs.data(dataName)
      fit = myWs.pdf(fitName)
      fit.Print()

      ###### Extend the fit (give it a normalization parameter)
      print dataName
      sumEntries = data.sumEntries()
      sumEntriesS = data.sumEntries('1','signal')
      print sumEntries, sumEntriesS
      #raw_input()
      dataYieldName = '_'.join(['data','yield',lepton,tev,'cat'+cat])
      dataYield = RooRealVar(dataYieldName,dataYieldName,sumEntries)
      if doExt:
        norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.5,sumEntries*1.5)
        print 'start', norm.getVal()
        fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
        fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)

        fit_ext.fitTo(data,RooFit.Range('fullRegion'))

        testFrame = mzg.frame()
        data.plotOn(testFrame)
        fit_ext.plotOn(testFrame)
        testFrame.Draw()
        c.Print('debugPlots/'+'_'.join(['test','data','fit',lepton,tev,'cat'+cat])+'.pdf')
        print 'end', norm.getVal()
      else:
        norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.9,sumEntries*1.1)


      ###### Import the fit and data, and rename them to the card convention

      dataNameNew = '_'.join(['data','obs',lepton,tev,'cat'+cat])
      dataYieldNameNew = '_'.join(['data','yield',lepton,tev,'cat'+cat])
      dataYield.SetName(dataYieldNameNew)

      getattr(card_ws,'import')(data,RooFit.Rename(dataNameNew))
      if doExt:
        getattr(card_ws,'import')(fit_ext)
      else:
        getattr(card_ws,'import')(fit)
        normNameFixed  = '_'.join(['bkg',lepton,tev,'cat'+cat,'norm'])
        norm.SetName(normNameFixed)
        getattr(card_ws,'import')(norm)
      getattr(card_ws,'import')(dataYield)
      card_ws.commitTransaction()
      #fit_ext.Print()
      fitBuilder = FitBuilder(mzg,tev,lepton,cat)
      fitBuilder.BackgroundNameFixer(card_ws,fitNameHeader,doExt)
      #BackgroundNameFixer(tev,lepton,cat,card_ws,cat,doExt)

card_ws.writeToFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/CardBackground_'+suffixCard+'.root')






