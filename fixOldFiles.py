#!/usr/bin/env python
import sys,os
#sys.argv.append('-b')
from ROOT import *
import numpy as np


gROOT.SetBatch()

leptonList = ['mu','el']
yearList = ['2011','2012']
catList = ['0','1','2','3','4','5']
massList = ['120','125','130','135','140','145','150','155','160']
sigNameListInput = ['gg','vbf','tth','wh','zh']

for lep in leptonList:
  for year in yearList:
    infileData = TFile('inputFiles/poterFiles/data_'+lep.capitalize()+year+'.root','READ')
    infileSignal = TFile('inputFiles/poterFiles/signal_'+lep.capitalize()+year+'.root','READ')
    if lep == 'el': outfile = TFile('inputFiles/m_llgFile_'+lep[0].capitalize()*2+year+'ABCD_Proper.root','RECREATE')
    else: outfile = TFile('inputFiles/m_llgFile_'+lep.capitalize()*2+year+'ABCD_Proper.root','RECREATE')

    # data part
    dataTreeIn = infileData.Get('m_llg_DATA')
    outfile.cd()
    dataTreeOut = TTree('m_llg_DATA','m_llg_DATA')

    n0 = np.zeros(1, dtype='d')
    n1 = np.zeros(1, dtype='d')
    n2 = np.zeros(1, dtype='d')
    n3 = np.zeros(1, dtype='d')
    n4 = np.zeros(1, dtype='d')
    n5 = np.zeros(1, dtype='d')
    dataTreeOut.Branch('m_llg_DATA',n0,'m_llg_DATA/D')
    dataTreeOut.Branch('m_llgCAT1_DATA',n1,'m_llgCAT1_DATA/D')
    dataTreeOut.Branch('m_llgCAT2_DATA',n2,'m_llgCAT2_DATA/D')
    dataTreeOut.Branch('m_llgCAT3_DATA',n3,'m_llgCAT3_DATA/D')
    dataTreeOut.Branch('m_llgCAT4_DATA',n4,'m_llgCAT4_DATA/D')
    if year == '2012': dataTreeOut.Branch('m_llgCAT5_DATA',n5,'m_llgCAT5_DATA/D')

    for event in dataTreeIn:
      n0[0] = event.m_llg_DATA
      n1[0] = event.m_llgCAT1_DATA
      n2[0] = event.m_llgCAT4_DATA
      n3[0] = event.m_llgCAT2_DATA
      n4[0] = event.m_llgCAT3_DATA
      if year == '2012': n5[0] = event.m_llgCAT5_DATA

      dataTreeOut.Fill()

    outfile.Write()
    outfile.Close()
    infileData.Close()
    infileSignal.Close()

