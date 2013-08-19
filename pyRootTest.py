#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );

mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',0,100)
for i in range(0,100):
  newDataTree = TTree('tree_tmp','tree_tmp')
  newDataTree.Print()
  tmpMassEventNew = np.zeros(1,dtype = float)
  tmpMassEventOld = np.zeros(1,dtype = float)
  dataFile = TFile('data_Mu2011.root','r')
  dataTree = dataFile.Get('m_llg_DATA')
  dataTree.SetBranchAddress('m_llgCAT1_DATA',tmpMassEventOld)
  newDataTree.Branch('CMS_hzg_mass', tmpMassEventNew,'CMS_hzg_mass/D')
  for j in range (0,dataTree.GetEntries()):
    dataTree.GetEntry(j)
    tmpMassEventNew[0] = tmpMassEventOld[0]
    print tmpMassEventNew[0],tmpMassEventOld[0]
    newDataTree.Fill()

  newDataTree.Print()
  raw_input()
  newDataTree.Delete()
  #data_argS = RooArgSet(mzg)
  #data_ds = RooDataSet('tmp_ds','tmp_ds',data_argS,RooFit.Import(newDataTree))

