#!/usr/bin/env python
import sys
sys.argv.append('-b')
import os
from ROOT import *
from collections import defaultdict
gROOT.ProcessLine('.L ./tdrstyle.C')
setTDRStyle()

def loopThruPulls():
  yearList = ['2012']
  leptonList = ['el','mu']
  genFuncList = ['GaussPow','GaussExp','SechPow','SechExp']
  #catList = ['1','2','3','4']
  catList = ['0']
  massList = ['120','125','130','135','140','145','150','155','160']
  for year in yearList:
    for lepton in leptonList:
      for genFunc in genFuncList:
        for cat in catList:
          for mass in massList:
            makePullPlots(year,lepton,genFunc,cat,mass)

def makePullPlots(year, lepton, genFunc, cat, mass):

  #get the toy file and tree

  toyFileName = 'batchOutput/'+lepton+'_'+year+'/'+lepton+'_toys_4cat_preapproval_gen'+genFunc+'_cat'+str(cat)+'_mH'+mass+'_merged.root'
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
  #define the fit functions we'll be using today (and their associated plot colors)

  #turnOnList = ['Sech','Gauss']
  turnOnList = ['Gauss']
  tailList = ['Bern3','Bern4','Bern5']
  colorDict = {'SechBern3':kCyan,'SechBern4':kCyan+1,'SechBern5':kCyan+2,'SechBern6':kCyan+3,
      'GaussBern3':kRed,'GaussBern4':kRed+1,'GaussBern5':kRed+2,'GaussBern6':kRed+3}

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
  for turnOn in turnOnList:
    for tail in tailList:
      fitFunc = turnOn+tail
      cutStr = 'stat'+fitFunc+'==0&&covQual'+fitFunc+'>=1'
      if (mass is '120') and (lepton is 'el') and ('GaussBern5' in fitFunc) and (genFunc is 'SechPow'):
        print 'ok'
        raw_input()
        cutStr = cutStr+'&&fitbkg'+fitFunc+'err>42'
      elif genFunc is 'GaussPow' and 'GaussBern5' in fitFunc and int(mass) < 140:
        cutStr = cutStr+'&&fitbkg'+fitFunc+'err>40'
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
          tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, 0, 200)
        elif dist in ['nSig','nBG']:
          tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, -200, 200)
        elif dist == 'typeA':
          tmpHist = TH1F(dist+'_'+fitFunc, dist+'_'+fitFunc, 100, -10, 10)

        tmpHist.SetLineWidth(2)
        tmpHist.SetLineColor(colorDict[fitFunc])
        tmpHist.SetTitle(dist)
        canList[i].cd()

        #build the histos

        if dist == 'sigPull':
          toyTree.Draw('(yield.fitsig'+fitFunc+'/yield.fitsig'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('nSig/#sigma(nSig)')
        elif dist == 'bgPull':
          toyTree.Draw('((yield.fitbkg'+fitFunc+'-genbkg)/yield.fitbkg'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('nBG/#sigma(nBG)')
        elif dist == 'nSig':
          toyTree.Draw('(yield.fitsig'+fitFunc+')>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('nSig')
        elif dist == 'nBG':
          toyTree.Draw('(yield.fitbkg'+fitFunc+'-genbkg)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('nBG')
        elif dist == 'sigErr':
          toyTree.Draw('(yield.fitsig'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('#sigma(nSig)')
        elif dist == 'bgErr':
          toyTree.Draw('(yield.fitbkg'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('#sigma(nBG)')
        elif dist == 'typeA':
          toyTree.Draw('(yield.fitsig'+fitFunc+'/yield.fitbkg'+fitFunc+'err)>>'+dist+'_'+fitFunc ,cutStr,'goff')
          tmpHist.GetXaxis().SetTitle('nSig/#sigma(nBG)')

        tmpHist.GetYaxis().SetTitle('A.U.')
        tmpHist.GetYaxis().CenterTitle()

        print fitFunc,dist,tmpHist.GetEntries()
        if(tmpHist.Integral()>0): tmpHist.Scale(1./tmpHist.Integral())

        histListDict[dist].append(tmpHist)
        legList[i].AddEntry(tmpHist,fitFunc+': #mu={0:.2f}, #sigma={1:.2f}'.format(tmpHist.GetMean(), tmpHist.GetRMS()),'l')


  #make the plots

  if not os.path.isdir('pullPlotDir/'+lepton+'_'+year):
    os.makedirs('pullPlotDir/'+lepton+'_'+year)

  #get a txt file ready for the latex
  f = open('pullPlotDir/'+lepton+'_'+year+'/'+lepton+'_'+year+'_'+genFunc+'_cat'+cat+'_mH'+mass+'.txt', 'w')
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
    canList[i].Print('pullPlotDir/'+lepton+'_'+year+'/'+dist+'_'+lepton+'_'+year+'_'+genFunc+'_cat'+cat+'_mH'+mass+'.pdf')

    if dist == 'typeA':
      f.write('typeA:\n')
      for hist in histListDict[dist]:
        f.write(hist.GetName().strip('typeA_')+', ')
      f.write('\n')
      for hist in histListDict[dist]:
        f.write('{0:.2f}, '.format(hist.GetMean()))
      f.write('\n')
    if dist == 'bgPull':
      f.write('bgPull:\n')
      for hist in histListDict[dist]:
        f.write(hist.GetName().strip('bgPull_')+', ')
      f.write('\n')
      for hist in histListDict[dist]:
        f.write('{0:.2f}, '.format(hist.GetMean()))
      f.write('\n')
  f.close()


if __name__=="__main__":
  if len(sys.argv) == 2:
    loopThruPulls()
  elif len(sys.argv) != 7:
    print 'args: year, lepton, genfunc, cat, mass'
  else:
    a,b,c,d,e = sys.argv[1:6]
    makePullPlots(a,b,c,d,e)










