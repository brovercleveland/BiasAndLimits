#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
import math
#import pdb
from rooFitBuilder import *
from signalCBFits import AutoVivification
from xsWeighter import LumiXSWeighter

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()


def BGPlots():
  suffixCard = 'MVA_02-03-14'

  rooWsFile = TFile('testRooFitOut_'+suffixCard+'.root')
  myWs = rooWsFile.Get('ws')
  #leptonList = ['mu','el']
  leptonList = ['mu']
  yearList = ['2012']
  #catList = ['1','2','3','4','6','7','8','9']
  catList = ['1']
  dataDict = AutoVivification()
  fitDict = AutoVivification()

  h1 = TH1F("h1", "h1", 80, 100, 180);
  fit1 = TH1F("Fith", "", 100, 0, 100)
  fitSB1 = TH1F("FitSB", "", 100, 0, 100)
  chan1 = TLatex()
  L1 = TLatex()
  sigma1 = TH1F("Fits", "", 100, 0, 100)
  sigma2 = TH1F("Fit2", "", 100, 0, 100)
  leg1 = TLegend(0.37, 0.63, 0.94, 0.86)
  leg2 = TLegend(0.15, 0.70, 0.52, 0.85)

  h1Top = TH1F("h1Top", "h1", 80, 100, 180);
  fit1Top = TH1F("FithTop", "", 100, 0, 100)
  fitSB1Top = TH1F("FitSBTop", "", 100, 0, 100)
  chan1Top = TLatex()
  L1Top = TLatex()
  sigma1Top = TH1F("FitsTop", "", 100, 0, 100)
  sigma2Top = TH1F("Fit2Top", "", 100, 0, 100)
  leg1Top = TLegend(0.82, 0.70, 0.95, 0.85)
  h1Bottom = TH1F("h1Bottom", "h1", 80, 100, 180);
  fit1Bottom = TH1F("FithBottom", "", 100, 0, 100)
  fitSB1Bottom = TH1F("FitSBBottom", "", 100, 0, 100)
  chan1Bottom = TLatex()
  L1Bottom = TLatex()
  sigma1Bottom = TH1F("FitsBottom", "", 100, 0, 100)
  sigma2Bottom = TH1F("Fit2Bottom", "", 100, 0, 100)
  leg1Bottom = TLegend(0.34, 0.85, 0.53, 0.93)
  c = TCanvas("c","c",0,0,1200,1200)
  print c.GetLeftMargin()
  print c.GetRightMargin()
  c.SetLeftMargin(0.00)
  c.SetRightMargin(0.000)
  #raw_input()
  height = 1-c.GetTopMargin()-c.GetBottomMargin()

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

        dataDict[year][lepton][cat] = myWs.data(dataName)
        fitDict[year][lepton][cat] = myWs.pdf(fitName)


        mzg = myWs.var("CMS_hzg_mass")
        mzg.setBins(90)

        c.cd()
        frameTop = mzg.frame()
        frameTop.SetMinimum(0.00001)
        #if cats == '14': frameTop.SetYTitle("Events / 2 GeV")
        #else: frameTop.SetYTitle(" ")
        frameTop.SetYTitle("Events / 2 GeV")
        frameTop.GetXaxis().SetTitleSize(0)
        frameTop.GetXaxis().SetLabelSize(0)
        frameTop.GetYaxis().SetNdivisions(506)
        frameBottom = mzg.frame()
        frameBottom.SetMinimum(0.00001)
        frameBottom.GetYaxis().SetTitleSize(0)
        frameBottom.GetYaxis().SetNdivisions(506)

        pad1 = TPad()
        pad1.SetTicks(1, 1);
        pad1.Draw();
        pad1.SetBottomMargin(0.5*height+c.GetBottomMargin());
        pad1.SetFillStyle(4000);
        pad1.SetFillColor(kWhite);
        pad1.SetLeftMargin(0.10)
        pad1.SetRightMargin(0.03)

        pad2 = TPad()
        pad2.SetTicks(1, 1);
        pad2.Draw();
        pad2.SetTopMargin(0.5*height+c.GetTopMargin());
        pad2.SetFillStyle(4000);
        pad2.SetFillColor(kWhite);
        pad2.SetLeftMargin(0.10)
        pad2.SetRightMargin(0.03)

        pad1.cd()
        dataDict[year][lepton][cat].plotOn(frameTop, RooFit.Binning(45))
        fitDict[year][lepton][cat].plotOn(frameTop, RooFit.Range('fullRegion'), RooFit.LineWidth(2))
        #pdfTop.plotOn(frameTop, RooFit.Range('sigRegion'), RooFit.LineWidth(2))
        frameTop.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
        frameTop.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
        frameTop.GetYaxis().CenterTitle()
        frameTop.SetTitleOffset(0.975,"Y")
        frameTop.SetTitle('Test Plot {0} {1} {2}'.format(lepton,year,cat))
        frameTop.Draw()
        #if cat is '14' and not (year is '2012' and lepton is 'muons'):
        #  chi2 = frameTop.chiSquare(7)
        #else:
        #  chi2 = frameTop.chiSquare(8)
        #print 'Test Plot\t{0}\t{1}\t{2}\t{3}'.format(lepton,year,cat[0], chi2)
        #raw_input()

        onesigmaTop = TGraphAsymmErrors()
        twosigmaTop = TGraphAsymmErrors()
        tmpCurveTop = RooCurve(frameTop.getObject(int(frameTop.numItems())-1))
        doBandsFit(onesigmaTop, twosigmaTop, mzg, fitDict[year][lepton][cat], tmpCurveTop, dataDict[year][lepton][cat], frameTop, year, lepton)
        twosigmaTop.SetLineColor(kYellow)
        twosigmaTop.SetFillColor(kYellow)
        twosigmaTop.SetMarkerColor(kYellow)
        onesigmaTop.SetLineColor(kGreen)
        onesigmaTop.SetFillColor(kGreen)
        onesigmaTop.SetMarkerColor(kGreen)

        frameTop.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
        h1Top.SetMarkerStyle(20)
        h1Top.SetMarkerColor(kBlack)
        h1Top.SetLineColor(1)
        frameTop.Draw("e0")
        frameTop.SetTitle("")
        twosigmaTop.Draw("L3 same")
        onesigmaTop.Draw("L3 same")
        frameTop.Draw("e0same")
        #allSigTop.Scale(75)
        #allSigTop.Rebin(2)
        #allSigTop.SetLineColor(kRed)
        #allSigTop.SetLineWidth(2)
        #allSigTop.Draw('samehist')

        L1Top.SetNDC()
        L1Top.SetTextSize(0.045)
        L1Top.SetTextFont(62)
        #if cat == '14' and year == '2011': L1Top.DrawLatex(0.8, 0.9, ('Class 1'))
        if cat == '1' and year == '2011': L1Top.DrawLatex(0.8, 0.9, ('Class 1'))
        elif cat == '14' and year == '2012': L1Top.DrawLatex(0.8, 0.9, ('Class 1'))
        elif cat == '23': L1Top.DrawLatex(0.8, 0.9, ('Class 3'))
        chan1Top.SetNDC()
        chan1Top.SetTextSize(0.045)
        chan1Top.SetTextFont(62)
        if year == '2011' and cat == '14':
          chan1Top.DrawLatex(0.10, 0.96, ("CMS"))
          chan1Top.DrawLatex(0.57, 0.96, "#sqrt{s} = 7 TeV, L = 5 fb^{-1}");
          if lepton == 'electrons' and cat == '14': chan1Top.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
          elif lepton == 'muons' and cat == '14': chan1Top.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
        elif year == '2012' and cat == '14':
          chan1Top.DrawLatex(0.10, 0.96, ("CMS"))
          chan1Top.DrawLatex(0.51, 0.96, "#sqrt{s} = 8 TeV, L = 19.6 fb^{-1}");
          if lepton == 'electrons' and cat == '14': chan1Top.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
          elif lepton == 'muons' and cat == '14': chan1Top.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
        fit1Top.SetLineColor(kBlue)
        fit1Top.SetLineWidth(2)
        fitSB1Top.SetLineColor(kBlue)
        fitSB1Top.SetLineWidth(2)
        sigma1Top.SetFillColor(kGreen)
        sigma1Top.SetLineWidth(2)
        sigma2Top.SetFillColor(kYellow)
        sigma2Top.SetLineWidth(2)
        leg1Top.SetFillColor(0)
        leg1Top.SetFillStyle(0)
        leg1Top.SetShadowColor(0)
        leg1Top.SetBorderSize(0)
        leg1Top.SetTextFont(62)
        leg1Top.SetTextSize(0.047)
        leg1Top.AddEntry(h1Top, "Data", "pl")
        leg1Top.AddEntry(sigma1Bottom, "#pm 1 #sigma", "f")
        leg1Top.AddEntry(sigma2Bottom, "#pm 2 #sigma", "f")
        #leg1Top.AddEntry(allSignal, "Signal m_{H} = 125 GeV x 100", "l")
        #if cat == '14' and year == '2012': leg1Top.Draw()
        if cat == '14' and year == '2012': leg1Top.Draw()
        #cTop.Print('prettyPlots/testPlot_'+lepton+'_'+year+'_'+cat+'.root')
        c.Print('prettyPlots/testPlot_'+lepton+'_'+year+'_'+cat+'.pdf')
        leg1Top.Clear()
        pad1.Clear()
        c.Clear()

        pad1.Close()
        print 'bottom of loop'


