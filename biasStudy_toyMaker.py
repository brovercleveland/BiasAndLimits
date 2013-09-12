#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
from collections import defaultdict
from toyStructs import makeToyStucts
import re

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

def doBiasStudy(year = '2012', lepton = 'mu', cat = '1', genFunc = 'GaussExp', mass = '125', trials = 100, job = 0):
  rooWsFile = TFile('testRooFitOut_Poter.root','r')
  myWs = rooWsFile.Get('ws')
  outName = '_'.join(['biasToys',year,lepton,'cat'+cat,genFunc,mass,'job'+str(job)])
  outFile = TFile(outName, 'RECREATE')
  tree = TTree('toys','toys')
  makeToyStucts()

  testFuncs = ['GaussBern3', 'GaussBern4', 'GaussBern5']

  #set up branches
  from ROOT import TOYDATA
  toyDataStruct = TOYDATA()
  tree.Branch('toyData', toyDataStruct, 'totalData/I:sigWindowData')
  for func in testFuncs:
    if func is 'GaussBern3':
      from ROOT import GAUSSBERN3
      GaussBern3Struct = GAUSSBERN3()
      tree.Branch('GaussBern3',GaussBern3Struct,'





