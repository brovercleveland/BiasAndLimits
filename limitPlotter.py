#!/usr/bin/env python
import sys
import os
from ROOT import *
import numpy as np
from collections import defaultdict
import configLimits as cfl
import CMS_lumi

gROOT.SetBatch()
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

fullCombo =cfl.fullCombo
byParts = cfl.byParts
YR = cfl.YR
sigFit = cfl.sigFit
#YR = 'YR2012ICHEP'
suffix = cfl.suffixPostFix
mode = cfl.mode

extraList = False
#extraList = ['Output_FullCombo__12-04-14_HighMass','Output_FullCombo__12-04-14_HighMass800', 'Output_FullCombo__12-04-14_HighMass900']
#extraList = ['Output_FullCombo__12-04-14_HighMassNarrow800']
#extraList = ['Output_FullCombo__01-29-15_HighMassUp800','Output_FullCombo__01-29-15_HighMassDown800']
#extraList = ['Output_FullCombo__01-29-15_HighMassUpNarrow800','Output_FullCombo__01-29-15_HighMassDownNarrow800']
#extraList = ['Output_FullCombo__02-03-15_HighMassPUWeightUp800']
#extraList = ['Output_FullCombo__02-04-15_HighMassZ75800']
#extraPath = ['12-04-14_HighMass', '12-04-14_HighMass800', '12-04-14_HighMass900']
#extraPath = ['12-04-14_HighMassNarrow800']
#extraPath = ['01-29-15_HighMassUp800','01-29-15_HighMassDown800']
#extraPath = ['01-29-15_HighMassUpNarrow800','01-29-15_HighMassDownNarrow800']
#extraPath = ['02-03-15_HighMassPUWeightUp800']
#extraPath = ['02-04-15_HighMassZ75800']

doObs = cfl.obs
syst = cfl.syst





