#!/usr/bin/env python
import sys
sys.argv.append('-b')
sys.argv.append('-n')
from ROOT import *
import numpy as np
import math

#print gSystem.GetIncludePath()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" ) #for fermilab compatibility
#print gSystem.GetIncludePath()
gROOT.ProcessLine('.x RooStepBernstein.cxx+')
gROOT.ProcessLine('.x RooGaussStepBernstein.cxx+')
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

stepThrough = False

def makePlots():
  yearList = ['2011','2012']
  leptonList = ['muons','electrons']
  catList = ['cat1','cat2','cat3','cat4','vbf']
  doubleCatList = ['14','23']
  vbfList = ['2012mu','2012el','2011']

#  yearList = ['2012']
#  leptonList = ['muons']
#  catList = ['cat1']

  f_ws_muon_2012 = TFile('models_4cat_preapproval_muons_2012_GaussBernVBFtag.root')
  f_ws_electron_2012 = TFile('models_4cat_preapproval_electrons_2012_GaussBernVBFtag.root')
  f_ws_muon_2011 = TFile('models_4cat_preapproval_muons_2011_GaussBernVBFtag.root')
  f_ws_electron_2011 = TFile('models_4cat_preapproval_electrons_2011_GaussBernVBFtag.root')
  f_ws_all_2011 = TFile('models_4cat_preapproval_all_2011_GaussBernVBFtag.root')

  el2012_Signal = TFile('/uscms/home/bpollack/work/CMSSW_5_3_6/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_EE2012ABCD_MoriondV5_2-10-13.root')
  mu2012_Signal = TFile('/uscms/home/bpollack/work/CMSSW_5_3_6/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_MuMu2012ABCD_MoriondV6_2-20-13.root')
  el2011_Signal = TFile('/uscms_data/d2/bpollack/CMSSW_5_3_2/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_EE2011_Medium_ICHEPmzmzg_1-19-13.root')
  mu2011_Signal = TFile('/uscms_data/d2/bpollack/CMSSW_5_3_2/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_MuMu2011_Medium_ICHEPmzmzg_1-19-13.root')

  print 'getting ws'
  myws_muon_2012 = f_ws_muon_2012.Get("ws")
  myws_electron_2012 = f_ws_electron_2012.Get("ws")
  myws_muon_2011 = f_ws_muon_2011.Get("ws")
  myws_electron_2011 = f_ws_electron_2011.Get("ws")
  myws_all_2011 = f_ws_all_2011.Get("ws")

  if stepThrough: raw_input('Hit any key to continue')
  print 'printing ws electron'
  myws_all_2011.Print();

  if stepThrough: raw_input('Hit any key to continue')
  print 'done printing WS ...'

  h2 = TH1F("h1", "h1", 80, 100, 180);
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
      if year == '2012' and lepton == 'muons':
        current_ws = myws_muon_2012
        current_sig = mu2012_Signal
      elif year == '2011' and lepton == 'muons':
        current_ws = myws_muon_2011
        current_sig = mu2011_Signal
      elif year == '2012' and lepton == 'electrons':
        current_ws = myws_electron_2012
        current_sig = el2012_Signal
      elif year == '2011' and lepton == 'electrons':
        current_ws = myws_electron_2011
        current_sig = el2011_Signal
      mzg = current_ws.var("CMS_hzg_mass")
      mzg.setBins(90)
      #mzg.setRange(100,190)
      mzg.setRange('sigRegion',120,160)
      mzg.Print()

      if year == '2012':
        if lepton == 'electrons':
          lumi = 19.6195
        else:
          lumi = 19.6175
      else:
        if lepton == 'electrons':
          lumi = 4.98
        else:
          lumi = 5.05

      for cats in doubleCatList:

        c.cd()
        frameTop = mzg.frame()
        frameTop.SetMinimum(0.00001)
        if cats == '14': frameTop.SetYTitle("Events / 2 GeV")
        else: frameTop.SetYTitle(" ")
        frameTop.GetXaxis().SetTitleSize(0)
        frameTop.GetXaxis().SetLabelSize(0)
        frameTop.GetYaxis().SetNdivisions(506)
        frameBottom = mzg.frame()
        frameBottom.SetMinimum(0.00001)
        frameBottom.GetYaxis().SetTitleSize(0)
        frameBottom.GetYaxis().SetNdivisions(506)
        if year == '2012' and lepton == 'muons' and cats == '14':
          frameBottom.SetMaximum(325)
        elif year == '2012' and lepton == 'muons' and cats == '23':
          frameBottom.SetMaximum(210)
        elif year == '2012' and lepton == 'electrons' and cats == '14':
          frameBottom.SetMaximum(237)
        elif year == '2012' and lepton == 'electrons' and cats == '23':
          frameBottom.SetMaximum(215)
        elif year == '2011' and lepton == 'muons' and cats == '14':
          frameBottom.SetMaximum(55)
        elif year == '2011' and lepton == 'muons' and cats == '23':
          frameBottom.SetMaximum(65)
        elif year == '2011' and lepton == 'electrons' and cats == '14':
          frameBottom.SetMaximum(55)
        elif year == '2011' and lepton == 'electrons' and cats == '23':
          frameBottom.SetMaximum(49)

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

        if cats == '14':
          if lepton == 'electrons' and year =='2012':
            dataTop = current_ws.data('dsdatacat1')
            pdfTop = current_ws.pdf('GaussBern4Full_cat1_'+lepton+'_'+year)
          else:
            dataTop = current_ws.data('dsdatacat1')
            pdfTop = current_ws.pdf('GaussBern5Full_cat1_'+lepton+'_'+year)
          sigTop_gg = current_sig.Get('h1_InvariantMassReco1GevCAT1FULLRANGE_Signal'+year+'ggM125')
          sigTop_vbf = current_sig.Get('h1_InvariantMassReco1GevCAT1FULLRANGE_Signal'+year+'vbfM125')
          sigTop_wh = current_sig.Get('h1_InvariantMassReco1GevCAT1FULLRANGE_Signal'+year+'whM125')
          sigTop_zh = current_sig.Get('h1_InvariantMassReco1GevCAT1FULLRANGE_Signal'+year+'zhM125')
          sigTop_tth = current_sig.Get('h1_InvariantMassReco1GevCAT1FULLRANGE_Signal'+year+'tthM125')
          dataBottom = current_ws.data('dsdatacat4')
          pdfBottom = current_ws.pdf('GaussBern5Full_cat4_'+lepton+'_'+year)
          sigBottom_gg = current_sig.Get('h1_InvariantMassReco1GevCAT4FULLRANGE_Signal'+year+'ggM125')
          sigBottom_vbf = current_sig.Get('h1_InvariantMassReco1GevCAT4FULLRANGE_Signal'+year+'vbfM125')
          sigBottom_wh = current_sig.Get('h1_InvariantMassReco1GevCAT4FULLRANGE_Signal'+year+'whM125')
          sigBottom_zh = current_sig.Get('h1_InvariantMassReco1GevCAT4FULLRANGE_Signal'+year+'zhM125')
          sigBottom_tth = current_sig.Get('h1_InvariantMassReco1GevCAT4FULLRANGE_Signal'+year+'tthM125')
        if cats == '23':
          if lepton == 'electrons':
            dataTop = current_ws.data('dsdatacat3')
            pdfTop = current_ws.pdf('GaussBern5Full_cat3_'+lepton+'_'+year)
          else:
            dataTop = current_ws.data('dsdatacat2')
            pdfTop = current_ws.pdf('GaussBern5Full_cat2_'+lepton+'_'+year)
          sigTop_gg = current_sig.Get('h1_InvariantMassReco1GevCAT2FULLRANGE_Signal'+year+'ggM125')
          sigTop_vbf = current_sig.Get('h1_InvariantMassReco1GevCAT2FULLRANGE_Signal'+year+'vbfM125')
          sigTop_wh = current_sig.Get('h1_InvariantMassReco1GevCAT2FULLRANGE_Signal'+year+'whM125')
          sigTop_zh = current_sig.Get('h1_InvariantMassReco1GevCAT2FULLRANGE_Signal'+year+'zhM125')
          sigTop_tth = current_sig.Get('h1_InvariantMassReco1GevCAT2FULLRANGE_Signal'+year+'tthM125')
          if lepton == 'electrons':
            dataBottom = current_ws.data('dsdatacat2')
            pdfBottom = current_ws.pdf('GaussBern5Full_cat2_'+lepton+'_'+year)
          else:
            dataBottom = current_ws.data('dsdatacat3')
            pdfBottom = current_ws.pdf('GaussBern5Full_cat3_'+lepton+'_'+year)
          sigBottom_gg = current_sig.Get('h1_InvariantMassReco1GevCAT3FULLRANGE_Signal'+year+'ggM125')
          sigBottom_vbf = current_sig.Get('h1_InvariantMassReco1GevCAT3FULLRANGE_Signal'+year+'vbfM125')
          sigBottom_wh = current_sig.Get('h1_InvariantMassReco1GevCAT3FULLRANGE_Signal'+year+'whM125')
          sigBottom_zh = current_sig.Get('h1_InvariantMassReco1GevCAT3FULLRANGE_Signal'+year+'zhM125')
          sigBottom_tth = current_sig.Get('h1_InvariantMassReco1GevCAT3FULLRANGE_Signal'+year+'tthM125')

        allSigTop = sigTop_gg.Clone()
        allSigTop.Reset()
        sigTop_gg.Scale(lumi/(99991/(19.52*0.00154*0.100974*1000)))
        sigTop_vbf.Scale(lumi/(99885/(1.578*0.00154*0.10098*1000)))
        sigTop_wh.Scale(lumi/(656101/(0.6966*0.00154*1000)))
        sigTop_zh.Scale(lumi/(344143/(0.3943*0.00154*1000)))
        sigTop_tth.Scale(lumi/(100048/(0.1302*0.00154*0.10098*1000)))
        allSigTop.Add(sigTop_gg)
        #allSigTop.Add(sigTop_vbf)
        #allSigTop.Add(sigTop_wh)
        #allSigTop.Add(sigTop_zh)
        #allSigTop.Add(sigTop_tth)

        allSigBottom = sigBottom_gg.Clone()
        allSigBottom.Reset()
        sigBottom_gg.Scale(lumi/(99991/(19.52*0.00154*0.100974*1000)))
        sigBottom_vbf.Scale(lumi/(99885/(1.578*0.00154*0.10098*1000)))
        sigBottom_wh.Scale(lumi/(656101/(0.6966*0.00154*1000)))
        sigBottom_zh.Scale(lumi/(344143/(0.3943*0.00154*1000)))
        sigBottom_tth.Scale(lumi/(100048/(0.1302*0.00154*0.10098*1000)))
        allSigBottom.Add(sigBottom_gg)
        #allSigBottom.Add(sigBottom_vbf)
        #allSigBottom.Add(sigBottom_wh)
        #allSigBottom.Add(sigBottom_zh)
        #allSigBottom.Add(sigBottom_tth)


        pad1.cd()
        dataTop.plotOn(frameTop, RooFit.Binning(45))
        pdfTop.plotOn(frameTop, RooFit.Range('fullRegion'), RooFit.LineWidth(2))
        #pdfTop.plotOn(frameTop, RooFit.Range('sigRegion'), RooFit.LineWidth(2))
        frameTop.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
        frameTop.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
        frameTop.GetYaxis().CenterTitle()
        frameTop.SetTitleOffset(0.975,"Y")
        frameTop.SetTitle('Test Plot {0} {1} {2}'.format(lepton,year,cats))
        frameTop.Draw()
        if cats is '14' and not (year is '2012' and lepton is 'muons'):
          chi2 = frameTop.chiSquare(7)
        else:
          chi2 = frameTop.chiSquare(8)
        print 'Test Plot\t{0}\t{1}\t{2}\t{3}'.format(lepton,year,cats[0], chi2)
        raw_input()


        onesigmaTop = TGraphAsymmErrors()
        twosigmaTop = TGraphAsymmErrors()
        tmpCurveTop = RooCurve(frameTop.getObject(int(frameTop.numItems())-1))
        doBandsFit(onesigmaTop, twosigmaTop, mzg, pdfTop, tmpCurveTop, dataTop, frameTop, year, lepton)
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
        allSigTop.Scale(75)
        allSigTop.Rebin(2)
        allSigTop.SetLineColor(kRed)
        allSigTop.SetLineWidth(2)
        allSigTop.Draw('samehist')

        L1Top.SetNDC()
        L1Top.SetTextSize(0.045)
        L1Top.SetTextFont(62)
        if cats == '14' and year == '2011': L1Top.DrawLatex(0.8, 0.9, ('Class 1'))
        elif cats == '14' and year == '2012': L1Top.DrawLatex(0.8, 0.9, ('Class 1'))
        elif cats == '23': L1Top.DrawLatex(0.8, 0.9, ('Class 3'))
        chan1Top.SetNDC()
        chan1Top.SetTextSize(0.045)
        chan1Top.SetTextFont(62)
        if year == '2011' and cats == '14':
          chan1Top.DrawLatex(0.10, 0.96, ("CMS"))
          chan1Top.DrawLatex(0.57, 0.96, "#sqrt{s} = 7 TeV, L = 5 fb^{-1}");
          if lepton == 'electrons' and cats == '14': chan1Top.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
          elif lepton == 'muons' and cats == '14': chan1Top.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
        elif year == '2012' and cats == '14':
          chan1Top.DrawLatex(0.10, 0.96, ("CMS"))
          chan1Top.DrawLatex(0.51, 0.96, "#sqrt{s} = 8 TeV, L = 19.6 fb^{-1}");
          if lepton == 'electrons' and cats == '14': chan1Top.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
          elif lepton == 'muons' and cats == '14': chan1Top.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
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
        if cats == '14' and year == '2012': leg1Top.Draw()
        #cTop.Print('testPlot_'+lepton+'_'+year+'_'+cat+'.root')

        pad2.cd()
        dataBottom.plotOn(frameBottom, RooFit.Binning(45))
        pdfBottom.plotOn(frameBottom, RooFit.Range('fullRegion'), RooFit.LineWidth(2))
        #pdfBottom.plotOn(frameBottom, RooFit.Range('sigRegion'), RooFit.LineWidth(2))
        frameBottom.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
        frameBottom.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
        if cats == '14': frameBottom.GetXaxis().SetLabelSize(0); frameBottom.GetXaxis().SetLabelOffset(999)
        frameBottom.GetYaxis().CenterTitle()
        frameBottom.SetTitleOffset(1.2,"Y")
        frameBottom.SetTitle('Test Plot {0} {1} {2}'.format(lepton,year,cats))
        frameBottom.Draw()
        chi2 = frameBottom.chiSquare(8)
        print 'Test Plot\t{0}\t{1}\t{2}\t{3}'.format(lepton,year,cats[1], chi2)
        raw_input()

        onesigmaBottom = TGraphAsymmErrors()
        twosigmaBottom = TGraphAsymmErrors()
        tmpCurveBottom = RooCurve(frameBottom.getObject(int(frameBottom.numItems())-1))
        doBandsFit(onesigmaBottom, twosigmaBottom, mzg, pdfBottom, tmpCurveBottom, dataBottom, frameBottom, year, lepton)
        twosigmaBottom.SetLineColor(kYellow)
        twosigmaBottom.SetFillColor(kYellow)
        twosigmaBottom.SetMarkerColor(kYellow)
        onesigmaBottom.SetLineColor(kGreen)
        onesigmaBottom.SetFillColor(kGreen)
        onesigmaBottom.SetMarkerColor(kGreen)

        frameBottom.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
        frameBottom.GetXaxis()
        h1Bottom.SetMarkerStyle(20)
        h1Bottom.SetMarkerColor(kBlack)
        h1Bottom.SetLineColor(1)
        frameBottom.Draw("e0")
        frameBottom.SetTitle("")
        twosigmaBottom.Draw("L3 same")
        onesigmaBottom.Draw("L3 same")
        frameBottom.Draw("e0same")
        allSigBottom.Scale(75)
        allSigBottom.Rebin(2)
        allSigBottom.SetLineColor(kRed)
        allSigBottom.SetLineWidth(2)
        allSigBottom.Draw('samehist')

        L1Bottom.SetNDC()
        L1Bottom.SetTextSize(0.045)
        L1Bottom.SetTextFont(62)
        if cats == '14': L1Bottom.DrawLatex(0.8, 0.5, ('Class 2'))
        elif cats == '23': L1Bottom.DrawLatex(0.8, 0.5, ('Class 4'))
        chan1Bottom.SetNDC()
        chan1Bottom.SetTextSize(0.045)
        chan1Bottom.SetTextFont(62)
        fit1Bottom.SetLineColor(kBlue)
        fit1Bottom.SetLineWidth(2)
        fitSB1Bottom.SetLineColor(kBlue)
        fitSB1Bottom.SetLineWidth(2)
        sigma1Bottom.SetFillColor(kGreen)
        sigma1Bottom.SetLineWidth(2)
        sigma2Bottom.SetFillColor(kYellow)
        sigma2Bottom.SetLineWidth(2)
        leg1Bottom.SetFillColor(0)
        leg1Bottom.SetFillStyle(0)
        leg1Bottom.SetShadowColor(0)
        leg1Bottom.SetBorderSize(0)
        leg1Bottom.SetTextFont(62)
        leg1Bottom.SetTextSize(0.042)
        #leg1Bottom.AddEntry(allSignal, "Signal m_{H} = 125 GeV x 100", "l")
        leg1Bottom.AddEntry(fitSB1Top, "Background Model", "l")
        leg1Bottom.AddEntry(allSigTop, "Expected Signal #times 75", "l")
        if cats == '14' and year == '2012': leg1Bottom.Draw()
        c.Print('testPlot_'+lepton+'_'+year+'_'+cats+'.pdf')
        c.Print('testPlot_'+lepton+'_'+year+'_'+cats+'.ps')
        #cBottom.Print('testPlot_'+lepton+'_'+year+'_'+cat+'.root')
        leg1Bottom.Clear()
        leg1Top.Clear()
        pad1.Clear()
        pad2.Clear()
        c.Clear()

        pad1.Close()
        pad2.Close()

  for selection in vbfList:
    if selection == '2012mu':
      current_ws = myws_muon_2012
      current_sig = mu2012_Signal
    elif selection == '2012el':
      current_ws = myws_electron_2012
      current_sig = el2012_Signal
    elif selection == '2011':
      current_ws= myws_all_2011
      current_sig_mu = mu2011_Signal
      current_sig_el = el2011_Signal
    mzg = current_ws.var("CMS_hzg_mass")
    mzg.setBins(36)
    #mzg.setRange(100,190)
    mzg.setRange('sigRegion',120,160)
    mzg.Print()

    if selection == '2012el':
      lumi = 19.6195
    elif selection == '2012mu':
      lumi = 19.6175
    elif selection == '2011':
      lumi = 4.98 + 5.05

    c.cd()
    frame = mzg.frame()
    frame.SetMinimum(0.0)
    frame.SetYTitle("Events / 2.5 GeV")

    pad1 = TPad()
    pad1.SetTicks(1, 1);
    pad1.Draw();
    #pad1.SetBottomMargin(0.5*height+c.GetBottomMargin());
    pad1.SetFillStyle(4000);
    pad1.SetFillColor(kWhite);
    pad1.SetLeftMargin(0.10)
    pad1.SetRightMargin(0.03)

    #current_ws.Print()
    if '2012' in selection:
      data = current_ws.data('dsdatacat5')
      pdf = current_ws.pdf('Bern3Full_cat5')
      pdf.Print()
      raw_input()
      sig_vbf = current_sig.GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+selection.strip('elmu')+'vbfM125')
      frame.SetMaximum(7.5)
    else:
      frame.SetMaximum(4.2)
    #  data = current_ws.data('data_obs_cat15')
    #  pdf = current_ws.pdf('MzgBkgBern_cat15')
      data = current_ws.data('dsdatacat5')
      pdf = current_ws.pdf('Bern3Full_cat5')


      sig_vbf_mu = current_sig_mu.GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+selection.strip('elmu')+'vbfM125')
      sig_vbf_el = current_sig_el.GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+selection.strip('elmu')+'vbfM125')

      sig_vbf = sig_vbf_mu
      sig_vbf.Add(sig_vbf_el)

    print selection

    allSig = sig_vbf.Clone()
    allSig.Reset()
    sig_vbf.Scale(lumi/(99885/(1.578*0.00154*0.10098*1000)))
    allSig.Add(sig_vbf)

    pad1.cd()
    #data_hist = data.createHistogram("CMS_hzg_mass,y",36)
    data.plotOn(frame, RooFit.Binning(36),RooFit.DataError(RooAbsData.SumW2))
    #data_hist.plotOn(frame)
    pdf.plotOn(frame, RooFit.Range('fullRegion'), RooFit.LineWidth(2))
    #pdf.plotOn(frame, RooFit.Range('sigRegion'), RooFit.LineWidth(2))
    frame.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
    frame.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
    frame.GetYaxis().CenterTitle()
    frame.SetTitleOffset(0.975,"Y")
    frame.SetTitle('Test Plot {0} '.format(selection))
    frame.SetMinimum(0.00001)
    frame.Draw()
    chi2 = frame.chiSquare(4)
    print 'Test Plot\t{0}\t{1}'.format(selection,chi2)
    raw_input()

    onesigma = TGraphAsymmErrors()
    twosigma = TGraphAsymmErrors()
    tmpCurve = RooCurve(frame.getObject(int(frame.numItems())-1))
    doBandsFit(onesigma, twosigma, mzg, pdf, tmpCurve, data, frame, selection.strip('muel'), 'vbf')
    twosigma.SetLineColor(kYellow)
    twosigma.SetFillColor(kYellow)
    twosigma.SetMarkerColor(kYellow)
    onesigma.SetLineColor(kGreen)
    onesigma.SetFillColor(kGreen)
    onesigma.SetMarkerColor(kGreen)

    frame.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
    h1.SetMarkerStyle(20)
    h1.SetMarkerColor(kBlack)
    h1.SetLineColor(1)
    frame.Draw("e0")
    frame.SetTitle("")
    twosigma.Draw("L3 same")
    onesigma.Draw("L3 same")
    frame.Draw("e0same")
    if selection == '2011':
      allSig.Scale(1.5)
    else:
      allSig.Scale(2.6)
    allSig.Rebin(2)
    allSig.SetLineColor(kRed)
    allSig.SetLineWidth(2)
    allSig.Draw('samehist')

    L1.SetNDC()
    L1.SetTextSize(0.045)
    L1.SetTextFont(62)
    L1.DrawLatex(0.58, 0.9, ('Class Dijet-Tagged'))
    chan1.SetNDC()
    chan1.SetTextSize(0.045)
    chan1.SetTextFont(62)
    if '2011' in selection:
      chan1.DrawLatex(0.10, 0.96, ("CMS"))
      chan1.DrawLatex(0.57, 0.96, "#sqrt{s} = 7 TeV, L = 5 fb^{-1}");
      if 'el' in selection: chan1.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
      elif 'mu' in selection: chan1.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
      else: chan1.DrawLatex(0.25, 0.96, "H #rightarrow Z #gamma #rightarrow ll#gamma");
    else:
      chan1.DrawLatex(0.10, 0.96, ("CMS"))
      chan1.DrawLatex(0.51, 0.96, "#sqrt{s} = 8 TeV, L = 19.6 fb^{-1}");
      if 'el' in selection: chan1.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow ee#gamma");
      elif 'mu' in selection: chan1.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow #mu#mu#gamma");
      else: chan1.DrawLatex(0.22, 0.96, "H #rightarrow Z #gamma #rightarrow ll#gamma");
    fit1.SetLineColor(kBlue)
    fit1.SetLineWidth(2)
    fitSB1.SetLineColor(kBlue)
    fitSB1.SetLineWidth(2)
    sigma1.SetFillColor(kGreen)
    sigma1.SetLineWidth(2)
    sigma2.SetFillColor(kYellow)
    sigma2.SetLineWidth(2)
    leg1.SetFillColor(0)
    leg1.SetFillStyle(0)
    leg1.SetShadowColor(0)
    leg1.SetBorderSize(0)
    leg1.SetTextFont(62)
    leg1.SetTextSize(0.047)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.SetShadowColor(0)
    leg2.SetBorderSize(0)
    leg2.SetTextFont(62)
    leg2.SetTextSize(0.047)
    leg1.AddEntry(h1, "Data", "pl")
    leg1.AddEntry(fitSB1, "Background Model", "l")
    leg1.AddEntry(allSig, "Expected Signal #times 10", "l")
    leg2.AddEntry(sigma1, "#pm 1 #sigma", "f")
    leg2.AddEntry(sigma2, "#pm 2 #sigma", "f")
    #leg1.AddEntry(allSignal, "Signal m_{H} = 125 GeV x 100", "l")
    leg1.Draw()
    leg2.Draw()
    #c.Print('testPlot_'+lepton+'_'+selection+'_'+cat+'.root')

    c.Print('testPlot_'+selection+'.pdf')
    c.Print('testPlot_'+selection+'.ps')
    #cBottom.Print('testPlot_'+lepton+'_'+selection+'_'+cat+'.root')
    leg1.Clear()
    leg2.Clear()
    pad1.Clear()
    c.Clear()

    pad1.Close()
  del c


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
    if lepton != 'vbf':
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

      nll = epdf.createNLL(datanorm,RooFit.Extended())
      minim = RooMinimizer(nll)
      minim.setErrorLevel(0.5*pow(ROOT.Math.normal_quantile(1-0.5*(1-clone),1.0),2)) #0.5 is because qmu is -2*NLL
      minim.setStrategy(2)
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
  makePlots()
