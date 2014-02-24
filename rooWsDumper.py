#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

leptonList = ['mu','el']
yearList = ['2011','2012']
catList = ['1','2','3','4']
massList = ['120','125','130','135','140','145','150']

#rooWsFile_bkg = TFile('testRooFitOut_Poter.root')
#rooWsFile_bkg = TFile('exampleCards/hzg.inputbkg_8TeV.root')
#rooWsFile_sig = TFile('exampleCards/hzg.mH120.0.inputsig_8TeV.root')
rooWsFile_sig = TFile('testCards/testCardSignal_125.0.root')
#rooWsFile_bkg = TFile('testCards/testCardBackground_MVA.root')
#myWs = rooWsFile.Get('ws')
#myWs_sig = rooWsFile_sig.Get('w_all')
#myWs_bkg = rooWsFile_bkg.Get('w_all')
myWs_sig = rooWsFile_sig.Get('ws_card')
#myWs_bkg = rooWsFile_bkg.Get('ws_card')
print 'printing rooWsFile'
myWs_sig.Print()
#myWs_bkg.Print()

testVar = myWs_bkg.var('mzg_bkg_norm_cat31')
testVar.Print()

mzg = myWs_bkg.var("CMS_hzg_mass")
mzg.setRange(100,190)
mzg.Print()
c = TCanvas("c","c",0,0,500,400)
c.cd()
data = myWs_bkg.data('data_obs_mu_2012_cat1')
pdf = myWs_bkg.pdf('bkg_mu_2012_cat1')
testFrame1 = mzg.frame()
data.plotOn(testFrame1)
pdf.plotOn(testFrame1)
testFrame1.Draw()
c.Print('debugPlots/test_ws_bkg.pdf')
c.Clear()
testFrame2 = mzg.frame()
sig = myWs_sig.pdf('sig_gg_mu_2012_cat1')
sig.plotOn(testFrame2)
testFrame2.Draw()
c.Print('debugPlots/test_ws_signal.pdf')


'''
mzg = myWs.var("CMS_hzg_mass")
mzg.Print()

c = TCanvas("c","c",0,0,500,400)
c.cd()
testFrame = mzg.frame()

for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      for mass in massList:
        pdf_sig = myWs.pdf('pdf_sig_'+lepton+'_'+year+'_cat'+cat+'_M'+mass)
        pdf_sig.Print()

        if lepton is 'el': color = kRed
        else: color = kBlue
        if year is 2011: color = color+2
        pdf_sig.plotOn(testFrame,RooFit.LineColor(color),RooFit.LineStyle(int(cat)))
testFrame.Draw()
c.Print('debugPlots/test_ws_signal.pdf')
'''
