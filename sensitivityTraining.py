#!/usr/bin/env python
import sys
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
from math import sqrt

gROOT.SetBatch()
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

leptonList = ['mu','el']
tevList = ['8TeV']
catList = ['0','1','2','3','4','5']
sigNameList = ['ggH','qqH','ttH','WH','ZH']
#sigNameList = ['ttH']

def Sensitivity(suffix = 'Proper'):

  rooWsFile = TFile('outputDir/{0}/initRooFitOut_{0}.root'.format(suffix))
  myWs = rooWsFile.Get('ws')

  mzg = myWs.var('CMS_hzg_mass')
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
          sigName = '_'.join(['ds',prod,'hzg',lepton,tev,'cat'+cat,'M125'])
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
  if len(sys.argv) > 1:
    Sensitivity(sys.argv[1])
  else:
    Sensitivity()
