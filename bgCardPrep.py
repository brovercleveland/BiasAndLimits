#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import configLimits as cfl
import CMS_lumi

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

doMVA = cfl.doMVA
doExt = cfl.doExt
suffixCard = cfl.suffixPostFix

leptonList = cfl.leptonList
tevList = cfl.tevList
catListSmall = cfl.catListSmall
catListBig = cfl.catListBig

YR = cfl.YR
sigFit = cfl.sigFit
highMass = cfl.highMass
blind = cfl.blind
doFancy = cfl.doFancy


#rooWsFile = TFile('testRooFitOut_Poter.root')
rooWsFile = TFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffixCard+'.root')
myWs = rooWsFile.Get('ws')
card_ws = RooWorkspace('ws_card')
#card_ws.autoImportClassCode(True)

c = TCanvas("c","c",0,0,500,400)
c.cd()
mzg = myWs.var('CMS_hzg_mass')
mzg.setRange('signal',120,130)

########################################
# prep the background and data card    #
# we're going to the extend the bg pdf #
# and rename the parameters to work    #
# with the higgs combination tool      #
########################################


for tev in tevList:
  for lepton in leptonList:
    if tev == '8TeV' and doMVA: catList = catListBig
    else: catList = catListSmall
    for cat in catList:
      if cat is '5' and tev is '7TeV' and lepton is 'mu': continue
      elif cat is '5' and tev is '7TeV' and lepton is 'el': lepton = 'all'

      dataName = '_'.join(['data',lepton,tev,'cat'+cat])
      suffix = '_'.join([tev,lepton,'cat'+cat])

      fitNameHeader = cfl.bgLimitDict[highMass][tev][lepton][cat]
      #fitNameHeader = 'ExpSum'
      fitName = fitNameHeader+'_'+suffix
      normName = 'norm'+fitName

      data = myWs.data(dataName)
      fit = myWs.pdf(fitName)
      fit.Print()

      ###### Extend the fit (give it a normalization parameter)
      print dataName
      sumEntries = data.sumEntries()
      sumEntriesS = data.sumEntries('1','signal')
      print sumEntries, sumEntriesS
      #raw_input()
      dataYieldName = '_'.join(['data','yield',lepton,tev,'cat'+cat])
      dataYield = RooRealVar(dataYieldName,dataYieldName,sumEntries)
      if doExt:
        norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.1,sumEntries*2)
        print 'start', norm.getVal()
        fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
        fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)
        #fit_ext = fit

        fit_ext.fitTo(data,RooFit.Range('fullRegion'))

        testFrame = mzg.frame()
        data.plotOn(testFrame)
        fit_ext.plotOn(testFrame)
        testFrame.Draw()
        c.Print('debugPlots/'+'_'.join(['test','data','fit',lepton,tev,'cat'+cat])+'.pdf')
        print 'end', norm.getVal()
      else:
        norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.1,sumEntries*5)
        #norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.8,sumEntries*1.2)


      ###### Import the fit and data, and rename them to the card convention

      dataNameNew = '_'.join(['data','obs',lepton,tev,'cat'+cat])
      dataYieldNameNew = '_'.join(['data','yield',lepton,tev,'cat'+cat])
      dataYield.SetName(dataYieldNameNew)

      getattr(card_ws,'import')(data,RooFit.Rename(dataNameNew))
      if doExt:
        getattr(card_ws,'import')(fit_ext)
      else:
        getattr(card_ws,'import')(fit)
        normNameFixed  = '_'.join(['bkg',lepton,tev,'cat'+cat,'norm'])
        norm.SetName(normNameFixed)
        getattr(card_ws,'import')(norm)
      getattr(card_ws,'import')(dataYield)
      card_ws.commitTransaction()
      #fit_ext.Print()
      fitBuilder = FitBuilder(mzg,tev,lepton,cat)
      fitBuilder.BackgroundNameFixer(card_ws,fitNameHeader,doExt)

      if doFancy:
        c.SetTopMargin(0.075);
        ######################
        # making fancy plots #
        ######################

        fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
        fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)
        #fit_res = fit_ext.fitTo(data,RooFit.Range('fullRegion'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minos(RooArgSet(norm)), RooFit.Minimizer("Minuit2"))
        #fit_res = fit_ext.fitTo(data,RooFit.Range('fullRegion'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minos(RooArgSet(norm)), RooFit.Minimizer("Minuit"))
        fit_res = None
        if lepton == 'mu' or lepton == 'el':
          fit_res = fit_ext.fitTo(data,RooFit.Range('fullRegion'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.InitialHesse(True), RooFit.Minos(True), RooFit.Minimizer("Minuit"))
        else:
          #fit_res = fit_ext.fitTo(data,RooFit.Range('fullRegion'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minimizer("Minuit2"))
          fit_res = fit_ext.fitTo(data,RooFit.Range('fullRegion'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended())

        testFrame = mzg.frame()
        binning = (cfl.bgRange[1]-cfl.bgRange[0])/20

        if blind:
          data.plotOn(testFrame,RooFit.Binning(3,cfl.bgRange[0],cfl.blindRange[1]),RooFit.Name('data'),RooFit.MarkerSize(0.5))
          data.plotOn(testFrame,RooFit.Binning(5,cfl.blindRange[1],cfl.bgRange[1]),RooFit.Name('data'), RooFit.MarkerSize(0.5))
          data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.Invisible())
        else:
          data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.MarkerSize(0.5),RooFit.XErrorSize(0))

        linearInterp = True
        if lepton == 'el' or lepton == 'mu': linearInterp = False
        #fit_ext.plotOn(testFrame, RooFit.Name(fitExtName+"2sigma"),
        #           RooFit.VisualizeError(fit_res,RooArgSet(norm),2,False), RooFit.FillColor(kYellow),RooFit.LineColor(kBlack))
        fit_ext.plotOn(testFrame, RooFit.Name(fitExtName+"2sigma"),
                   RooFit.VisualizeError(fit_res,2, linearInterp), RooFit.FillColor(kYellow),RooFit.LineColor(kBlack))
        #fit_ext.plotOn(testFrame, RooFit.Name(fitExtName+"1sigma"),
        #           RooFit.VisualizeError(fit_res,RooArgSet(norm),1,False), RooFit.FillColor(kGreen), RooFit.LineColor(kBlack))
        fit_ext.plotOn(testFrame, RooFit.Name(fitExtName+"1sigma"),
                   RooFit.VisualizeError(fit_res,1, linearInterp), RooFit.FillColor(kGreen), RooFit.LineColor(kBlack))
        fit_ext.plotOn(testFrame, RooFit.Name(fitExtName), RooFit.LineColor(kBlue), RooFit.LineWidth(1))
        #fit_ext.paramOn(testFrame,RooFit.ShowConstants(True), RooFit.Layout(0.6, 1.0, 0.98))
        #testFrame.getAttText().SetTextSize(0.021)

        if blind:
          data.plotOn(testFrame,RooFit.Binning(3,cfl.bgRange[0],cfl.blindRange[1]),RooFit.Name('data'),RooFit.MarkerSize(0.5))
          data.plotOn(testFrame,RooFit.Binning(5,cfl.blindRange[1],cfl.bgRange[1]),RooFit.Name('data'), RooFit.MarkerSize(0.5))
          data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.Invisible())
        else:
          data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.MarkerSize(0.5),RooFit.XErrorSize(0))

        #if hjp:
        #  testFrame.SetMaximum(12)
        #elif cat in ['0']:
        #  testFrame.SetMaximum(82)
        #elif cat in ['m1','m2','m3','m4','m5','m6']:
        #  testFrame.SetMaximum(22)
        #elif cat in ['m7']:
        #  testFrame.SetMaximum(42)
        #else:
        #  testFrame.SetMaximum(65)

        testFrame.Draw()
        #hsig[0].SetAxisRange(115,135,"X")
        #hsig[0].SetLineColor(kRed+1)
        #hsig[0].SetLineWidth(2)
        #hsig[0].Draw('same hist')
        testFrame.SetMinimum(0.1)
        c.SetLogy()


        if lepton=='mu':
          testFrame.SetTitle(";m_{#mu#mu#gamma} (GeV);Events/"+str(20)+" GeV")
        elif lepton=='el':
          testFrame.SetTitle(";m_{ee#gamma} (GeV);Events/"+str(20)+" GeV")
        testFrame.GetYaxis().CenterTitle()
        testFrame.GetXaxis().SetTitleOffset(0.8)
        testFrame.GetYaxis().SetTitleOffset(0.85)

        #if hjp: leg  = TLegend(0.45,0.62,0.91,0.87)
        #leg  = TLegend(0.46,0.73,0.80,0.95)
        #leg.SetFillColor(0)
        #leg.SetFillStyle(0)
        #leg.SetBorderSize(0)
        ##leg.AddEntry(hsig[0],'Expected signal x'+str(factor),'f')
        ##leg.AddEntry(testFrame.findObject(bkgModel+'1sigma'),"Background Model",'f')
        #leg.AddEntry(testFrame.findObject(fitExtName),"Background Model",'l')
        #leg.AddEntry(data,'Data','lep')
        #leg.SetTextSize(0.042)
        #leg.Draw()

        #leg2  = TLegend(0.70,0.70,0.98,0.8)
        #leg2.SetNColumns(2)
        #leg2.SetFillColor(0)
        #leg2.SetFillStyle(0)
        #leg2.SetBorderSize(0)
        #leg2.AddEntry(c.findObject(fitExtName+'1sigma'),"#pm 1 #sigma",'f')
        #leg2.AddEntry(c.findObject(fitExtName+'2sigma'),"#pm 2 #sigma",'f')
        #leg2.SetTextSize(0.042)
        #leg2.Draw()

        leg  = TLegend(0.2,0.2,0.6,0.45)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        if lepton=='el':
          leg.SetHeader('A #rightarrowZ#gamma#rightarrow ee#gamma')
        else:
          leg.SetHeader('A #rightarrowZ#gamma#rightarrow#mu#mu#gamma')
        leg.AddEntry(testFrame.findObject(fitExtName),"Background Model",'l')
        leg.AddEntry(testFrame.findObject(fitExtName+'1sigma'),"#pm 1 #sigma",'f')
        leg.AddEntry(testFrame.findObject(fitExtName+'2sigma'),"#pm 2 #sigma",'f')
        leg.SetTextSize(0.042)
        leg.Draw()

        #lat1 = TLatex()
        #lat1.SetNDC()
        #lat1.SetTextSize(0.040)
        #if lepton=='el':
        #  lat1.DrawLatex(0.18,0.95, 'A #rightarrowZ#gamma#rightarrow ee#gamma')
        #else:
        #  lat1.DrawLatex(0.18,0.95, 'A #rightarrowZ#gamma#rightarrow#mu#mu#gamma')

        #lat2 = TLatex()
        #lat2.SetNDC()
        #lat2.SetTextSize(0.040)
        #lat2.DrawLatex(0.40,0.95, 'CMS Preliminary')

        #CMS_lumi.relPosX = 0.08
        CMS_lumi.CMS_lumi(c,2,33)

        gPad.RedrawAxis()
        if blind:
          c.Print('debugPlots/fancyPlots/'+'_'.join(['PAS','fit','blind',suffixCard,tev,lepton,'cat'+cat])+'.pdf')
        else:
          c.Print('debugPlots/fancyPlots/'+'_'.join(['PAS','fit',suffixCard,tev,lepton,'cat'+cat])+'.pdf')

card_ws.writeToFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/CardBackground_'+suffixCard+'.root')






