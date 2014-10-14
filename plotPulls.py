#!/usr/bin/env python
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys, os
import argparse
from ROOT import *
from collections import defaultdict
from rooFitBuilder import FitBuilder
import configLimits as cfl
gROOT.ProcessLine('.L ./tdrstyle.C')
setTDRStyle()

YR = cfl.YR
sigFit = cfl.sigFit
highMass = cfl.highMass
genFuncs = cfl.genFuncs
testFuncs = cfl.testFuncs
suffix = cfl.suffix

def getArgs():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v","--verbose",action = "store_true")
  group.add_argument("-q","--quiet",action = "store_true")
  subparser = parser.add_subparsers(dest = 'command')
  parser_a = subparser.add_parser("all", help="Loop through all of the tev, lepton, cat, genFunc, mass")
  #parser_a.add_argument("--all", help="Loop through all of the tev, lepton, cat, genFunc, mass", action="store_true")
  parser_b = subparser.add_parser("single", help="Only plot a single set of bias studies")
  parser_b.add_argument("--tev", help="CoM Energy", default = cfl.tevList[0], choices = ['7TeV','8TeV'] )
  parser_b.add_argument("--lepton", help="Lepton Flavor", default = cfl.leptonList[0], choices = ['mu','el'])
  parser_b.add_argument("--cat", help="Cat Number", default = cfl.catListSmall[0], type = int)
  parser_b.add_argument("--genFunc", help="PDF used to generate toy data", default = cfl.genFuncs[0], type = str)
  parser_b.add_argument("--mass", help="Mass of signal template", default = cfl.massList[0], type = int)
  args = parser.parse_args()
  return args

