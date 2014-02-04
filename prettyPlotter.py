#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

def CombinedBG():
  suffixCard = 'MVA_02-03-14'

  rooWsFile = TFile('testRooFitOut_'+suffixCard+'.root')
  myWs = rooWsFile.Get('ws')
  leptonList = ['mu','el']
  yearList = ['2012']
  catList = ['1','2','3','4','6','7','8','9']

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

