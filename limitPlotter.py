#!/usr/bin/env python
import sys
import os
from ROOT import *
import numpy as np
from collections import defaultdict
import configLimits as cfl

gROOT.SetBatch()
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

fullCombo =cfl.fullCombo
byParts = cfl.byParts
YR = cfl.YR
sigFit = cfl.sigFit
#YR = 'YR2012ICHEP'
suffix = cfl.suffix
mode = cfl.mode
#suffix = '04-28-14_Proper'
#extras = ['04-28-14_PhoMVA','04-28-14_PhoMVAKinMVA']
extras = []
doObs = cfl.obs
syst = cfl.syst





def LimitPlot(CardOutput,AnalysisSuffix,cardName,extraSuffix):
  massList = [float(x) for x in cfl.massListBig]

  c = TCanvas("c","c",0,0,500,400)
  c.cd()
  if cfl.highMass and not cfl.modelIndependent: c.SetLogy()

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
      #currentDir = '/'.join(['outputDir',AnalysisSuffix+'_'+YR+'_'+sigFit,str(mass),'limitOutput'])
      currentDir = '/'.join(['outputDir',AnalysisSuffix+'_'+YR+'_'+sigFit,str(mass)])
    else:
      currentDir = '/'.join(['outputDir',AnalysisSuffix,str(mass),'limitOutput'])
    #print currentDir
    #fileList = os.listdir(currentDir)
    #if cfl.syst:
    #  thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' not in fileName,fileList)[0]
    #else:
    #  thisFile = filter(lambda fileName: CardOutput in fileName and 'nosyst' in fileName,fileList)[0]
    #print fileList
    #raw_input()
    thisFile = 'higgsCombine{1}.Asymptotic.mH{0}.root'.format(str(mass).replace('.0',''),cardName)
    #f = open('/'.join([currentDir,thisFile]))
    f = TFile('/'.join([currentDir,thisFile]))
    t = f.Get('limit')
    #print f
    #raw_input()
    xAxis.append(mass)

    #for line in f:
    #  splitLine = line.split()
    #  if 'Observed' in splitLine: obs.append(float(splitLine[-1]))
    #  elif '2.5%:' in splitLine: exp2SigLow.append(float(splitLine[-1]))
    #  elif '16.0%:' in splitLine: exp1SigLow.append(float(splitLine[-1]))
    #  elif '50.0%:' in splitLine: exp.append(float(splitLine[-1]))
    #  elif '84.0%:' in splitLine: exp1SigHi.append(float(splitLine[-1]))
    #  elif '97.5%:' in splitLine: exp2SigHi.append(float(splitLine[-1]))
    #f.close()

    count = 0
    for ev in t:
      if count == 0: exp2SigLow.append(ev.limit)
      elif count == 1: exp1SigLow.append(ev.limit)
      elif count == 2: exp.append(ev.limit)
      elif count == 3: exp1SigHi.append(ev.limit)
      elif count == 4: exp2SigHi.append(ev.limit)
      elif count == 5: obs.append(ev.limit)
      count +=1
    f.Close()

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
        if syst:
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
  if len(extras) == 0 and doObs:
    mg.Add(observed)
  elif len(extras) != 0:
    for i,ar in enumerate(extraExpected):
      ar.SetMarkerColor(kBlack)
      ar.SetMarkerStyle(kFullCircle)
      ar.SetMarkerSize(1.5)
      ar.SetLineColor(colorList[i])
      ar.SetLineWidth(2)
      ar.SetLineStyle(2)
      mg.Add(ar)
  else:
    print 'no obs'

  mg.Draw('AL3')
  #mg.Draw('Asame')
  mg.GetXaxis().SetTitle('m_{H} (GeV)')
  if cfl.modelIndependent:
    mg.GetYaxis().SetTitle('#sigma(gg->a)XBR(a->ll#gamma) (fb)')
  else:
    mg.GetYaxis().SetTitle('95% CL limit on #sigma/#sigma_{SM}')
  mg.GetXaxis().SetLimits(massList[0],massList[-1]);
  c.RedrawAxis()
  if extraSuffix == None and not doObs: extraSuffix = 'noObs'
  global syst
  if syst == False: syst = 'nosyst'
  saveNames = ['limitPlot']
  for saveName in [CardOutput, suffix, YR, sigFit, extraSuffix, syst]:
    if type(saveName) == str:
      saveNames.append(saveName)

  c.Print('debugPlots/'+'_'.join(saveNames)+'.pdf')


if __name__=='__main__':
  try:
    extraSuffix = sys.argv[1]
  except:
    extraSuffix = None
  if fullCombo:
    print 'FULL COMBO PLOT'
    if mode == 'Combo':
      cardName = '_'.join(['hzg','FullCombo_',suffix])
    else:
      cardName = '_'.join(['hzg',myLepton,tev,'cat'+cat+'_',suffix])
    cardName = 'Output'+cardName[3:]
    LimitPlot('FullCombo',suffix,cardName,extraSuffix)
  if byParts:
    print 'BY PARTS PLOTS'
    leptonList = cfl.leptonList
    tevList = cfl.tevList
    catListBig = cfl.catListBig
    catListSmall = cfl.catListSmall
    for lepton in leptonList:
      for tev in tevList:
        for cat in catListSmall:
          if cat == '0' and not cfl.highMass: continue
          if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
          elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
          else: myLepton = lepton
          outputName = '_'.join(['Output',myLepton,tev,'cat'+cat])
          print outputName
          if mode == 'Combo':
            cardName = '_'.join(['hzg','FullCombo_',suffix])
          else:
            cardName = '_'.join(['hzg',myLepton,tev,'cat'+cat+'_',suffix])
          cardName = 'Output'+cardName[3:]


          LimitPlot(outputName,suffix,cardName,extraSuffix)