def makePullPlots(tev,lepton, cat, genFunc, mass):

  #get the toy file and tree
  biasPath = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'
  biasPath = biasPath+suffix+'_'+YR+'_'+sigFit+'/biasStudy'
  toyFileName = biasPath+'/combine/'+'_'.join(['combined',tev,lepton,cat,genFunc,mass])+'.root'

  print toyFileName
  toyFile = TFile(toyFileName)
  toyTree = toyFile.Get('toys')

  gStyle.SetOptStat(0)
  gStyle.SetTitleFontSize(2.7)
  gStyle.SetTitleH(0.08) # Set the height of the title box
  gStyle.SetTitleW(1)    # Set the width of the title box
  gStyle.SetTitleX(0)    # Set the position of the title box
  gStyle.SetTitleY(0.99)    # Set the position of the title box
  gStyle.SetLineWidth(2)


  #make a TCanvas and TLegend for each type of distribution

  distList = ['sigPull','bgPull','nSig','nBG','sigErr','bgErr','typeA']
  canList = []
  legList = []
  for dist in distList:
    canvasTmp = TCanvas(dist+'Can',dist+'Can',900,700)
    canList.append(canvasTmp)

    legendTmp = TLegend(0.6,0.55,1.0,0.9)
    legendTmp.SetFillColor(0)
    #legendTmp.SetFillStyle(0)
    legendTmp.SetTextSize(0.03)
    legList.append(legendTmp)

  #this is a dictionary where each key is the distribution string, and each value is the list of histograms associated with that dist
  histListDict = defaultdict(list)

  #start the main loop and make all the histos

  # build the fit func name
  for fitFunc in testFuncs:
    cutStr = ''
    #cutStr = 'stat'+fitFunc+'==0&&covQual'+fitFunc+'>=1'
    if (mass == '400') and (lepton == 'el') and ('TripExpSum' == fitFunc):
      cutStr = cutStr+fitFunc+'.yieldBkgErr>2'
    elif (mass == '450') and (lepton == 'el') and ('TripExpSum' == fitFunc):
      cutStr = cutStr+fitFunc+'.paramP3Err<1.2'
    #elif genFunc is 'GaussPow' and 'GaussBern5' in fitFunc and int(mass) < 140:
    #  cutStr = cutStr+'&&fitbkg'+fitFunc+'err>40'
    #elif '130' is mass:
      #  cutStr = cutStr+'&&fitbkg'+fitFunc+'err>25'
    #else:
      #   cutStr = cutStr+'&&fitbkg'+fitFunc+'err>20'
    #if fitFunc != 'GaussBern5': continue

    #go through all the distributions you want
    for i,dist in enumerate(distList):

      if dist in ['sigPull','bgPull']:
        tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, -6, 6)
      elif dist in ['sigErr','bgErr']:
        tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, 0, 50)
      elif dist in ['nSig','nBG']:
        tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, -200, 200)
      elif dist == 'typeA':
        tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, -10, 10)

      tmpHist.SetLineWidth(2)
      tmpHist.SetLineColor(FitBuilder.FitColorDict[fitFunc])
      tmpHist.SetTitle(dist)
      canList[i].cd()

      #build the histos

      if dist == 'sigPull':
        #toyTree.Draw('(yield.fitsig'+fitFunc+'/yield.fitsig'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        toyTree.Draw('('+fitFunc+'.yieldSig/'+fitFunc+'.yieldSigErr)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('nSig/#sigma(nSig)')
      elif dist == 'bgPull':
        toyTree.Draw('(('+fitFunc+'.yieldBkg-toyData.sigWindowData)/'+fitFunc+'.yieldBkgErr)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('nBG/#sigma(nBG)')
      elif dist == 'nSig':
        toyTree.Draw('('+fitFunc+'.yieldSig)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('nSig')
      elif dist == 'nBG':
        toyTree.Draw('('+fitFunc+'.yieldBkg-toyData.sigWindowData)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('nBG')
      elif dist == 'sigErr':
        toyTree.Draw('('+fitFunc+'.yieldSigErr)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('#sigma(nSig)')
      elif dist == 'bgErr':
        toyTree.Draw('('+fitFunc+'.yieldBkgErr)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('#sigma(nBG)')
      elif dist == 'typeA':
        toyTree.Draw('('+fitFunc+'.yieldSig/'+fitFunc+'.yieldBkgErr)>>'+dist+'_'+fitFunc ,cutStr,'goff')
        tmpHist.GetXaxis().SetTitle('nSig/#sigma(nBG)')

      tmpHist.GetYaxis().SetTitle('A.U.')
      tmpHist.GetYaxis().CenterTitle()

      print fitFunc,dist,tmpHist.GetEntries()
      if(tmpHist.Integral()>0): tmpHist.Scale(1./tmpHist.Integral())

      histListDict[dist].append(tmpHist)
      legList[i].AddEntry(tmpHist,fitFunc+': #mu={0:.2f}, #sigma={1:.2f}'.format(tmpHist.GetMean(), tmpHist.GetRMS()),'l')


  #make the plots

  plotDir = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/biasPulls'
  if not os.path.isdir(plotDir): os.mkdir(plotDir)

  #get a txt file ready for the latex
  biasPathText = biasPath.rstrip('biasStudy')+mass+'.0/biasOutput'
  if not os.path.isdir(biasPathText): os.mkdir(biasPathText)

  with open(biasPathText+'/'+'_'.join(['rawText',tev,lepton,'cat'+cat, genFunc])+'.txt','w') as f:
    for i,dist in enumerate(distList):
      canList[i].cd()

      ymax = max(map(lambda x:x.GetMaximum(),histListDict[dist]))*1.1 #this is awesome if it works, python rocks

      histListDict[dist][0].Draw()
      histListDict[dist][0].SetMaximum(ymax)
      print  histListDict[dist][0]
      #raw_input()
      for j in range(1,len(histListDict[dist])):
        histListDict[dist][j].Draw('same')
      legList[i].Draw('same')
      canList[i].Print(plotDir+'/'+'_'.join([dist,tev,lepton,'cat'+cat, genFunc,'M'+mass])+'.pdf')

      if dist == 'typeA':
        f.write('typeA:\n')
        for hist in histListDict[dist]:
          f.write(hist.GetName().replace('typeA_','')+', ')
        f.write('\n')
        for hist in histListDict[dist]:
          f.write('{0:.2f}, '.format(hist.GetMean()))
        f.write('\n')
      if dist == 'bgPull':
        f.write('bgPull:\n')
        for hist in histListDict[dist]:
          f.write(hist.GetName().replace('bgPull_','')+', ')
        f.write('\n')
        for hist in histListDict[dist]:
          f.write('{0:.2f}, '.format(hist.GetMean()))
        f.write('\n')

  for can in canList:
    can.IsA().Destructor(can)
  for leg in legList:
    leg.IsA().Destructor(leg)
  for dist in histListDict:
    for hist in histListDict[dist]:
      hist.IsA().Destructor(hist)
  toyFile.Close()

if __name__=="__main__":
  args = getArgs()
  if args.command == 'single':
    makePullPlots(args.tev,args.lepton,str(args.cat),args.genFunc,str(args.mass))
  elif args.command == 'all':
    for tev in cfl.tevList:
      for lepton in cfl.leptonList:
        for cat in cfl.catListSmall:
          for func in cfl.genFuncs:
            for mass in cfl.massList:
              print tev, lepton, cat, func, mass
              makePullPlots(tev, lepton, cat,func, mass)










