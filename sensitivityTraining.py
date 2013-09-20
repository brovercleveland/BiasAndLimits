#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
from math import sqrt

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

doME = True

leptonList = ['mu']
yearList = ['2012']
catList = ['0','1','2','3','4']
sigNameList = ['gg','vbf','tth','wh','zh']

rooWsFile1 = TFile('testRooFitOut_Poter.root')
rooWsFile2 = TFile('testRooFitOut_ME.root')
myWs1 = rooWsFile1.Get('ws')
myWs2 = rooWsFile2.Get('ws')

c = TCanvas("c","c",0,0,500,400)
c.cd()
mzg1 = myWs1.var('CMS_hzg_mass')
mzg1.setRange('signal',120,130)
mzg2 = myWs2.var('CMS_hzg_mass')
mzg2.setRange('signal',120,130)

# cat scale factors for signal
MEscales = {'0':8721.14/9796.82, '1':2953.66/3265.75, '2':1568.26/1753.6, '3':1609.57/1881.76, '4':2589.67/2895.74}

############################################
# Get significance or sensitivity for M125 #
############################################

for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      dataName = '_'.join(['data',lepton,year,'cat'+cat])
      suffix = '_'.join([year,lepton,'cat'+cat])
      if doME:
        data = myWs2.data(dataName)
      else:
        data = myWs1.data(dataName)

      sumEntries = data.sumEntries()
      sumEntriesS = data.sumEntries('1','signal')
      print sumEntriesS
      totalSig = 0
      for prod in sigNameList:
        sigName = '_'.join(['ds','sig',prod,lepton,year,'cat'+cat,'M125'])
        sig_ds = myWs1.data(sigName)
        if doME:
          totalSig = totalSig + MEscales[cat]*sig_ds.sumEntries('1','signal')
        else:
          totalSig = totalSig + sig_ds.sumEntries('1','signal')

      signif = totalSig/sqrt(totalSig+sumEntriesS)
      print 'bg', sumEntriesS, 'sig', totalSig, 'sig scale', MEscales[cat]
      print year, lepton, cat, signif, doME
      raw_input()
