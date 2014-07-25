#!/usr/bin/env python
import sys
sys.argv.append('-b')
import os
from ROOT import *
import numpy as np
from collections import defaultdict
import configLimits as cfl

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

fullCombo =cfl.fullCombo
byParts = cfl.byParts
YR = cfl.YR
sigFit = cfl.sigFit
#YR = 'YR2012ICHEP'
suffix = cfl.suffix
#suffix = '04-28-14_Proper'
#extras = ['04-28-14_PhoMVA','04-28-14_PhoMVAKinMVA']
extras = []





def LimitPlot(CardOutput,AnalysisSuffix):
  massList = [120.0,120.5,121.0,121.5,122.0,122.5,123.0,123.5,124.0,124.5,
   124.6,124.7,124.8,124.9,125.0,125.1,125.2,125.3,125.4,125.5,
   125.6,125.7,125.8,125.9,126.0,126.1,126.2,126.3,126.4,126.5,
   127.0,127.5,128.0,128.5,129.0,129.5,130.0,
   130.5,131.0,131.5,132.0,132.5,133.0,133.5,134.0,134.5,135.0,
   135.5,136.0,136.5,137.0,137.5,138.0,138.5,139.0,139.5,140.0,
   141.0,142.0,143.0,144.0,145.0,146.0,147.0,148.0,149.0,150.0,
   151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0,160.0]

  c = TCanvas("c","c",0,0,500,400)
  c.cd()

  colorList = [kRed,kBlue,kGreen+1]

  xAxis = []
  obs = []
  exp = []
  exp1SigHi = []
  exp1SigLow = []
  exp2SigHi = []
  exp2SigLow = []

  expExtra = []
  for ex in extras:
    expExtra.append([])
  for mass in massList:
    if YR:
      currentDir = '/'.join(['outputDir',AnalysisSuffix+'_'+YR+'_'+sigFit,str(mass),'limitOutput'])
    else:
      currentDir = '/'.join(['outputDir',AnalysisSuffix,str(mass),'limitOutput'])
    #print currentDir
    fileList = os.listdir(currentDir)
    if cfl.syst:
      thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' not in fileName,fileList)[0]
    else:
      thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' in fileName,fileList)[0]
    #print fileList
    #raw_input()
    f = open('/'.join([currentDir,thisFile]))
    #print f
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
    if mass == 125.0:
      print mass
      print 'obs:', obs[-1]
      print 'exp:', exp[-1]
    if len(obs) != len(xAxis):
      obs.append(0.0)
      print 'obs busted for',mass
      raw_input()
    if len(exp) != len(xAxis):
      exp.append(0.0)
      print 'exp busted for',mass
      raw_input()
    if len(exp1SigLow) != len(xAxis):
      exp1SigLow.append(0.0)
      print 'exp1SigLow busted for',mass
      raw_input()
    if len(exp2SigLow) != len(xAxis):
      exp2SigLow.append(0.0)
      print 'exp2SigLow busted for',mass
      raw_input()
    if len(exp1SigHi) != len(xAxis):
      exp1SigHi.append(0.0)
      print 'exp1SigHi busted for',mass
      raw_input()
    if len(exp2SigHi) != len(xAxis):
      exp2SigHi.append(0.0)
      print 'exp2SigHi busted for',mass
      raw_input()

    if len(extras) != 0:
      for i,extraSuffix in enumerate(extras):
        if YR:
          currentDir = '/'.join(['outputDir',extraSuffix+'_'+YR+'_'+sigFit,str(mass),'limitOutput'])
        else:
          currentDir = '/'.join(['outputDir',extraSuffix,str(mass),'limitOutput'])
        fileList = os.listdir(currentDir)
        if cfl.syst:
          thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' not in fileName,fileList)[0]
        else:
          thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' in fileName,fileList)[0]
        f = open('/'.join([currentDir,thisFile]))
        for line in f:
          splitLine = line.split()
          if '50.0%:' in splitLine: expExtra[i].append(float(splitLine[-1]))
        f.close()


  #print 'masses:', xAxis
  #print 'obs:',obs
  #print 'exp:',exp
  #print exp2SigLow
  #print exp1SigLow
  #print exp1SigHi
  #print exp2SigHi

  exp2SigLowErr = [a-b for a,b in zip(exp,exp2SigLow)]
  exp1SigLowErr = [a-b for a,b in zip(exp,exp1SigLow)]
  exp2SigHiErr = [fabs(a-b) for a,b in zip(exp,exp2SigHi)]
  exp1SigHiErr = [fabs(a-b) for a,b in zip(exp,exp1SigHi)]

  #print '2 sig low:',exp2SigLowErr
  #print '1 sig low:',exp1SigLowErr
  #print '1 sig hi:',exp1SigHiErr
  #print '2 sig hi:',exp2SigHiErr

  xAxis_Array = np.array(xAxis,dtype=float)
  obs_Array = np.array(obs,dtype=float)
  exp_Array = np.array(exp,dtype='d')
  exp2SigLowErr_Array = np.array(exp2SigLowErr,dtype=float)
  exp1SigLowErr_Array = np.array(exp1SigLowErr,dtype=float)
  exp1SigHiErr_Array = np.array(exp1SigHiErr,dtype=float)
  exp2SigHiErr_Array = np.array(exp2SigHiErr,dtype=float)
  zeros_Array = np.zeros(len(xAxis),dtype = float)

  mg = TMultiGraph()
  mg.SetTitle('')

  nPoints = len(xAxis)
  expected = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)
  oneSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp1SigLowErr_Array,exp1SigHiErr_Array)
  twoSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp2SigLowErr_Array,exp2SigHiErr_Array)
  observed = TGraphAsymmErrors(nPoints,xAxis_Array,obs_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)
  if len(extras) != 0:
    extraExpected = []
    for ar in expExtra:
      extraExpected.append(TGraphAsymmErrors(nPoints,xAxis_Array,np.array(ar,dtype='d'),zeros_Array,zeros_Array,zeros_Array,zeros_Array))


  #expected.Print()
  #raw_input()
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
  if len(extras) == 0:
    print 'non obs'
    mg.Add(observed)
  else:
    for i,ar in enumerate(extraExpected):
      ar.SetMarkerColor(kBlack)
      ar.SetMarkerStyle(kFullCircle)
      ar.SetMarkerSize(1.5)
      ar.SetLineColor(colorList[i])
      ar.SetLineWidth(2)
      ar.SetLineStyle(2)
      mg.Add(ar)

  mg.Draw('AL3')
  #mg.Draw('Asame')
  mg.GetXaxis().SetTitle('m_{H} (GeV)')
  mg.GetYaxis().SetTitle('95% CL limit on #sigma/#sigma_{SM}')
  mg.GetXaxis().SetLimits(massList[0],massList[-1]);
  c.RedrawAxis()
  if YR:
    if cfl.syst:
      c.Print('debugPlots/limitPlot_'+CardOutput+'_'+suffix+'_'+YR+'_'+sigFit+'.pdf')
    else:
      c.Print('debugPlots/limitPlot_'+CardOutput+'_'+suffix+'_'+YR+'_'+sigFit+'_nosyst.pdf')
  else:
    if cfl.syst:
      c.Print('debugPlots/limitPlot_'+CardOutput+'_'+suffix+'.pdf')
    else:
      c.Print('debugPlots/limitPlot_'+CardOutput+'_'+suffix+'_nosyst.pdf')


if __name__=='__main__':
  if fullCombo:
    print 'FULL COMBO PLOT'
    LimitPlot('FullCombo',suffix)
  if byParts:
    print 'BY PARTS PLOTS'
    leptonList = cfl.leptonList
    tevList = cfl.tevList
    catListBig = cfl.catListBig
    catListSmall = cfl.catListSmall
    for lepton in leptonList:
      for tev in tevList:
        for cat in catListSmall:
          if cat == '0': continue
          if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
          elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
          else: myLepton = lepton
          outputName = '_'.join(['Output',myLepton,tev,'cat'+cat])
          print outputName
          LimitPlot(outputName,suffix)