def doBandsFit(onesigma, twosigma, hmass, cpdf, nomcurve, datanorm, plot, year, lepton):

  print 'starting bands'
  nlim = RooRealVar("nlim","",0,0,1e+5)
  print 'total steps needed:', plot.GetXaxis().GetNbins()
  oldhi = oldlo = 9999
  for i in range(1,plot.GetXaxis().GetNbins()+1):
    r = TRandom(i)
    lowedge = plot.GetXaxis().GetBinLowEdge(i)
    upedge = plot.GetXaxis().GetBinUpEdge(i)
    center = plot.GetXaxis().GetBinCenter(i)
    nombkg = nomcurve.interpolate(center)
    print 'trial number:', i
    print 'nombkg', nombkg
    nlim.setVal(nombkg)
    #nlim.setRange(nombkg*0.5, nombkg*2.0)
    nlim.removeRange()
    hmass.setRange("errRange",lowedge,upedge)
    epdf = RooExtendPdf("epdf","",cpdf,nlim,"errRange")
    #nll = epdf.createNLL(datanorm,RooFit.Extended())
    #minim = RooMinimizer(nll)
    #minim.setStrategy(0)
    #minim.setPrintLevel(-1)
    clone = 1.0 - 2.0*(RooStats.SignificanceToPValue(1.0))
    cltwo = 1.0 - 2.0*(RooStats.SignificanceToPValue(2.0))
    print 'clone', clone, 'cltwo', cltwo
    #minim.migrad()
    #minim.hesse()
    #minim.minos(RooArgSet(nlim))
    onesigma.SetPoint(i-1,center,nombkg)
    #onelo=-nlim.getErrorLo()
    #onehi=nlim.getErrorHi()
    tempi = i
    if i>82: tempi=i+(i-82)*3
    if lepton == 'vbf':
      if i<8:
        onehi = onelo=nombkg*0.042+(math.cosh((tempi-45)/45.0)-0.5)
      else:
        onehi = onelo=nombkg*0.017+(math.cosh((tempi-45)/45.0)-0.5)
      print (math.cosh((tempi-45)/45.0)-1)
    else:
      #if i<8:
      #  onehi = onelo=nombkg*0.42*(math.cosh((tempi-18)/18.0))
      #else:
      #  onehi = onelo=nombkg*0.42*(math.cosh((tempi-18)/18.0))
      #print (math.cosh((tempi-45)/45.0)-1)

      nll = epdf.createNLL(datanorm,RooFit.Extended(),RooFit.NumCPU(8))
      minim = RooMinimizer(nll)
      minim.setErrorLevel(0.5*pow(ROOT.Math.normal_quantile(1-0.5*(1-clone),1.0),2)) #0.5 is because qmu is -2*NLL
      minim.setStrategy(1)
      minim.setPrintLevel(-1)
      minim.migrad()
      minim.hesse()
      minim.minos(RooArgSet(nlim))
      onelo=-nlim.getErrorLo()
      onehi=nlim.getErrorHi()

      #if abs(onehi) <0.05 or abs(onehi) > 0.9:
      #if abs(onelo) <0.05 or abs(onelo) > 0.9:
      #  onelo = oldlo
      #oldhi = onehi
      #oldlo = onelo

    onesigma.SetPointError(i-1,0.,0.,onelo,onehi)

    if abs(onelo)<0.01:
      onesigma.SetPointError(i-1,0.,0.,onehi,onehi)
      onelo=onehi

    if abs(onehi)<0.01:
      onesigma.SetPointError(i-1,0.,0.,onelo,onelo)
      onehi=onelo

    if( abs(onelo) <0.01 and abs(onehi)<0.01):
      onesigma.SetPointError(i-1,0.,0.,nlim.getError(),nlim.getError())
      onelo=nlim.getError()
      onehi=nlim.getError()

    if((lepton=="muons")and(year=="2011")and(onehi)>6):
      onesigma.SetPointError(i-1,0.,0.,2.1,2.1)

    if((lepton=="electrons")and(year=="2012")and(onehi>11)and(i>30)):
      onesigma.SetPointError(i-1,0.,0.,5.1,5.1)

    print 'one errHi', onehi, 'one errLo', onelo

    #minim.setErrorLevel(0.5*pow(ROOT.Math.normal_quantile(1-0.5*(1-cltwo),1.0),2)) #0.5 is because qmu is -2*NLL
    # eventually if cl = 0.95 this is the usual 1.92!
    #minim.migrad()
    #minim.minos(RooArgSet(nlim))
    #minim.hesse()
    twosigma.SetPoint(i-1,center,nombkg)
    twolo = 1.92*onelo
    twohi = 1.92*onehi
    twosigma.SetPointError(i-1,0.,0.,twolo,twohi)

    print 'two errHi', twohi, 'two errLo', twolo
  onesigma.Print("V")
  twosigma.Print("V")

if __name__=="__main__":
  BGPlots()




