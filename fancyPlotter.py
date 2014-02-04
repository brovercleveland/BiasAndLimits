#!/usr/bin/env python
import sys
import os
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
#from rooFitBuilder import *

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()
gStyle.SetOptStat(0)
#RooDataSet.setDefaultStorageType(RooAbsData.Tree)

def Cat0SignalComps(bgFiles = [TFile('specialFiles/BaselineMassTrees.root','r'),
  TFile('specialFiles/MVAMassTrees.root','r'),
  TFile('specialFiles/MEMassTrees.root','r')] ):
  scale = 19.52*0.00154*0.10098*1000
  scale = 100000/scale
  scale = (19.672)/scale

  c = TCanvas("c","c",0,0,500,400)
  c.cd()

  histList = []
  for i,bgFile in enumerate(bgFiles):
    histList.append(TH1F('histo'+str(i), 'histo'+str(i), 45, 100, 190))
    if i == 0:
      SignalTree = bgFile.Get('m_llg_Signal2012ggM125')
      #SignalTree.Draw('m_llg_Signal2012ggM125*unBinnedWeight_Signal2012ggM125>>histo'+str(i))
      SignalTree.Draw('m_llg_Signal2012ggM125>>histo'+str(i))
    else:
      SignalTree = bgFile.Get('m_llg_Signal2012ggM125NLOp8')
      #SignalTree.Draw('m_llg_Signal2012ggM125NLOp8*unBinnedWeight_Signal2012ggM125NLOp8>>histo'+str(i))
      SignalTree.Draw('m_llg_Signal2012ggM125NLOp8>>histo'+str(i))
  leg = MakeLegend()
  for i,hist in enumerate(histList):
    hist.SetMarkerSize(0.7)
    hist.SetLineWidth(2)
    hist.Scale(scale)
    print hist.Integral()+hist.Integral()*0.1
    raw_input()

    if i == 0:
      hist.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
      hist.GetYaxis().SetTitle('Events')
      hist.Draw('hist')
      leg.AddEntry(hist, 'Baseline','l')
      print 'case 0'
    elif i == 1:
      hist.SetMarkerStyle(21)
      hist.SetMarkerColor(kGreen+2)
      hist.SetLineColor(kGreen+2)
      hist.Draw('sameshist')
      leg.AddEntry(hist, 'MVA','l')
      print 'case not 0'
    elif i == 2:
      hist.SetMarkerStyle(22)
      hist.SetMarkerColor(kOrange+2)
      hist.SetLineColor(kOrange+2)
      hist.Draw('sameshist')
      leg.AddEntry(hist, 'ME','l')
  title = TPaveText(0.2,0.92,0.8,1.0,'brNDC')
  title.SetBorderSize(0)
  title.SetFillStyle(0)
  title.SetFillColor(0)
  title.SetTextFont(42)
  title.SetTextSize(0.035)
  title.AddText('CMS #sqrt{s} = 8 TeV, 19.7 fb^{-1}')
  title.Draw()
  leg.Draw()
  #testFrame.Draw()
  if not os.path.isdir('prettyPlots'): os.mkdir('prettyPlots')
  c.Print('prettyPlots/SignalComp.pdf')

def MakeLegend(x1 = None, y1 = None, x2 = None, y2 = None):
  if x1 == y1 == x2 == y2 == None:
    x1 = 0.80
    y1 = 0.73
    x2 = 0.945
    y2 = 0.92
  leg = TLegend(x1,y1,x2,y2,'',"brNDC")
  leg.SetBorderSize(1)
  leg.SetTextSize(0.03)
  leg.SetFillColor(0)
  leg.SetFillStyle(0)
  return leg

def LumiXSScale(self,name):
  '''Outputs scale for MC with respect to lumi and XS'''

  if name is 'DATA': return 1

  lumi = 0
  if self.lepton is 'mu': lumi = 19.672
  elif self.lepton is 'el': lumi = 19.711
  else: raise NameError('LumiXSScale lepton incorrect')

  scaleDict = AutoVivification()

  scaleDict['2012']['DYJets'] = 3503.71*1000
  scaleDict['2012']['ZGToLLG'] = 156.2*1000
  scaleDict['2012']['gg']['125'] = 19.52*0.00154*0.10098*1000

  initEvents = self.thisFile.GetDirectory('Misc').Get('h1_acceptanceByCut_'+name).Integral(1,1)
  if 'Signal' in name:
    sig = name[10:].partition('M')[0]
    mass = name[10:].partition('M')[-1][0:3]
    scale = initEvents/scaleDict[self.year][sig][mass]
  else:
    scale = initEvents/scaleDict[self.year][name]
  scale = lumi/scale
  return scale


if __name__ == '__main__':
  #Cat0BGComps()
  Cat0SignalComps()
