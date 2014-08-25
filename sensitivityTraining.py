#!/usr/bin/env python
import sys
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
from math import sqrt
import configLimits as cfl

gROOT.SetBatch()
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

leptonList = cfl.leptonList
tevList = ['8TeV']
catList = cfl.catListSmall
sigNameList = cfl.sigNameList
highMass = cfl.highMass
suffix = cfl.suffix
sigFit = cfl.sigFit
YR = cfl.YR
if highMass:
  mass = 'M200'
else:
  mass = 'M125'

def Sensitivity(suffix = 'Proper'):

  rooWsFile = TFile('outputDir/{0}_{1}_{2}/initRooFitOut_{0}.root'.format(suffix,YR,sigFit))
  myWs = rooWsFile.Get('ws')

  mzg = myWs.var('CMS_hzg_mass')
  if highMass:
    mzg.setRange('signal',180,220)
  else:
    mzg.setRange('signal',120,130)

  print suffix
  print


############################################
# Get significance or sensitivity for M125 #
############################################

  for tev in tevList:
    print tev
    for lepton in leptonList:
      print ' '+lepton
      for cat in catList:
        print '  Cat'+cat
        dataName = '_'.join(['data',lepton,tev,'cat'+cat])
        data = myWs.data(dataName)

        sumEntries = data.sumEntries()
        sumEntriesS = data.sumEntries('1','signal')
        #print sumEntries
        totalSigS = 0
        totalSig = 0
        totalSigRaw = 0
        for prod in sigNameList:
          sigName = '_'.join(['ds',prod,'hzg',lepton,tev,'cat'+cat,mass])
          print sigName
          sig_ds = myWs.data(sigName)
          if (prod == 'WH' and suffix != 'Proper'):
            totalSigS = totalSigS + sig_ds.sumEntries('1','signal')/10
            totalSig = totalSig + sig_ds.sumEntries()/10
          elif (prod == 'ZH' and suffix != 'Proper'):
            totalSigS = totalSigS + sig_ds.sumEntries('1','signal')/2
            totalSig = totalSig + sig_ds.sumEntries()/2
          else:
            totalSigS = totalSigS + sig_ds.sumEntries('1','signal')
            totalSig = totalSig + sig_ds.sumEntries()
          if prod == 'ggH':
            totalSigRaw = totalSigRaw + sig_ds.numEntries()

        signif = totalSigS/sqrt(totalSigS+sumEntriesS)
        print '    100-190: total bg: {0:}, total sig: {1:.3}'.format(sumEntries,totalSig)
        print '    120-130: total bg: {0:}, total sig: {1:.3}, signif: {2:.3}, acc: {3:.3}%'.format(sumEntriesS,totalSigS, signif, totalSigRaw*100./(100000/3))


if __name__ == "__main__":
  Sensitivity(suffix)
