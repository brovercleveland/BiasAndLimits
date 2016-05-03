#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

rooWsFile= TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/SVN_datacards/750.0/CardBackground_04-27-15_HighMassNarrowRedux1600.root')
myWs = rooWsFile.Get('ws_card')
myWs.Print()
thing = myWs.var("bkg_p5_el_8TeV_cat0")
thing.Print()

'''
testVar = myWs_bkg.var('bkg_p1_mu_8TeV_cat0')
testVar.Print()

mzg = myWs_bkg.var("CMS_hzg_mass")
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