def LimitPlot(CardOutput,AnalysisSuffix,cardName,extraSuffix):
  massList = [float(x) for x in cfl.massListBig]

  c = TCanvas("c","c",0,0,500,400)
  c.cd()
  c.SetTopMargin(0.075);

  if cfl.highMass and '2000' in suffix: c.SetLogy()


  colorList = [kRed,kBlue,kGreen+1]

  xAxis = []
  obs = []
  exp = []
  exp1SigHi = []
  exp1SigLow = []
  exp2SigHi = []
  exp2SigLow = []

  if extraList: expExList = [ [] for i in extraList]

  for mass in massList:
    if YR:
      currentDir = '/'.join(['outputDir',AnalysisSuffix+'_'+YR+'_'+sigFit,str(mass)])
    else:
      currentDir = '/'.join(['outputDir',AnalysisSuffix,str(mass),'limitOutput'])
    thisFile = 'higgsCombine{1}.Asymptotic.mH{0}.root'.format(str(mass).replace('.0',''),cardName)
    f = TFile('/'.join([currentDir,thisFile]))
    t = f.Get('limit')
    fex = []
    tex = []
    if extraList:
      for i, extra in enumerate(extraList):
        if extraPath[i] == None:
          extraDir = currentDir
        else:
          extraDir = '/'.join(['outputDir',extraPath[i]+'_'+YR+'_'+sigFit,str(mass)])
        extraFile = 'higgsCombine{1}.Asymptotic.mH{0}.root'.format(str(mass).replace('.0',''),extra)
        fex.append(TFile('/'.join([extraDir,extraFile])))
        tex.append(fex[-1].Get('limit'))

    xAxis.append(mass)


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
    if extraList:
      for i,extra in enumerate(extraList):
        count = 0
        for ev in tex[i]:
          if count == 2: expExList[i].append(ev.limit)
          count +=1
        fex[i].Close()

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

  if extraList:
    expEx_Array = []
    for i, expEx in enumerate(expExList):
      expEx_Array.append(np.array(expEx,dtype='d'))


  mg = TMultiGraph()
  mg.SetTitle('')

  nPoints = len(xAxis)
  expected = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)
  oneSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp1SigLowErr_Array,exp1SigHiErr_Array)
  oneSigma.SetName('oneSigma')
  twoSigma = TGraphAsymmErrors(nPoints,xAxis_Array,exp_Array,zeros_Array,zeros_Array,exp2SigLowErr_Array,exp2SigHiErr_Array)
  twoSigma.SetName('twoSigma')
  observed = TGraphAsymmErrors(nPoints,xAxis_Array,obs_Array,zeros_Array,zeros_Array,zeros_Array,zeros_Array)
  if extraList:
    expectedEx  = []
    for expExArr in expEx_Array:
      expectedEx.append(TGraphAsymmErrors(nPoints,xAxis_Array,expExArr,zeros_Array,zeros_Array,zeros_Array,zeros_Array))
      print max([100.0*(i-j)/j for i,j in zip(expExArr,exp_Array)])


  #expected.Print()
  #raw_input()
  oneSigma.SetFillColor(kGreen)
  twoSigma.SetFillColor(kYellow)
  oneSigma.SetLineStyle(2)
  twoSigma.SetLineStyle(2)

  expected.SetMarkerColor(kBlack)
  expected.SetMarkerStyle(kFullCircle)
  expected.SetMarkerSize(1.5)
  expected.SetLineColor(kBlack)
  expected.SetLineWidth(2)
  expected.SetLineStyle(2)

  observed.SetLineWidth(2)

  if extraList:
    for i, graph in enumerate(expectedEx):
      graph.SetLineColor(kBlue+10*i)
      graph.SetLineWidth(2)
  mg.Add(twoSigma)
  mg.Add(oneSigma)
  mg.Add(expected)
  if not extraList and doObs:
    mg.Add(observed)
  elif extraList:
    for graph in expectedEx:
      mg.Add(graph)
  else:
    print 'no obs'

  mg.Draw('AL3')
  if 'Narrow' in suffix:
    mg.SetMinimum(0.005)
  else:
    mg.SetMinimum(0.15)

  mg.GetXaxis().SetTitleFont(42)
  mg.GetYaxis().SetTitleFont(42)
  mg.GetXaxis().SetLabelFont(42)
  mg.GetYaxis().SetLabelFont(42)
  #mg.Draw('Asame')
  if cfl.highMass:
    mg.GetXaxis().SetTitle('m_{A} (GeV)')
  else:
    mg.GetXaxis().SetTitle('m_{H} (GeV)')
  if cfl.modelIndependent:
    mg.GetYaxis().SetTitle('#sigma(gg#rightarrowA)#timesBR(A#rightarrowZ#gamma#rightarrowll#gamma) (fb)')
  else:
    mg.GetYaxis().SetTitle('95% CL limit on #sigma/#sigma_{SM}')
  mg.GetXaxis().SetLimits(massList[0],massList[-1]);
  c.RedrawAxis()

  mg.GetXaxis().SetTitleOffset(0.8)
  mg.GetYaxis().SetTitleOffset(0.85)
  mg.GetYaxis().CenterTitle()


  leg  = TLegend(0.60,0.65,0.98,0.85)
  leg.SetTextFont(42)
  leg.SetFillColor(0)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  if 'Narrow' in suffix:
    leg.SetHeader('Narrow signal model')
  else:
    leg.SetHeader('Broad signal model')
  leg.AddEntry(observed, "Observed",'l')
  leg.AddEntry(oneSigma,"Expected #pm 1 #sigma",'fl')
  leg.AddEntry(twoSigma,"Expected #pm 2 #sigma",'fl')
  leg.SetTextSize(0.042)
  leg.Draw()

  #cmsText = TLatex()
  #cmsText.SetNDC()
  #cmsText.SetTextSize(0.06)
  #cmsText.SetTextFont(61)
  #cmsText.DrawLatex(0.2,0.89, 'CMS')
  #cmsText.Draw()

  #prelimText = TLatex()
  #prelimText.SetNDC()
  #prelimText.SetTextSize(0.055)
  #prelimText.SetTextFont(52)
  #prelimText.DrawLatex(0.2,0.89, 'Preliminary')
  #prelimText.Draw()
  CMS_lumi.relPosX = 0.08
  CMS_lumi.CMS_lumi(c,2,11)

  if extraSuffix == None and not doObs: extraSuffix = 'noObs'
  global syst
  if syst == False: syst = 'nosyst'
  saveNames = ['limitPlot']
  for saveName in [CardOutput, suffix, YR, sigFit, extraSuffix, syst]:
    if type(saveName) == str:
      saveNames.append(saveName)

  c.Print('debugPlots/limitPlots/'+'_'.join(saveNames)+'.pdf')


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
    if syst == False: cardName = 'Output'+cardName[3:]+'_nosyst'
    else: cardName = 'Output'+cardName[3:]
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



