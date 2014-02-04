#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

leptonList = ['mu','el']
yearList = ['2012']
#yearList = ['2012','2011']
#catList = ['0']
catList = ['1','2','3','4','6','7','8','9']
catFix = True
suffixCard = 'MVA_02-03-14'

#rooWsFile = TFile('testRooFitOut_Poter.root')
rooWsFile = TFile('testRooFitOut_'+suffixCard+'.root')
myWs = rooWsFile.Get('ws')
card_ws = RooWorkspace('ws_card')
card_ws.autoImportClassCode(True)

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


for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      if cat is '5' and year is '2011' and lepton is 'mu': continue
      elif cat is '5' and year is '2011' and lepton is 'el': lepton = 'all'
      dataName = '_'.join(['data',lepton,year,'cat'+cat])
      suffix = '_'.join([year,lepton,'cat'+cat])
      if cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
        fitName = '_'.join(['GaussBern4',year,lepton,'cat'+cat])
        normName = 'normGaussBern4_'+suffix
      elif cat is '5':
        fitName = '_'.join(['Bern3',year,lepton,'cat'+cat])
        normName = 'normBern3_'+suffix
      elif cat is '0':
        fitName = '_'.join(['GaussBern6',year,lepton,'cat'+cat])
        normName = 'normGaussBern6_'+suffix
      else:
        fitName = '_'.join(['GaussBern5',year,lepton,'cat'+cat])
        normName = 'normGaussBern5_'+suffix

      data = myWs.data(dataName)
      fit = myWs.pdf(fitName)

      ###### Extend the fit (give it a normalization parameter)
      print dataName
      sumEntries = data.sumEntries()
      sumEntriesS = data.sumEntries('1','signal')
      print sumEntries, sumEntriesS
      #raw_input()
      dataYieldName = '_'.join(['data','yield',lepton,year,'cat'+cat])
      dataYield = RooRealVar(dataYieldName,dataYieldName,sumEntries)
      norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.25,sumEntries*1.75)
      fitExtName = '_'.join(['bkgTmp',lepton,year,'cat'+cat])
      fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)

      fit_ext.fitTo(data,RooFit.Range('fullRegion'))

      testFrame = mzg.frame()
      data.plotOn(testFrame)
      fit_ext.plotOn(testFrame)
      testFrame.Draw()
      c.Print('debugPlots/'+'_'.join(['test','data','fit',lepton,year,'cat'+cat])+'.pdf')

      ###### Import the fit and data, and rename them to the card convention
      newCat = cat
      if catFix:
        if year is '2012':
          if cat == '2':
            newCat = '3'
          elif cat == '3':
            newCat = '4'
          elif cat == '4':
            newCat = '2'
          elif cat == '7':
            newCat = '9'
          elif cat == '8':
            newCat = '7'
          elif cat == '9':
            newCat = '8'
      dataNameNew = '_'.join(['data','obs',lepton,year,'cat'+newCat])
      dataYieldNameNew = '_'.join(['data','yield',lepton,year,'cat'+newCat])
      dataYield.SetName(dataYieldNameNew)

      getattr(card_ws,'import')(data,RooFit.Rename(dataNameNew))
      getattr(card_ws,'import')(fit_ext)
      getattr(card_ws,'import')(dataYield)
      card_ws.commitTransaction()
      fit_ext.Print()
      BackgroundNameFixer(year,lepton,cat,card_ws,newCat)

card_ws.writeToFile('testCards/testCardBackground_'+suffixCard+'.root')






