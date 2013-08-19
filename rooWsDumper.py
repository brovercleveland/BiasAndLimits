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

#rooWsFile = TFile('testRooFitOut.root')
rooWsFile = TFile('exampleCards/hzg.inputbkg_8TeV.root')
#rooWsFile = TFile('exampleCards/hzg.mH122.0.inputsig_8TeV.root')
#rooWsFile = TFile('testCardSignal_125.0.root')
#myWs = rooWsFile.Get('ws')
myWs = rooWsFile.Get('w_all')
#myWs = rooWsFile.Get('ws_card')
print 'printing rooWsFile'
myWs.Print()

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
