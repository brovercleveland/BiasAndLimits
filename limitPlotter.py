#!/usr/bin/env python
import sys
sys.argv.append('-b')
import os
from ROOT import *
import numpy as np
from collections import defaultdict

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

fullCombo = False
byParts = True
suffix = 'Proper'





def LimitPlot(CardOutput,AnalysisSuffix):
  massList = [120.0,120.5,121.0,121.5,122.0,122.5,123.0,123.5,124.0,124.5,125.0,
   125.5,126.0,126.5,127.0,127.5,128.0,128.5,129.0,129.5,130.0,
   130.5,131.0,131.5,132.0,132.5,133.0,133.5,134.0,134.5,135.0,
   135.5,136.0,136.5,137.0,137.5,138.0,138.5,139.0,139.5,140.0,
   141.0,142.0,143.0,144.0,145.0,146.0,147.0,148.0,149.0,150.0,
   151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0,160.0]

  c = TCanvas("c","c",0,0,500,400)
  c.cd()

  xAxis = []
  obs = []
  exp = []
  exp1SigHi = []
  exp1SigLow = []
  exp2SigHi = []
  exp2SigLow = []
  for mass in massList:
    currentDir = '/'.join(['outputDir',AnalysisSuffix,str(mass),'limitOutput'])
    fileList = os.listdir(currentDir)
    thisFile = filter(lambda fileName: CardOutput in fileName,fileList)[0]
    print fileList
    #raw_input()
    f = open('/'.join([currentDir,thisFile]))
    print f
    #raw_input()
    xAxis.append(mass)
    for line in f:
      splitLine = line.split()
      if 'Observed' in splitLine: obs.append(float(splitLine[-1]))
      elif '2.5%:' in splitLine: exp2SigLow.append(float(splitLine[-1]))
      elif '16.0%:' in splitLine: exp1SigLow.append(float(splitLine[-1]))
      elif '50.0%:' in splitLine: exp.append(float(splitLine[-1]))
      elif '84.0%:' in splitLine: exp1SigHi.append(float(splitLine[-1]))
      elif '97.5%:' in splitLine: exp2SigHi.append(float(splitLine[-1]))
    f.close()
  print 'masses:', xAxis
  print 'obs:',obs
  print 'exp:',exp
  #print exp2SigLow
  #print exp1SigLow
  #print exp1SigHi
  #print exp2SigHi

  exp2SigLowErr = [a-b for a,b in zip(exp,exp2SigLow)]
  exp1SigLowErr = [a-b for a,b in zip(exp,exp1SigLow)]
  exp2SigHiErr = [fabs(a-b) for a,b in zip(exp,exp2SigHi)]
  exp1SigHiErr = [fabs(a-b) for a,b in zip(exp,exp1SigHi)]

  print '2 sig low:',exp2SigLowErr
  print '1 sig low:',exp1SigLowErr
  print '1 sig hi:',exp1SigHiErr
  print '2 sig hi:',exp2SigHiErr

  xAxis_Array = np.array(xAxis)
  obs_Array = np.array(obs)
  exp_Array = np.array(exp)
  exp2SigLowErr_Array = np.array(exp2SigLowErr)
  exp1SigLowErr_Array = np.array(exp1SigLowErr)
  exp1SigHiErr_Array = np.array(exp1SigHiErr)
  exp2SigHiErr_Array = np.array(exp2SigHiErr)
  zeros_Array = np.zeros(len(xAxis),dtype = float)

  mg = TMultiGraph()
  mg.SetTitle('')

  nPoints = len(xAxis)
  expected = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)
  oneSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp1SigLowErr_Array,exp1SigHiErr_Array)
  twoSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp2SigLowErr_Array,exp2SigHiErr_Array)
  observed = TGraphAsymmErrors(nPoints,xAxis_Array,obs_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)

  oneSigma.SetFillColor(kGreen)

  twoSigma.SetFillColor(kYellow)

  expected.SetMarkerColor(kBlack)
  expected.SetMarkerStyle(kFullCircle)
  expected.SetMarkerSize(1.5)
  expected.SetLineColor(kBlack)
  expected.SetLineWidth(2)
  expected.SetLineStyle(2)

  observed.SetLineWidth(2)

  mg.Add(twoSigma)
  mg.Add(oneSigma)
  mg.Add(expected)
  mg.Add(observed)

  mg.Draw('AL3')
  mg.GetXaxis().SetTitle('m_{H} (GeV)')
  mg.GetYaxis().SetTitle('95% CL limit on #sigma/#sigma_{SM}')
  mg.GetXaxis().SetLimits(massList[0],massList[-1]);

  c.Print('debugPlots/limitPlot_'+CardOutput+'.pdf')

if __name__=='__main__':
  if fullCombo:
    LimitPlot('FullCombo',suffix)
  if byParts:
    leptonList = ['mu','el']
    yearList = ['2012','2011']
    catListBig = ['1','2','3','4','5','6','7','8','9']
    catListSmall = ['1','2','3','4','5']
    for lepton in leptonList:
      for year in yearList:
        for cat in catListSmall:
          if cat == '5' and year == '2011' and lepton == 'el': myLepton = 'all'
          elif cat == '5' and year == '2011' and lepton == 'mu': continue
          else: myLepton = lepton
          outputName = '_'.join(['Output',myLepton,year,'cat'+cat])
          LimitPlot(outputName,suffix)



