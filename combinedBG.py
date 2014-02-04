#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.x RooStepBernstein.cxx+')
gROOT.ProcessLine('.x RooGaussStepBernstein.cxx+')
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()
#setTDRStyle()

verbose = False
makeNewResults =False

def doCombinedBG():
  print 'opening file'
  f_ws_muon_2012 = TFile('models_4cat_preapproval_muons_2012_GaussBernVBFtag.root')
  f_ws_electron_2012 = TFile('models_4cat_preapproval_electrons_2012_GaussBernVBFtag.root')
  f_ws_muon_2011 = TFile('models_4cat_preapproval_muons_2011_GaussBernVBFtag.root')
  f_ws_electron_2011 = TFile('models_4cat_preapproval_electrons_2011_GaussBernVBFtag.root')
  el2012_Moriond = TFile('/uscms/home/bpollack/work/CMSSW_5_3_6/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_EE2012ABCD_MoriondV5_2-10-13.root')
  mu2012_Moriond = TFile('/uscms/home/bpollack/work/CMSSW_5_3_6/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_MuMu2012ABCD_MoriondV6_2-20-13.root')
  el2011 = TFile('/uscms_data/d2/bpollack/CMSSW_5_3_2/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_EE2011_Medium_ICHEPmzmzg_1-19-13.root')
  mu2011 = TFile('/uscms_data/d2/bpollack/CMSSW_5_3_2/src/PollackPrograms/HiggsZGAnalyzer/batchHistos/higgsHistograms_MuMu2011_Medium_ICHEPmzmzg_1-19-13.root')
  #el2012_Moriond = TFile('higgsHistograms_EE2012ABCD_MoriondV5_2-10-13.root')
  #mu2012_Moriond = TFile('higgsHistograms_MuMu2012ABCD_MoriondV6_2-20-13.root')
  #el2011 = TFile('higgsHistograms_EE2011_Medium_ICHEPmzmzg_1-19-13.root')
  #mu2011 = TFile('higgsHistograms_MuMu2011_Medium_ICHEPmzmzg_1-19-13.root')
  print 'getting ws'
  myws_muon_2012 = f_ws_muon_2012.Get("ws")
  myws_electron_2012 = f_ws_electron_2012.Get("ws")
  myws_muon_2011 = f_ws_muon_2011.Get("ws")
  myws_electron_2011 = f_ws_electron_2011.Get("ws")

  if not makeNewResults:
    f_ws_fitres = TFile('fullpolyws.root')
    myws_poly = f_ws_fitres.Get('ws')
    print 'printing ws poly'
    myws_poly.Print();
    fitres = RooFitResult(myws_poly.genobj('totalpolyfitres'))
    fitres.Print()

#  raw_input('Hit any key to continue')
  print 'printing ws electron'
  myws_electron_2011.Print();
  raw_input('Hit any key to continue')
  print 'done printing WS ...'
  mzg_muon_2012 = myws_muon_2012.var("CMS_hzg_mass")
  mzg_muon_2012.setBins(90)
  mzg_muon_2012.Print()
  mzg_electron_2012 = myws_electron_2012.var("CMS_hzg_mass")
  mzg_electron_2012.setBins(90)
  mzg_electron_2012.Print()
  mzg_muon_2011 = myws_muon_2011.var("CMS_hzg_mass")
  mzg_muon_2011.setBins(90)
  mzg_muon_2011.Print()
  mzg_electron_2011 = myws_electron_2011.var("CMS_hzg_mass")
  mzg_electron_2011.setBins(90)
  mzg_electron_2011.Print()

  bgPdfList = []
  bgNormList = []
  fracPdfList = []
  frac_2011weightPdfList = []
  frac_2012weightPdfList = []
  frac_ALLweightPdfList = []

  mzgList = [mzg_electron_2012,mzg_muon_2012,mzg_electron_2011,mzg_muon_2011]

  dict2012_Moriond = {'mu':mu2012_Moriond,'el':el2012_Moriond}
  dict2011 = {'mu':mu2011,'el':el2011}
  yearDict = {2011:dict2011,2012:dict2012_Moriond}
  leptons = ['mu','el']
  allSignal = gg125 = yearDict[2011]['mu'].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(2011)+'ggM125').Clone()
  allSignal.Reset()
  allSignal.Print()
  #raw_input('Hit any key to continue')
  for year in yearDict.keys():
    for lep in leptons:
      gg125 = yearDict[year][lep].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(year)+'ggM125')
      vbf125 = yearDict[year][lep].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(year)+'vbfM125')
      wh125 = yearDict[year][lep].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(year)+'whM125')
      zh125 = yearDict[year][lep].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(year)+'zhM125')
      tth125 = yearDict[year][lep].GetDirectory('ZGamma').Get('h1_InvariantMass_Signal'+str(year)+'tthM125')

   #   raw_input('Hit any key to continue')
      if year == 2012:
        if lep == 'el':
          lumi = 19.6195
        else:
          lumi = 19.6175
      else:
        if lep == 'el':
          lumi = 4.98
        else:
          lumi = 5.05

      gg125.Scale(lumi/(99991/(19.52*0.00154*0.100974*1000)))
      vbf125.Scale(lumi/(99885/(1.578*0.00154*0.10098*1000)))
      wh125.Scale(lumi/(656101/(0.6966*0.00154*1000)))
      zh125.Scale(lumi/(344143/(0.3943*0.00154*1000)))
      tth125.Scale(lumi/(100048/(0.1302*0.00154*0.10098*1000)))
      allSignal.Add(gg125)
      allSignal.Add(vbf125)
      allSignal.Add(wh125)
      allSignal.Add(zh125)
      allSignal.Add(tth125)

#2012 muon signif [('CAT1', 0.004359196206029166), ('CAT2', 0.0021423433075113151), ('CAT3', 0.0014066633650406933), ('CAT4', 0.0023852237058661018)]
#2012 elec signif [('CAT1', 0.0043679269110740541), ('CAT2', 0.0021969060774770007), ('CAT3', 0.0014579738792316868), ('CAT4', 0.0024094804711304076)]
#2011 muon signif [('CAT1', 0.0041321823033112874), ('CAT2', 0.0019841545908581555), ('CAT3', 0.0016123331942843135), ('CAT4', 0.0025599442942319068)]
#2011 elec signif [('CAT1', 0.0041475745496618215), ('CAT2', 0.0027760146820201364), ('CAT3', 0.0020663796471802939), ('CAT4', 0.0024861342001010864)]

#make the signifcance weight dictionaries

  totalSignif2012 = 0.004359196206029166+0.0021423433075113151+0.0014066633650406933+0.0023852237058661018+0.0043679269110740541+0.0021969060774770007+0.0014579738792316868+0.0024094804711304076
  totalSignif2011 = 0.0041321823033112874+0.0019841545908581555+0.0016123331942843135+0.0025599442942319068+0.0041475745496618215+0.0027760146820201364+0.0020663796471802939+0.0024861342001010864
  totalSignifAll = totalSignif2012 + totalSignif2011
  signifFrac2012Dict = {'mucat1_2012':0.004359196206029166/totalSignif2012,'mucat2_2012':0.0021423433075113151/totalSignif2012,'mucat3_2012':0.0014066633650406933/totalSignif2012,'mucat4_2012':0.0023852237058661018/totalSignif2012,
      'elcat1_2012':0.0043679269110740541/totalSignif2012,'elcat2_2012':0.0021969060774770007/totalSignif2012,'elcat3_2012':0.0014579738792316868/totalSignif2012,'elcat4_2012':0.0024094804711304076/totalSignif2012}

  signifFrac2011Dict = {'mucat1_2011':0.0041321823033112874/totalSignif2011,'mucat2_2011':0.0019841545908581555/totalSignif2011,'mucat3_2011':0.0016123331942843135/totalSignif2011,'mucat4_2011':0.0025599442942319068/totalSignif2011,
      'elcat1_2011':0.0041475745496618215/totalSignif2011,'elcat2_2011':0.0027760146820201364/totalSignif2011,'elcat3_2011':0.0020663796471802939/totalSignif2011,'elcat4_2011':0.0024861342001010864/totalSignif2011}

  signifFracAllDict = {'mucat1_2012':0.004359196206029166/totalSignifAll,'mucat2_2012':0.0021423433075113151/totalSignifAll,'mucat3_2012':0.0014066633650406933/totalSignifAll,'mucat4_2012':0.0023852237058661018/totalSignifAll,
      'elcat1_2012':0.0043679269110740541/totalSignifAll,'elcat2_2012':0.0021969060774770007/totalSignifAll,'elcat3_2012':0.0014579738792316868/totalSignifAll,'elcat4_2012':0.0024094804711304076/totalSignifAll,
      'mucat1_2011':0.0041321823033112874/totalSignifAll,'mucat2_2011':0.0019841545908581555/totalSignifAll,'mucat3_2011':0.0016123331942843135/totalSignifAll,'mucat4_2011':0.0025599442942319068/totalSignifAll,
      'elcat1_2011':0.0041475745496618215/totalSignifAll,'elcat2_2011':0.0027760146820201364/totalSignifAll,'elcat3_2011':0.0020663796471802939/totalSignifAll,'elcat4_2011':0.0024861342001010864/totalSignifAll}


  #grab the stored fits
  ee_2012_bg_cat1 = myws_electron_2012.pdf('GaussBern4Full_cat1_electrons_2012'); bgPdfList.append(ee_2012_bg_cat1);
  ee_2012_bg_cat2 = myws_electron_2012.pdf('GaussBern5Full_cat2_electrons_2012'); bgPdfList.append(ee_2012_bg_cat2);
  ee_2012_bg_cat3 = myws_electron_2012.pdf('GaussBern5Full_cat3_electrons_2012'); bgPdfList.append(ee_2012_bg_cat3);
  ee_2012_bg_cat4 = myws_electron_2012.pdf('GaussBern5Full_cat4_electrons_2012'); bgPdfList.append(ee_2012_bg_cat4);
  mumu_2012_bg_cat1 = myws_muon_2012.pdf('GaussBern5Full_cat1_muons_2012'); bgPdfList.append(mumu_2012_bg_cat1);
  mumu_2012_bg_cat2 = myws_muon_2012.pdf('GaussBern5Full_cat2_muons_2012'); bgPdfList.append(mumu_2012_bg_cat2);
  mumu_2012_bg_cat3 = myws_muon_2012.pdf('GaussBern5Full_cat3_muons_2012'); bgPdfList.append(mumu_2012_bg_cat3);
  mumu_2012_bg_cat4 = myws_muon_2012.pdf('GaussBern5Full_cat4_muons_2012'); bgPdfList.append(mumu_2012_bg_cat4);

  ee_2011_bg_cat1 = myws_electron_2011.pdf('GaussBern4Full_cat1_electrons_2011'); bgPdfList.append(ee_2011_bg_cat1);
  ee_2011_bg_cat2 = myws_electron_2011.pdf('GaussBern5Full_cat2_electrons_2011'); bgPdfList.append(ee_2011_bg_cat2);
  ee_2011_bg_cat3 = myws_electron_2011.pdf('GaussBern5Full_cat3_electrons_2011'); bgPdfList.append(ee_2011_bg_cat3);
  ee_2011_bg_cat4 = myws_electron_2011.pdf('GaussBern5Full_cat4_electrons_2011'); bgPdfList.append(ee_2011_bg_cat4);
  mumu_2011_bg_cat1 = myws_muon_2011.pdf('GaussBern5Full_cat1_muons_2011'); bgPdfList.append(mumu_2011_bg_cat1);
  mumu_2011_bg_cat2 = myws_muon_2011.pdf('GaussBern5Full_cat2_muons_2011'); bgPdfList.append(mumu_2011_bg_cat2);
  mumu_2011_bg_cat3 = myws_muon_2011.pdf('GaussBern5Full_cat3_muons_2011'); bgPdfList.append(mumu_2011_bg_cat3);
  mumu_2011_bg_cat4 = myws_muon_2011.pdf('GaussBern5Full_cat4_muons_2011'); bgPdfList.append(mumu_2011_bg_cat4);

  ee_2012_norm_cat1 = myws_electron_2012.var('nGaussBern4_cat1_electrons_2012'); bgNormList.append(ee_2012_norm_cat1);
  ee_2012_norm_cat2 = myws_electron_2012.var('nGaussBern5_cat2_electrons_2012'); bgNormList.append(ee_2012_norm_cat2);
  ee_2012_norm_cat3 = myws_electron_2012.var('nGaussBern5_cat3_electrons_2012'); bgNormList.append(ee_2012_norm_cat3);
  ee_2012_norm_cat4 = myws_electron_2012.var('nGaussBern5_cat4_electrons_2012'); bgNormList.append(ee_2012_norm_cat4);
  mumu_2012_norm_cat1 = myws_muon_2012.var('nGaussBern5_cat1_muons_2012'); bgNormList.append(mumu_2012_norm_cat1);
  mumu_2012_norm_cat2 = myws_muon_2012.var('nGaussBern5_cat2_muons_2012'); bgNormList.append(mumu_2012_norm_cat2);
  mumu_2012_norm_cat3 = myws_muon_2012.var('nGaussBern5_cat3_muons_2012'); bgNormList.append(mumu_2012_norm_cat3);
  mumu_2012_norm_cat4 = myws_muon_2012.var('nGaussBern5_cat4_muons_2012'); bgNormList.append(mumu_2012_norm_cat4);

  ee_2011_norm_cat1 = myws_electron_2011.var('nGaussBern4_cat1_electrons_2011'); bgNormList.append(ee_2011_norm_cat1);
  ee_2011_norm_cat2 = myws_electron_2011.var('nGaussBern5_cat2_electrons_2011'); bgNormList.append(ee_2011_norm_cat2);
  ee_2011_norm_cat3 = myws_electron_2011.var('nGaussBern5_cat3_electrons_2011'); bgNormList.append(ee_2011_norm_cat3);
  ee_2011_norm_cat4 = myws_electron_2011.var('nGaussBern5_cat4_electrons_2011'); bgNormList.append(ee_2011_norm_cat4);
  mumu_2011_norm_cat1 = myws_muon_2011.var('nGaussBern4_cat1_muons_2011'); bgNormList.append(mumu_2011_norm_cat1);
  mumu_2011_norm_cat2 = myws_muon_2011.var('nGaussBern5_cat2_muons_2011'); bgNormList.append(mumu_2011_norm_cat2);
  mumu_2011_norm_cat3 = myws_muon_2011.var('nGaussBern5_cat3_muons_2011'); bgNormList.append(mumu_2011_norm_cat3);
  mumu_2011_norm_cat4 = myws_muon_2011.var('nGaussBern5_cat4_muons_2011'); bgNormList.append(mumu_2011_norm_cat4);


#set the weighting fractions to 1 for the unweighted pdfs
  ee_2012_bg_cat1_frac = RooRealVar("frac1","frac1",1); fracPdfList.append(ee_2012_bg_cat1_frac)
  ee_2012_bg_cat2_frac = RooRealVar("frac2","frac2",1); fracPdfList.append(ee_2012_bg_cat2_frac)
  ee_2012_bg_cat3_frac = RooRealVar("frac3","frac3",1); fracPdfList.append(ee_2012_bg_cat3_frac)
  ee_2012_bg_cat4_frac = RooRealVar("frac4","frac4",1); fracPdfList.append(ee_2012_bg_cat4_frac)
  mumu_2012_bg_cat1_frac = RooRealVar("frac5","frac5",1); fracPdfList.append(mumu_2012_bg_cat1_frac)
  mumu_2012_bg_cat2_frac = RooRealVar("frac6","frac6",1); fracPdfList.append(mumu_2012_bg_cat2_frac)
  mumu_2012_bg_cat3_frac = RooRealVar("frac7","frac7",1); fracPdfList.append(mumu_2012_bg_cat3_frac)
  mumu_2012_bg_cat4_frac = RooRealVar("frac8","frac8",1); fracPdfList.append(mumu_2012_bg_cat4_frac)

  ee_2011_bg_cat1_frac = RooRealVar("frac9","frac9",1); fracPdfList.append(ee_2011_bg_cat1_frac)
  ee_2011_bg_cat2_frac = RooRealVar("frac10","frac10",1); fracPdfList.append(ee_2011_bg_cat2_frac)
  ee_2011_bg_cat3_frac = RooRealVar("frac11","frac11",1); fracPdfList.append(ee_2011_bg_cat3_frac)
  ee_2011_bg_cat4_frac = RooRealVar("frac12","frac12",1); fracPdfList.append(ee_2011_bg_cat4_frac)
  mumu_2011_bg_cat1_frac = RooRealVar("frac13","frac13",1); fracPdfList.append(mumu_2011_bg_cat1_frac)
  mumu_2011_bg_cat2_frac = RooRealVar("frac14","frac14",1); fracPdfList.append(mumu_2011_bg_cat2_frac)
  mumu_2011_bg_cat3_frac = RooRealVar("frac15","frac15",1); fracPdfList.append(mumu_2011_bg_cat3_frac)
  mumu_2011_bg_cat4_frac = RooRealVar("frac16","frac16",1); fracPdfList.append(mumu_2011_bg_cat4_frac)


#set the weighting fractions for the weighted pdfs
  ee_2012_bg_cat1_frac_2012weight = RooRealVar("frac_2012weight1","frac_2012weight1",signifFrac2012Dict['elcat1_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat1_frac_2012weight)
  ee_2012_bg_cat2_frac_2012weight = RooRealVar("frac_2012weight2","frac_2012weight2",signifFrac2012Dict['elcat2_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat2_frac_2012weight)
  ee_2012_bg_cat3_frac_2012weight = RooRealVar("frac_2012weight3","frac_2012weight3",signifFrac2012Dict['elcat3_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat3_frac_2012weight)
  ee_2012_bg_cat4_frac_2012weight = RooRealVar("frac_2012weight4","frac_2012weight4",signifFrac2012Dict['elcat4_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat4_frac_2012weight)
  mumu_2012_bg_cat1_frac_2012weight = RooRealVar("frac_2012weight5","frac_2012weight5",signifFrac2012Dict['mucat1_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat1_frac_2012weight)
  mumu_2012_bg_cat2_frac_2012weight = RooRealVar("frac_2012weight6","frac_2012weight6",signifFrac2012Dict['mucat2_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat2_frac_2012weight)
  mumu_2012_bg_cat3_frac_2012weight = RooRealVar("frac_2012weight7","frac_2012weight7",signifFrac2012Dict['mucat3_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat3_frac_2012weight)
  mumu_2012_bg_cat4_frac_2012weight = RooRealVar("frac_2012weight8","frac_2012weight8",signifFrac2012Dict['mucat4_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat4_frac_2012weight)

  ee_2011_bg_cat1_frac_2011weight = RooRealVar("frac_2011weight9","frac_2011weight9",signifFrac2011Dict['elcat1_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat1_frac_2011weight)
  ee_2011_bg_cat2_frac_2011weight = RooRealVar("frac_2011weight10","frac_2011weight10",signifFrac2011Dict['elcat2_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat2_frac_2011weight)
  ee_2011_bg_cat3_frac_2011weight = RooRealVar("frac_2011weight11","frac_2011weight11",signifFrac2011Dict['elcat3_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat3_frac_2011weight)
  ee_2011_bg_cat4_frac_2011weight = RooRealVar("frac_2011weight12","frac_2011weight12",signifFrac2011Dict['elcat4_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat4_frac_2011weight)
  mumu_2011_bg_cat1_frac_2011weight = RooRealVar("frac_2011weight13","frac_2011weight13",signifFrac2011Dict['mucat1_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat1_frac_2011weight)
  mumu_2011_bg_cat2_frac_2011weight = RooRealVar("frac_2011weight14","frac_2011weight14",signifFrac2011Dict['mucat2_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat2_frac_2011weight)
  mumu_2011_bg_cat3_frac_2011weight = RooRealVar("frac_2011weight15","frac_2011weight15",signifFrac2011Dict['mucat3_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat3_frac_2011weight)
  mumu_2011_bg_cat4_frac_2011weight = RooRealVar("frac_2011weight16","frac_2011weight16",signifFrac2011Dict['mucat4_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat4_frac_2011weight)

  ee_2012_bg_cat1_frac_ALLweight = RooRealVar("frac_ALLweight1"    , "frac_ALLweight1"  , signifFracAllDict['elcat1_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat1_frac_ALLweight)
  ee_2012_bg_cat2_frac_ALLweight = RooRealVar("frac_ALLweight2"    , "frac_ALLweight2"  , signifFracAllDict['elcat2_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat2_frac_ALLweight)
  ee_2012_bg_cat3_frac_ALLweight = RooRealVar("frac_ALLweight3"    , "frac_ALLweight3"  , signifFracAllDict['elcat3_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat3_frac_ALLweight)
  ee_2012_bg_cat4_frac_ALLweight = RooRealVar("frac_ALLweight4"    , "frac_ALLweight4"  , signifFracAllDict['elcat4_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat4_frac_ALLweight)
  mumu_2012_bg_cat1_frac_ALLweight = RooRealVar("frac_ALLweight5"  , "frac_ALLweight5"  , signifFracAllDict['mucat1_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat1_frac_ALLweight)
  mumu_2012_bg_cat2_frac_ALLweight = RooRealVar("frac_ALLweight6"  , "frac_ALLweight6"  , signifFracAllDict['mucat2_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat2_frac_ALLweight)
  mumu_2012_bg_cat3_frac_ALLweight = RooRealVar("frac_ALLweight7"  , "frac_ALLweight7"  , signifFracAllDict['mucat3_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat3_frac_ALLweight)
  mumu_2012_bg_cat4_frac_ALLweight = RooRealVar("frac_ALLweight8"  , "frac_ALLweight8"  , signifFracAllDict['mucat4_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat4_frac_ALLweight)
  ee_2011_bg_cat1_frac_ALLweight = RooRealVar("frac_ALLweight9"    , "frac_ALLweight9"  , signifFracAllDict['elcat1_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat1_frac_ALLweight)
  ee_2011_bg_cat2_frac_ALLweight = RooRealVar("frac_ALLweight10"   , "frac_ALLweight10" , signifFracAllDict['elcat2_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat2_frac_ALLweight)
  ee_2011_bg_cat3_frac_ALLweight = RooRealVar("frac_ALLweight11"   , "frac_ALLweight11" , signifFracAllDict['elcat3_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat3_frac_ALLweight)
  ee_2011_bg_cat4_frac_ALLweight = RooRealVar("frac_ALLweight12"   , "frac_ALLweight12" , signifFracAllDict['elcat4_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat4_frac_ALLweight)
  mumu_2011_bg_cat1_frac_ALLweight = RooRealVar("frac_ALLweight13" , "frac_ALLweight13" , signifFracAllDict['mucat1_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat1_frac_ALLweight)
  mumu_2011_bg_cat2_frac_ALLweight = RooRealVar("frac_ALLweight14" , "frac_ALLweight14" , signifFracAllDict['mucat2_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat2_frac_ALLweight)
  mumu_2011_bg_cat3_frac_ALLweight = RooRealVar("frac_ALLweight15" , "frac_ALLweight15" , signifFracAllDict['mucat3_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat3_frac_ALLweight)
  mumu_2011_bg_cat4_frac_ALLweight = RooRealVar("frac_ALLweight16" , "frac_ALLweight16" , signifFracAllDict['mucat4_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat4_frac_ALLweight)

# add up the pdfs for all cats and years and flavors
  totalBGpdf_2012 = RooAddPdf("totalBGpdf_2012","total BG pdf 2012",RooArgList(ee_2012_bg_cat1,ee_2012_bg_cat2,ee_2012_bg_cat3,ee_2012_bg_cat4,mumu_2012_bg_cat1,mumu_2012_bg_cat2,mumu_2012_bg_cat3,mumu_2012_bg_cat4),RooArgList(ee_2012_bg_cat1_frac,ee_2012_bg_cat2_frac,ee_2012_bg_cat3_frac,ee_2012_bg_cat4_frac,mumu_2012_bg_cat1_frac,mumu_2012_bg_cat2_frac,mumu_2012_bg_cat3_frac,mumu_2012_bg_cat4_frac))

  totalBGpdf_2011 = RooAddPdf("totalBGpdf_2011","total BG pdf 2011",RooArgList(ee_2011_bg_cat1,ee_2011_bg_cat2,ee_2011_bg_cat3,ee_2011_bg_cat4,mumu_2011_bg_cat1,mumu_2011_bg_cat2,mumu_2011_bg_cat3,mumu_2011_bg_cat4),RooArgList(ee_2011_bg_cat1_frac,ee_2011_bg_cat2_frac,ee_2011_bg_cat3_frac,ee_2011_bg_cat4_frac,mumu_2011_bg_cat1_frac,mumu_2011_bg_cat2_frac,mumu_2011_bg_cat3_frac,mumu_2011_bg_cat4_frac))

  totalBGpdf_2012_Weight = RooAddPdf("totalBGpdf_2012_Weight","total BG pdf 2012 Weighted",RooArgList(ee_2012_bg_cat1,ee_2012_bg_cat2,ee_2012_bg_cat3,ee_2012_bg_cat4,mumu_2012_bg_cat1,mumu_2012_bg_cat2,mumu_2012_bg_cat3,mumu_2012_bg_cat4), RooArgList(ee_2012_bg_cat1_frac_2012weight,ee_2012_bg_cat2_frac_2012weight,ee_2012_bg_cat3_frac_2012weight,ee_2012_bg_cat4_frac_2012weight,mumu_2012_bg_cat1_frac_2012weight,mumu_2012_bg_cat2_frac_2012weight,mumu_2012_bg_cat3_frac_2012weight,mumu_2012_bg_cat4_frac_2012weight))

  totalBGpdf_2011_Weight = RooAddPdf("totalBGpdf_2011_Weight","total BG pdf 2011 Weighted",RooArgList(ee_2011_bg_cat1,ee_2011_bg_cat2,ee_2011_bg_cat3,ee_2011_bg_cat4,mumu_2011_bg_cat1,mumu_2011_bg_cat2,mumu_2011_bg_cat3,mumu_2011_bg_cat4), RooArgList(ee_2011_bg_cat1_frac_2011weight,ee_2011_bg_cat2_frac_2011weight,ee_2011_bg_cat3_frac_2011weight,ee_2011_bg_cat4_frac_2011weight,mumu_2011_bg_cat1_frac_2011weight,mumu_2011_bg_cat2_frac_2011weight,mumu_2011_bg_cat3_frac_2011weight,mumu_2011_bg_cat4_frac_2011weight))


  '''
### for bands


  #grab the stored fits
#set the weighting fracBtions to 1 for the unweighted pdfs
  ee_2012B_bg_cat1_fracB = RooRealVar("fracB1","fracB1",1); fracPdfList.append(ee_2012_bg_cat1_frac)
  ee_2012B_bg_cat2_fracB = RooRealVar("fracB2","fracB2",1); fracPdfList.append(ee_2012_bg_cat2_frac)
  ee_2012B_bg_cat3_fracB = RooRealVar("fracB3","fracB3",1); fracPdfList.append(ee_2012_bg_cat3_frac)
  ee_2012B_bg_cat4_fracB = RooRealVar("fracB4","fracB4",1); fracPdfList.append(ee_2012_bg_cat4_frac)
  mumu_2012B_bg_cat1_fracB = RooRealVar("fracB5","fracB5",1); fracPdfList.append(mumu_2012_bg_cat1_frac)
  mumu_2012B_bg_cat2_fracB = RooRealVar("fracB6","fracB6",1); fracPdfList.append(mumu_2012_bg_cat2_frac)
  mumu_2012B_bg_cat3_fracB = RooRealVar("fracB7","fracB7",1); fracPdfList.append(mumu_2012_bg_cat3_frac)
  mumu_2012B_bg_cat4_fracB = RooRealVar("fracB8","fracB8",1); fracPdfList.append(mumu_2012_bg_cat4_frac)

  ee_2011B_bg_cat1_fracB = RooRealVar("fracB9","fracB9",1); fracPdfList.append(ee_2011_bg_cat1_frac)
  ee_2011B_bg_cat2_fracB = RooRealVar("fracB10","fracB10",1); fracPdfList.append(ee_2011_bg_cat2_frac)
  ee_2011B_bg_cat3_fracB = RooRealVar("fracB11","fracB11",1); fracPdfList.append(ee_2011_bg_cat3_frac)
  ee_2011B_bg_cat4_fracB = RooRealVar("fracB12","fracB12",1); fracPdfList.append(ee_2011_bg_cat4_frac)
  mumu_2011B_bg_cat1_fracB = RooRealVar("fracB13","fracB13",1); fracPdfList.append(mumu_2011_bg_cat1_frac)
  mumu_2011B_bg_cat2_fracB = RooRealVar("fracB14","fracB14",1); fracPdfList.append(mumu_2011_bg_cat2_frac)
  mumu_2011B_bg_cat3_fracB = RooRealVar("fracB15","fracB15",1); fracPdfList.append(mumu_2011_bg_cat3_frac)
  mumu_2011B_bg_cat4_fracB = RooRealVar("fracB16","fracB16",1); fracPdfList.append(mumu_2011_bg_cat4_frac)


#set the weighting fracBtions for the weighted pdfs
  ee_2012B_bg_cat1_fracB_2012Bweight = RooRealVar("fracB_2012Bweight1","fracB_2012Bweight1",signifFrac2012Dict['elcat1_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat1_frac_2012weight)
  ee_2012B_bg_cat2_fracB_2012Bweight = RooRealVar("fracB_2012Bweight2","fracB_2012Bweight2",signifFrac2012Dict['elcat2_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat2_frac_2012weight)
  ee_2012B_bg_cat3_fracB_2012Bweight = RooRealVar("fracB_2012Bweight3","fracB_2012Bweight3",signifFrac2012Dict['elcat3_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat3_frac_2012weight)
  ee_2012B_bg_cat4_fracB_2012Bweight = RooRealVar("fracB_2012Bweight4","fracB_2012Bweight4",signifFrac2012Dict['elcat4_2012']); frac_2012weightPdfList.append(ee_2012_bg_cat4_frac_2012weight)
  mumu_2012B_bg_cat1_fracB_2012Bweight = RooRealVar("fracB_2012Bweight5","fracB_2012Bweight5",signifFrac2012Dict['mucat1_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat1_frac_2012weight)
  mumu_2012B_bg_cat2_fracB_2012Bweight = RooRealVar("fracB_2012Bweight6","fracB_2012Bweight6",signifFrac2012Dict['mucat2_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat2_frac_2012weight)
  mumu_2012B_bg_cat3_fracB_2012Bweight = RooRealVar("fracB_2012Bweight7","fracB_2012Bweight7",signifFrac2012Dict['mucat3_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat3_frac_2012weight)
  mumu_2012B_bg_cat4_fracB_2012Bweight = RooRealVar("fracB_2012Bweight8","fracB_2012Bweight8",signifFrac2012Dict['mucat4_2012']); frac_2012weightPdfList.append(mumu_2012_bg_cat4_frac_2012weight)

  ee_2011B_bg_cat1_fracB_2011Bweight = RooRealVar("fracB_2011Bweight9","fracB_2011Bweight9",signifFrac2011Dict['elcat1_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat1_frac_2011weight)
  ee_2011B_bg_cat2_fracB_2011Bweight = RooRealVar("fracB_2011Bweight10","fracB_2011Bweight10",signifFrac2011Dict['elcat2_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat2_frac_2011weight)
  ee_2011B_bg_cat3_fracB_2011Bweight = RooRealVar("fracB_2011Bweight11","fracB_2011Bweight11",signifFrac2011Dict['elcat3_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat3_frac_2011weight)
  ee_2011B_bg_cat4_fracB_2011Bweight = RooRealVar("fracB_2011Bweight12","fracB_2011Bweight12",signifFrac2011Dict['elcat4_2011']); frac_2011weightPdfList.append(ee_2011_bg_cat4_frac_2011weight)
  mumu_2011B_bg_cat1_fracB_2011Bweight = RooRealVar("fracB_2011Bweight13","fracB_2011Bweight13",signifFrac2011Dict['mucat1_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat1_frac_2011weight)
  mumu_2011B_bg_cat2_fracB_2011Bweight = RooRealVar("fracB_2011Bweight14","fracB_2011Bweight14",signifFrac2011Dict['mucat2_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat2_frac_2011weight)
  mumu_2011B_bg_cat3_fracB_2011Bweight = RooRealVar("fracB_2011Bweight15","fracB_2011Bweight15",signifFrac2011Dict['mucat3_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat3_frac_2011weight)
  mumu_2011B_bg_cat4_fracB_2011Bweight = RooRealVar("fracB_2011Bweight16","fracB_2011Bweight16",signifFrac2011Dict['mucat4_2011']); frac_2011weightPdfList.append(mumu_2011_bg_cat4_frac_2011weight)

  ee_2012B_bg_cat1_fracB_ALLweight = RooRealVar("fracB_ALLweight1"    , "fracB_ALLweight1"  , signifFracAllDict['elcat1_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat1_frac_ALLweight)
  ee_2012B_bg_cat2_fracB_ALLweight = RooRealVar("fracB_ALLweight2"    , "fracB_ALLweight2"  , signifFracAllDict['elcat2_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat2_frac_ALLweight)
  ee_2012B_bg_cat3_fracB_ALLweight = RooRealVar("fracB_ALLweight3"    , "fracB_ALLweight3"  , signifFracAllDict['elcat3_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat3_frac_ALLweight)
  ee_2012B_bg_cat4_fracB_ALLweight = RooRealVar("fracB_ALLweight4"    , "fracB_ALLweight4"  , signifFracAllDict['elcat4_2012']); frac_ALLweightPdfList.append(ee_2012_bg_cat4_frac_ALLweight)
  mumu_2012B_bg_cat1_fracB_ALLweight = RooRealVar("fracB_ALLweight5"  , "fracB_ALLweight5"  , signifFracAllDict['mucat1_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat1_frac_ALLweight)
  mumu_2012B_bg_cat2_fracB_ALLweight = RooRealVar("fracB_ALLweight6"  , "fracB_ALLweight6"  , signifFracAllDict['mucat2_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat2_frac_ALLweight)
  mumu_2012B_bg_cat3_fracB_ALLweight = RooRealVar("fracB_ALLweight7"  , "fracB_ALLweight7"  , signifFracAllDict['mucat3_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat3_frac_ALLweight)
  mumu_2012B_bg_cat4_fracB_ALLweight = RooRealVar("fracB_ALLweight8"  , "fracB_ALLweight8"  , signifFracAllDict['mucat4_2012']); frac_ALLweightPdfList.append(mumu_2012_bg_cat4_frac_ALLweight)
  ee_2011B_bg_cat1_fracB_ALLweight = RooRealVar("fracB_ALLweight9"    , "fracB_ALLweight9"  , signifFracAllDict['elcat1_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat1_frac_ALLweight)
  ee_2011B_bg_cat2_fracB_ALLweight = RooRealVar("fracB_ALLweight10"   , "fracB_ALLweight10" , signifFracAllDict['elcat2_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat2_frac_ALLweight)
  ee_2011B_bg_cat3_fracB_ALLweight = RooRealVar("fracB_ALLweight11"   , "fracB_ALLweight11" , signifFracAllDict['elcat3_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat3_frac_ALLweight)
  ee_2011B_bg_cat4_fracB_ALLweight = RooRealVar("fracB_ALLweight12"   , "fracB_ALLweight12" , signifFracAllDict['elcat4_2011']); frac_ALLweightPdfList.append(ee_2011_bg_cat4_frac_ALLweight)
  mumu_2011B_bg_cat1_fracB_ALLweight = RooRealVar("fracB_ALLweight13" , "fracB_ALLweight13" , signifFracAllDict['mucat1_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat1_frac_ALLweight)
  mumu_2011B_bg_cat2_fracB_ALLweight = RooRealVar("fracB_ALLweight14" , "fracB_ALLweight14" , signifFracAllDict['mucat2_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat2_frac_ALLweight)
  mumu_2011B_bg_cat3_fracB_ALLweight = RooRealVar("fracB_ALLweight15" , "fracB_ALLweight15" , signifFracAllDict['mucat3_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat3_frac_ALLweight)
  mumu_2011B_bg_cat4_fracB_ALLweight = RooRealVar("fracB_ALLweight16" , "fracB_ALLweight16" , signifFracAllDict['mucat4_2011']); frac_ALLweightPdfList.append(mumu_2011_bg_cat4_frac_ALLweight)



# add up the pdfs for all cats and years and flavors
  totalBGpdf_2012B = RooAddPdf("totalBGpdf_2012B","total BG pdf 2012B",RooArgList(ee_2012B_bg_cat1,ee_2012B_bg_cat2,ee_2012B_bg_cat3,ee_2012B_bg_cat4,mumu_2012B_bg_cat1,mumu_2012B_bg_cat2,mumu_2012B_bg_cat3,mumu_2012B_bg_cat4), RooArgList(ee_2012_bg_cat1_frac,ee_2012_bg_cat2_frac,ee_2012_bg_cat3_frac,ee_2012_bg_cat4_frac,mumu_2012_bg_cat1_frac,mumu_2012_bg_cat2_frac,mumu_2012_bg_cat3_frac,mumu_2012_bg_cat4_frac))

  totalBGpdf_2011B = RooAddPdf("totalBGpdf_2011B","total BG pdf 2011B",RooArgList(ee_2011B_bg_cat1,ee_2011B_bg_cat2,ee_2011B_bg_cat3,ee_2011B_bg_cat4,mumu_2011B_bg_cat1,mumu_2011B_bg_cat2,mumu_2011B_bg_cat3,mumu_2011B_bg_cat4), RooArgList(ee_2011_bg_cat1_frac,ee_2011_bg_cat2_frac,ee_2011_bg_cat3_frac,ee_2011_bg_cat4_frac,mumu_2011_bg_cat1_frac,mumu_2011_bg_cat2_frac,mumu_2011_bg_cat3_frac,mumu_2011_bg_cat4_frac))

  totalBGpdf_2012B_Weight = RooAddPdf("totalBGpdf_2012B_Weight","total BG pdf 2012B Weighted",RooArgList(ee_2012B_bg_cat1,ee_2012B_bg_cat2,ee_2012B_bg_cat3,ee_2012B_bg_cat4,mumu_2012B_bg_cat1,mumu_2012B_bg_cat2,mumu_2012B_bg_cat3,mumu_2012B_bg_cat4), RooArgList(ee_2012_bg_cat1_frac_2012weight,ee_2012_bg_cat2_frac_2012weight,ee_2012_bg_cat3_frac_2012weight,ee_2012_bg_cat4_frac_2012weight,mumu_2012_bg_cat1_frac_2012weight,mumu_2012_bg_cat2_frac_2012weight,mumu_2012_bg_cat3_frac_2012weight,mumu_2012_bg_cat4_frac_2012weight))

  totalBGpdf_2011B_Weight = RooAddPdf("totalBGpdf_2011B_Weight","total BG pdf 2011B Weighted",RooArgList(ee_2011B_bg_cat1,ee_2011B_bg_cat2,ee_2011B_bg_cat3,ee_2011B_bg_cat4,mumu_2011B_bg_cat1,mumu_2011B_bg_cat2,mumu_2011B_bg_cat3,mumu_2011B_bg_cat4), RooArgList(ee_2011_bg_cat1_frac_2011weight,ee_2011_bg_cat2_frac_2011weight,ee_2011_bg_cat3_frac_2011weight,ee_2011_bg_cat4_frac_2011weight,mumu_2011_bg_cat1_frac_2011weight,mumu_2011_bg_cat2_frac_2011weight,mumu_2011_bg_cat3_frac_2011weight,mumu_2011_bg_cat4_frac_2011weight))
  '''



  # the 2011+2012 ones are too big to define like we did above, so we have to build them out of RooArgSets then convert them back into RooArgLists
  allBGpdfsSet = RooArgSet()
  allBGfracsSet = RooArgSet()
  allBGfracsWeightedSet = RooArgSet()
  print len(bgPdfList)
  for bg, frac in zip(bgPdfList,fracPdfList):
    allBGpdfsSet.add(bg)
    allBGfracsSet.add(frac)
  for frac in frac_ALLweightPdfList:
    allBGfracsWeightedSet.add(frac)
  frac_ALLunweightPdfList = []
  for i in range(0,16):
    tmpShit = RooRealVar('nofrac'+str(i),'nofrac'+str(i),1)
    frac_ALLunweightPdfList.append(tmpShit)

  allBGpdfsList = RooArgList(allBGpdfsSet)
  allBGfracsList = RooArgList(allBGfracsSet)
  allBGfracsWeightedList = RooArgList(allBGfracsWeightedSet)


  print 'debug1'
  allBGpdfsList.Print()
  allBGfracsList.Print()
  totalBGpdf_All = RooAddPdf("totalBGpdf_All","total BG pdf All",allBGpdfsList,allBGfracsList)
  print 'debug2'
  totalBGpdf_All_Weighted = RooAddPdf("totalBGpdf_All","total BG pdf All",allBGpdfsList,allBGfracsWeightedList)

  data_muon_2012 = []
  data_electron_2012 = []
  data_muon_2011 = []
  data_electron_2011 = []
  data_muon_2012_Weight2012 = []
  data_electron_2012_Weight2012 = []
  data_muon_2011_Weight2011 = []
  data_electron_2011_Weight2011 = []
  data_muon_2012_WeightAll = []
  data_electron_2012_WeightAll = []
  data_muon_2011_WeightAll = []
  data_electron_2011_WeightAll = []

#  get all the data together
  for i in range(1,5):
#    data_muon_2012.append(myws_muon_2012.data('dsdatacat'+str(i)))

    data_muon_2012.append(myws_muon_2012.data('dsdatacat'+str(i)))
    data_electron_2012.append(myws_electron_2012.data('dsdatacat'+str(i)))
    data_muon_2011.append(myws_muon_2011.data('dsdatacat'+str(i)))
    data_electron_2011.append(myws_electron_2011.data('dsdatacat'+str(i)))

    tmpMu2011_2011 = myws_muon_2011.data('dsdatacat'+str(i)).Clone()
    tmpMu2011_All  = myws_muon_2011.data('dsdatacat'+str(i)).Clone()
    tmpEl2011_2011 = myws_electron_2011.data('dsdatacat'+str(i)).Clone()
    tmpEl2011_All  = myws_electron_2011.data('dsdatacat'+str(i)).Clone()
    tmpMu2012_2012 = myws_muon_2012.data('dsdatacat'+str(i)).Clone()
    tmpMu2012_All  = myws_muon_2012.data('dsdatacat'+str(i)).Clone()
    tmpEl2012_2012 = myws_electron_2012.data('dsdatacat'+str(i)).Clone()
    tmpEl2012_All  = myws_electron_2012.data('dsdatacat'+str(i)).Clone()

# add a weight column to each data group for the signif weighting
    wgt = RooFormulaVar("wgt","wgt",str(signifFrac2011Dict['mucat'+str(i)+'_2011']),RooArgList(mzg_muon_2012))
    tmpMu2011_2011.addColumn(wgt)
    tmpMu2011_2011_W = RooDataSet(tmpMu2011_2011.GetName(),tmpMu2011_2011.GetTitle(),tmpMu2011_2011,tmpMu2011_2011.get(),'','wgt')

    wgt = RooFormulaVar("wgt","wgt",str(signifFrac2011Dict['elcat'+str(i)+'_2011']),RooArgList(mzg_muon_2012))
    tmpEl2011_2011.addColumn(wgt)
    tmpEl2011_2011_W = RooDataSet(tmpEl2011_2011.GetName(),tmpEl2011_2011.GetTitle(),tmpEl2011_2011,tmpEl2011_2011.get(),'','wgt')

    data_muon_2011_Weight2011.append(tmpMu2011_2011_W)
    data_electron_2011_Weight2011.append(tmpEl2011_2011_W)

    wgt = RooFormulaVar("wgt","wgt",str(signifFracAllDict['mucat'+str(i)+'_2011']),RooArgList(mzg_muon_2012))
    tmpMu2011_All.addColumn(wgt)
    tmpMu2011_All_W = RooDataSet(tmpMu2011_All.GetName(),tmpMu2011_All.GetTitle(),tmpMu2011_All,tmpMu2011_All.get(),'','wgt')

    wgt = RooFormulaVar("wgt","wgt",str(signifFracAllDict['elcat'+str(i)+'_2011']),RooArgList(mzg_muon_2012))
    tmpEl2011_All.addColumn(wgt)
    tmpEl2011_All_W = RooDataSet(tmpEl2011_All.GetName(),tmpEl2011_All.GetTitle(),tmpEl2011_All,tmpEl2011_All.get(),'','wgt')

    data_muon_2011_WeightAll.append(tmpMu2011_All_W)
    data_electron_2011_WeightAll.append(tmpEl2011_All_W)


    wgt = RooFormulaVar("wgt","wgt",str(signifFrac2012Dict['mucat'+str(i)+'_2012']),RooArgList(mzg_muon_2012))
    tmpMu2012_2012.addColumn(wgt)
    tmpMu2012_2012_W = RooDataSet(tmpMu2012_2012.GetName(),tmpMu2012_2012.GetTitle(),tmpMu2012_2012,tmpMu2012_2012.get(),'','wgt')

    wgt = RooFormulaVar("wgt","wgt",str(signifFrac2012Dict['elcat'+str(i)+'_2012']),RooArgList(mzg_muon_2012))
    tmpEl2012_2012.addColumn(wgt)
    tmpEl2012_2012_W = RooDataSet(tmpEl2012_2012.GetName(),tmpEl2012_2012.GetTitle(),tmpEl2012_2012,tmpEl2012_2012.get(),'','wgt')

    data_muon_2012_Weight2012.append(tmpMu2012_2012_W)
    data_electron_2012_Weight2012.append(tmpEl2012_2012_W)

    wgt = RooFormulaVar("wgt","wgt",str(signifFracAllDict['mucat'+str(i)+'_2012']),RooArgList(mzg_muon_2012))
    tmpMu2012_All.addColumn(wgt)
    tmpMu2012_All_W = RooDataSet(tmpMu2012_All.GetName(),tmpMu2012_All.GetTitle(),tmpMu2012_All,tmpMu2012_All.get(),'','wgt')

    wgt = RooFormulaVar("wgt","wgt",str(signifFracAllDict['elcat'+str(i)+'_2012']),RooArgList(mzg_muon_2012))
    tmpEl2012_All.addColumn(wgt)
    tmpEl2012_All_W = RooDataSet(tmpEl2012_All.GetName(),tmpEl2012_All.GetTitle(),tmpEl2012_All,tmpEl2012_All.get(),'','wgt')

    data_muon_2012_WeightAll.append(tmpMu2012_All_W)
    data_electron_2012_WeightAll.append(tmpEl2012_All_W)

#  raw_input('Hit any key to continue')
  print 'got data'

  data_total_2012 = RooDataSet('totalData2012','all data',RooArgSet(mzg_muon_2012))
  data_total_2011 = RooDataSet('totalData2011','all data',RooArgSet(mzg_muon_2012))
  data_total_All = RooDataSet('totalDataAll','all data',RooArgSet(mzg_muon_2012))
  data_total_2012W = RooDataSet('totalData2012W','all data',RooArgSet(mzg_muon_2012))
  data_total_AllW = RooDataSet('totalDataAllW','all data',RooArgSet(mzg_muon_2012))

# add the data together

  data_list_all = data_electron_2012+data_muon_2012+data_electron_2011+data_muon_2011
  for datacat in data_muon_2012:
    data_total_2012.append(datacat)
    data_total_All.append(datacat)
  for datacat in data_electron_2012:
    data_total_2012.append(datacat)
    data_total_All.append(datacat)
  for datacat in data_muon_2011:
    data_total_2011.append(datacat)
    data_total_All.append(datacat)
  for datacat in data_electron_2011:
    data_total_2011.append(datacat)
    data_total_All.append(datacat)

  for datacat in data_muon_2011_Weight2011[1:]:
    data_muon_2011_Weight2011[0].append(datacat)
  for datacat in data_electron_2011_Weight2011:
    data_muon_2011_Weight2011[0].append(datacat)

  for datacat in data_muon_2012_Weight2012[1:]:
    data_muon_2012_Weight2012[0].append(datacat)
  for datacat in data_electron_2012_Weight2012:
    data_muon_2012_Weight2012[0].append(datacat)

  for datacat in data_muon_2011_WeightAll[1:]:
    data_muon_2011_WeightAll[0].append(datacat)
  for datacat in data_electron_2011_WeightAll:
    data_muon_2011_WeightAll[0].append(datacat)
  for datacat in data_muon_2012_WeightAll:
    data_muon_2011_WeightAll[0].append(datacat)
  for datacat in data_electron_2012_WeightAll:
    data_muon_2011_WeightAll[0].append(datacat)

  data_muon_2011_Weight2011[0].Print()
  data_muon_2012_Weight2012[0].Print()
  data_muon_2011_WeightAll[0].Print()
  #raw_input('Hit any key to continue')

  c = TCanvas("c","c",0,0,500,400);
  #dataDict = {'2012':data_total_2012,'2011':data_total_2011,'All':data_total_All}
  dataDict = {'All':data_total_All,'Single':data_electron_2012[0]}
  dataDictWeight = {'2012':data_muon_2012_Weight2012[0],'2011':data_muon_2011_Weight2011[0],'All':data_muon_2011_WeightAll[0],'Single':data_electron_2012[0]}
  pdfDict = {'2012':totalBGpdf_2012,'2011':totalBGpdf_2011,'All':totalBGpdf_All,'Single':bgPdfList[0]}
  pdfDictWeight = {'2012':totalBGpdf_2012_Weight,'2011':totalBGpdf_2011_Weight,'All':totalBGpdf_All_Weighted,'Single':bgPdfList[0]}
  #binningDict = {'1 GeV':80,'2 GeV':40,'2.5 GeV':32,'3.2 GeV':25,'4 GeV':20}
  binningDict = {'2 GeV':45}

#  pdfDictB = {'2012':totalBGpdf_2012B,'2011':totalBGpdf_2011B,'All':totalBGpdf_AllB}
#  pdfDictWeight = {'2012':totalBGpdf_2012_WeightB,'2011':totalBGpdf_2011_WeightB,'All':totalBGpdf_All_WeightedB}
#  binningDictB = {'1 GeV':80,'2 GeV':40,'2.5 GeV':32,'3.2 GeV':25,'4 GeV':20}

# make plots for 2011, 2012, 2011+2012, various binnings
  h1 = TH1F("h1", "h1", 90, 100, 190);
  fit1 = TH1F("Fith", "", 100, 0, 100)
  fitSB1 = TH1F("FitSB", "", 100, 0, 100)
  chan1 = TLatex()
  L1 = TLatex()
  sigma1 = TH1F("Fits", "", 100, 0, 100)
  sigma2 = TH1F("Fit2", "", 100, 0, 100)
  leg1 = TLegend(0.38, 0.72, 0.68, 0.90)
  leg2 = TLegend(0.55, 0.55, 0.75, 0.68)

  if makeNewResults:
    ws =RooWorkspace("ws")
    pdfDict['All'].Print()
    allParams = pdfDict['All'].getParameters(RooArgSet(mzg_muon_2012))
    allParams.Print()

    #for letter in 'ABCD':
      #for lep in ['ee','mumu']:
        #for year in ['2011','2012']:
          #      allParams.find('mzg_bkg_norm'+letter+'_'+lep+'_'+year).setConstant(kTRUE)
    #  for number in '12345':
    #    allParams.find('c'+number+letter).setConstant(kTRUE)

    raw_input('Hit any key to continue')
    fit_s = pdfDict['All'].fitTo(dataDict['All'],RooFit.Save(), RooFit.Strategy(1))
    fit_s.SetName("totalpolyfitres")
    getattr(ws,'import')(fit_s)
    ws.writeToFile('fullpolyws.root')
    raw_input('Hit any key to continue')
    return


  for year in dataDict.keys():
    for width in binningDict.keys():
      mzg_muon_2012.setRange(100,190)
      mzg_muon_2012.setBins(45)
      frame = mzg_muon_2012.frame()
      dataDict[year].plotOn(frame,RooFit.Binning(binningDict[width]))
      pdfDict[year].plotOn(frame)
      frame.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
      frame.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
      frame.GetYaxis().CenterTitle()
      frame.SetTitleOffset(1.2,"Y")
      frame.SetTitle('Combined data '+year+', '+width)
      frame.Draw()

      onesigma = TGraphAsymmErrors()
      twosigma = TGraphAsymmErrors()
      tmpCurve = RooCurve(frame.getObject(int(frame.numItems())-1))
#test the error bands
      if year == 'All' and width == '2 GeV':
        #fit_s = pdfDict[year].fitTo(dataDict[year],RooFit.Save())
        #pdfDict[year].plotOn(frame, RooFit.Range('oldRegion'),RooFit.VisualizeError(fit_s))
        #doBandsFit(onesigma, twosigma, mzg_muon_2012, pdfDict[year], tmpCurve, dataDict[year], frame)
        doBandsNew(onesigma, twosigma, mzgList, pdfDict[year], bgPdfList, bgNormList, dataDict[year], frame, fitres, tmpCurve, frac_ALLunweightPdfList,1)
        twosigma.SetLineColor(kYellow)
        twosigma.SetFillColor(kYellow)
        twosigma.SetMarkerColor(kYellow)

        onesigma.SetLineColor(kGreen)
        onesigma.SetFillColor(kGreen)
        onesigma.SetMarkerColor(kGreen)
      frame.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
      frame.GetXaxis()
      h1.SetMarkerStyle(20)
      h1.SetMarkerColor(kBlack)
      h1.SetLineColor(1)
      frame.Draw("e0")
      frame.SetTitle("")
      frame.SetYTitle("Events / {0}".format(width))
      twosigma.Draw("L3 same")
      onesigma.Draw("L3 same")
      frame.Draw("e0same")
      allSignal.Scale(75)
      allSignal.Rebin(2)
      allSignal.SetLineColor(kRed)
      allSignal.SetLineWidth(2)
      allSignal.Draw('samehist')

      L1.SetNDC()
      L1.SetTextSize(0.045)
      L1.SetTextFont(62)
      L1.DrawLatex(0.26, 0.955, "#sqrt{s} = 7 TeV, L = 5 fb^{-1} #sqrt{s} = 8 TeV, L = 19.6 fb^{-1}");
      chan1.SetNDC()
      chan1.SetTextSize(0.045)
      chan1.SetTextFont(62)
      chan1.DrawLatex(0.80, 0.87, "H #rightarrow Z #gamma ")
      chan1.DrawLatex(0.15, 0.955, ("CMS"))
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
      leg1.SetTextSize(0.045)
      leg2.SetFillColor(0)
      leg2.SetFillStyle(0)
      leg2.SetShadowColor(0)
      leg2.SetBorderSize(0)
      leg2.SetTextFont(62)
      leg2.SetTextSize(0.045)
      leg1.AddEntry(h1, "Data", "pl")
      leg1.AddEntry(fitSB1, "Background Model", "l")
      leg1.AddEntry(allSignal, "Signal m_{H} = 125 GeV x 75", "l")
      leg2.AddEntry(sigma1, "#pm 1 #sigma", "f")
      leg2.AddEntry(sigma2, "#pm 2 #sigma", "f")
      leg1.Draw()
      leg2.Draw()
      c.Print('combinedData_'+year+'_'+width.replace(' ','')+'.pdf')
      c.Clear()
      leg1.Clear()
      leg2.Clear()

      frameW = mzg_muon_2012.frame(100,190)

      #RooDataSet::[CMS_hzg_mass,weight:wgt] = 5083 entries (621.642 weighted)
      #RooDataSet::[CMS_hzg_mass,weight:wgt] = 25874 entries (2999.21 weighted)
      #RooDataSet::[CMS_hzg_mass,weight:wgt] = 30957 entries (1781.36 weighted)

#make a scale to renormalize the weighted sets to the original yield
      if year == '2012': scale = 25874/2999.21
      elif year == '2011': scale = 5083/621.642
      else: scale = 30957/1781.36

      dataDictWeight[year].plotOn(frameW,RooFit.Binning(binningDict[width]),RooFit.Rescale(scale))
      pdfDictWeight[year].plotOn(frameW,RooFit.Normalization(scale))
      frameW.GetXaxis().SetTitle('m_{ll#gamma} (GeV)')
      frameW.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
      frameW.GetYaxis().CenterTitle()
      frameW.SetTitleOffset(1.2,"Y")
      frameW.SetTitle('Combined data '+year+', '+width+', Weighted to S/(S+B)')
      frameW.SetMaximum(frame.GetMaximum())
      frameW.SetMinimum(frame.GetMinimum())
      frameW.Draw()
      frameW.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
      frameW.GetXaxis()
      tmpCurve = RooCurve(frameW.getObject(int(frameW.numItems())-1))
      if year == 'All' and width == '2 GeV':
        #fit_s = pdfDict[year].fitTo(dataDict[year],RooFit.Save())
        #pdfDict[year].plotOn(frame, RooFit.Range('oldRegion'),RooFit.VisualizeError(fit_s))
        #doBandsFit(onesigma, twosigma, mzg_muon_2012, pdfDict[year], tmpCurve, dataDict[year], frame)
        doBandsNew(onesigma, twosigma, mzgList, pdfDict[year], bgPdfList, bgNormList, dataDict[year], frame, fitres, tmpCurve, frac_ALLweightPdfList, scale)
        twosigma.SetLineColor(kYellow)
        twosigma.SetFillColor(kYellow)
        twosigma.SetMarkerColor(kYellow)

        onesigma.SetLineColor(kGreen)
        onesigma.SetFillColor(kGreen)
        onesigma.SetMarkerColor(kGreen)
      h1.SetMarkerStyle(20)
      h1.SetMarkerColor(kBlack)
      h1.SetLineColor(1)
      frameW.Draw("e0")
      twosigma.Draw("L3 same")
      onesigma.Draw("L3 same")
      frameW.SetTitle("")
      frameW.SetYTitle("Events / {0}".format(width))
      frameW.Draw("e0same")

      allSignal.Draw('samehist')
      L1.SetNDC()
      L1.SetTextSize(0.045)
      L1.SetTextFont(62)
      L1.DrawLatex(0.39, 0.90, ('#sqrt{s} = 7 TeV, L = 5.0 fb^{-1}'))
      L1.DrawLatex(0.39, 0.85, ('#sqrt{s} = 8 TeV, L = 19.6 fb^{-1}'))
      L1.DrawLatex(0.39, 0.80, ('Electron + muon channels'))
      chan1.SetNDC()
      chan1.SetTextSize(0.045)
      chan1.SetTextFont(62)
      chan1.DrawLatex(0.45, 0.96, "H #rightarrow Z #gamma Weighted to S/(S+B)")
      chan1.DrawLatex(0.15, 0.96, ("CMS"))
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
      leg1.SetTextSize(0.035)
      leg2.SetFillColor(0)
      leg2.SetFillStyle(0)
      leg2.SetShadowColor(0)
      leg2.SetBorderSize(0)
      leg2.SetTextFont(62)
      leg2.SetTextSize(0.035)
      leg1.AddEntry(h1, "Data", "pl")
      leg1.AddEntry(fitSB1, "Background Model", "l")
      leg1.AddEntry(allSignal, "Signal m_{H} = 125 GeV x 100", "l")
      leg2.AddEntry(sigma1, "#pm 1 #sigma", "f")
      leg2.AddEntry(sigma2, "#pm 2 #sigma", "f")
      leg1.Draw()
      leg2.Draw()

      c.Print('combinedData_'+year+'_'+width.replace(' ','')+'_Weighted.pdf')
      leg1.Clear()
      leg2.Clear()

def doBandsFit(onesigma, twosigma, hmass, cpdf, nomcurve, datanorm, plot):
  nlim = RooRealVar("nlim","",0,0,1e+5)
  print 'total steps needed:', plot.GetXaxis().GetNbins()
  for i in range(1,plot.GetXaxis().GetNbins()+1):
    lowedge = plot.GetXaxis().GetBinLowEdge(i)
    upedge = plot.GetXaxis().GetBinUpEdge(i)
    center = plot.GetXaxis().GetBinCenter(i)
    nombkg = nomcurve.interpolate(center)
    print 'nombkg', nombkg
    nlim.setVal(nombkg)
    hmass.setRange("errRange",lowedge,upedge)
    #RooAbsPdf *epdf = 0
    epdf = RooExtendPdf("epdf","",cpdf,nlim,"errRange")
    #nll = epdf.createNLL(datanorm,RooFit.Extended(),RooFit.NumCPU(24))
    nll = epdf.createNLL(datanorm,RooFit.Extended())
    minim = RooMinimizer(nll)
    minim.setStrategy(0)
    minim.setPrintLevel(-1)
    clone = 1.0 - 2.0*(RooStats.SignificanceToPValue(1.0))
    cltwo = 1.0 - 2.0*(RooStats.SignificanceToPValue(2.0))
    print 'clone', clone, 'cltwo', cltwo
    minim.migrad()
    #minim.hesse()
    minim.minos(RooArgSet(nlim))
    print 'one errHi', nlim.getErrorHi(), 'one errLo', nlim.getErrorLo()
    onesigma.SetPoint(i-1,center,nombkg)
    onesigma.SetPointError(i-1,0.,0.,-nlim.getErrorLo(),nlim.getErrorHi())

    minim.setErrorLevel(0.5*pow(ROOT.Math.normal_quantile(1-0.5*(1-cltwo),1.0),2)) #0.5 is because qmu is -2*NLL
    # eventually if cl = 0.95 this is the usual 1.92!
    minim.migrad()
    minim.minos(RooArgSet(nlim))
    #minim.hesse()
    twosigma.SetPoint(i-1,center,nombkg)
    twosigma.SetPointError(i-1,0.,0.,-nlim.getErrorLo(),nlim.getErrorHi())
    print 'two errHi', nlim.getErrorHi(), 'two errLo', nlim.getErrorLo()
  onesigma.Print("V")
  twosigma.Print("V")

def doBandsNew(onesigma, twosigma, hmassList, cpdf, pdfList, normList, datanorm, plot, fit_s, nomcurve, weightList, weightScale):
  if verbose:
    print 'fit_s'
    fit_s.Print()
  for ibin in range(1,plot.GetXaxis().GetNbins()+1):
    for hmass in hmassList:
      hmass.setRange("binrange",plot.GetXaxis().GetBinLowEdge(ibin),plot.GetXaxis().GetBinUpEdge(ibin))
    binwcatnorms = RooArgSet('binwcatnorm')
    #binwcatnorms.Print()
    bkgsumw2 = 0.
    bincatnormsTmpList= []
    #for pdfcat,normcat in zip(pdfList,normList):
    for i in range (0,16):
      bcatpdf = pdfList[i]
      catnorm = normList[i]
      if i < 4: j=0
      elif i<8: j=1
      elif i<12: j=2
      else: j=3
      #catweight = weightscale*catweights[i]
      catweight = weightList[i].getValV()*weightScale
      catintegral = bcatpdf.createIntegral(RooArgSet(hmassList[j]),RooArgSet(hmassList[j]),"binrange")
      #catintegral = bcatpdf.createIntegral(RooArgSet(hmassList[j]),"binrange")
      catintegralFull = bcatpdf.createIntegral(RooArgSet(hmassList[j]))
      if verbose:
        print 'catnorm:', catnorm
        print 'catweight:',catweight
        print 'catintegral:', catintegral
        print 'catintegralFull:', catintegralFull

      binwcatnorm = RooProduct('catnorm_bin_'+str(ibin)+'_channel_'+str(i),'',RooArgSet(RooFit.RooConst(catweight),catnorm,catintegral))
      #binwcatnorm = RooProduct('catnorm_bin_'+str(ibin)+'_channel_'+str(i),'',RooArgSet(RooFit.RooConst(catweight),catintegral))
      bincatnormsTmpList.append(binwcatnorm)
      #bkgsumw2 += catintegral.getVal()*catnorm.getVal()*catweight*catweight
      if verbose:
        print
        print 'binrangelow:', plot.GetXaxis().GetBinLowEdge(ibin), 'binrangehigh:', plot.GetXaxis().GetBinUpEdge(ibin)
        print 'hmass:'
        hmassList[j].Print()
        print 'ibin:',ibin, 'bgchannel:', i
        print 'bcatpdf:'
        bcatpdf.Print()
        print 'catnorm:'
        catnorm.Print()
        print 'catintegralFull:'
        catintegralFull.Print()
        print 'catintegral:'
        catintegral.Print()
        print 'binwcatnorm:'
        binwcatnorm.Print()
        raw_input('Hit any key to continue')
    for item in bincatnormsTmpList:
      binwcatnorms.add(item)
    binwnorm = RooAddition('wnorm_'+str(ibin),'', binwcatnorms)
    normerr = binwnorm.getPropagatedError(fit_s)
    nombkg = nomcurve.interpolate(plot.GetXaxis().GetBinCenter(ibin))
    normerr = normerr/2.0
    if verbose:
      print 'binwnorm:'
      binwnorm.Print()
      print 'normerr:', normerr
      raw_input('Hit any key to continue')
    #normerr = 1.0
    onesigma.SetPoint(ibin-1,plot.GetXaxis().GetBinCenter(ibin),nombkg)
    twosigma.SetPoint(ibin-1,plot.GetXaxis().GetBinCenter(ibin),nombkg)
    #onesigma.SetPointError(ibin-1,plot.GetXaxis().GetBinWidth(ibin)/2.0,-normerr,normerr)
    #twosigma.SetPointError(ibin-1,plot.GetXaxis().GetBinWidth(ibin)/2.0,-2.0*normerr,2.0*normerr)
    onesigma.SetPointError(ibin-1,0,0,normerr,normerr)
    twosigma.SetPointError(ibin-1,0,0,2.0*normerr,2.0*normerr)
    #errgraphsub.SetPoint(ibin-1,plot.GetXaxis().GetBinCenter(ibin),0.)
    #errgraphsub2.SetPoint(ibin-1,plot.GetXaxis().GetBinCenter(ibin),0.)
    #errgraphsub.SetPointError(ibin-1,plot.GetXaxis().GetBinWidth(ibin)/2.0,sqrt(normerr*normerr+datanorm.GetBinError(ibin)*datanorm.GetBinError(ibin)))
    #errgraphsub2.SetPointError(ibin-1,plot.GetXaxis().GetBinWidth(ibin)/2.0,2.0*sqrt(normerr*normerr+datanorm.GetBinError(ibin)*datanorm.GetBinError(ibin)))
#    hsubdata.SetBinContent(ibin,datanorm.GetBinContent(ibin)-binwnorm.getVal())
#    hsubdata.SetBinError(ibin,datanorm.GetBinError(ibin))
  onesigma.Print("V")
  twosigma.Print("V")
'''
onesigma = TGraphAsymmErrors()
twosigma = TGraphAsymmErrors()

      #doBandsFit(onesigma1, twosigma1, &mzg, GaussBern5Full[i], dynamic_cast<RooCurve*>(tmpframe_2012Bern[i]->getObject(tmpframe_2012Bern[i]->numItems()-1)), ds_data[i], tmpframe_2012Bern[i]);
      #doBandsFit(TGraphAsymmErrors *onesigma, TGraphAsymmErrors *twosigma, RooRealVar * hmass, RooAbsPdf *cpdf, RooCurve *nomcurve,  RooAbsData *datanorm, RooPlot *plot)
nlim = RooRealVar("nlim","",0,0,1e+5)

for i in range(1,frame_2012.GetXaxis().GetNbins()+1):
  lowedge = frame_2012.GetXaxis().GetBinLowEdge(i)
  upedge = frame_2012.GetXaxis().GetBinUpEdge(i)
  center = frame_2012.GetXaxis().GetBinCenter(i)
  print 'numItems', (frame_2012.numItems())
  nombkg = RooCurve(frame_2012.getObject(int(frame_2012.numItems())-1)).interpolate(center)
  print 'nombkg', nombkg
  #nombkg = RooCurve(frame_2012.getObject(1)).interpolate(center)
  nlim.setVal(nombkg)
  mzg_muon_2012.setRange("errRange",lowedge,upedge)
  epdf = RooExtendPdf("epdf","",totalBGpdf,nlim,"errRange")
  epdf.evaluate()
  Oneslow= 0
  Oneshi=0
  Twoslow=0
  Twoshi=0

  step = 0.01
  Oneslow = -nlim.getErrorLo()
  Oneshi = -nlim.getErrorHi()

  print nlim.getErrorLo(),nlim.getErrorHi()
  print nlim.getError()
  Twoslow = -1.9205*nlim.getErrorLo()
  Twoshi = 1.9205*nlim.getErrorHi()
  onesigma.SetPoint(i-1,center,nombkg)
  onesigma.SetPointError(i-1,0.,0.,Oneslow, Oneshi)
  twosigma.SetPoint(i-1,center,nombkg)
  twosigma.SetPointError(i-1,0.,0.,Twoslow, Twoshi)

twosigma.SetLineColor(kGreen)
twosigma.SetFillColor(kGreen)
twosigma.SetMarkerColor(kGreen)

onesigma.SetLineColor(kYellow)
onesigma.SetFillColor(kYellow)
onesigma.SetMarkerColor(kYellow)


totalBGpdf.plotOn(frame_2012, RooFit.Name(totalBGpdf.GetName()),RooFit.LineColor(kBlue),RooFit.LineWidth(1),RooFit.Range("fullRegion"))


#frame_2012.GetXaxis().SetTitleSize(0)
#frame_2012.GetXaxis().SetLabelSize(0.05)
frame_2012.GetXaxis().SetTickLength(gStyle.GetTickLength()/2)
frame_2012.GetXaxis()
h1 = TH1F("h1", "h1", 90, 100, 190);
h1.SetMarkerStyle(20)
h1.SetMarkerColor(kBlack)
h1.SetLineColor(1)
frame_2012.Draw("e0")
twosigma.Draw("L3 same")
onesigma.Draw("L3 same")
frame_2012.SetTitle("title")
frame_2012.Draw("e0same")

L1 = TLatex()
L1.SetNDC()
L1.SetTextSize(0.035)
L1.SetTextFont(62)
L1.DrawLatex(0.25, 0.9, ("All data"))
chan1 = TLatex()
chan1.SetNDC()
chan1.SetTextSize(0.045)
chan1.SetTextFont(62)
chan1.DrawLatex(0.65, 0.9, "H #rightarrow Z #gamma ")
fit1 = TH1F("Fith", "", 100, 0, 100)
fit1.SetLineColor(kBlue)
fit1.SetLineWidth(2)

fitSB1 = TH1F("FitSB", "", 100, 0, 100)
fitSB1.SetLineColor(kBlue)
fitSB1.SetLineWidth(2)


sigma1 = TH1F("Fits", "", 100, 0, 100)
sigma1.SetFillColor(kYellow)
sigma1.SetLineWidth(2)

sigma2 = TH1F("Fit2", "", 100, 0, 100)
sigma2.SetFillColor(kGreen)
sigma2.SetLineWidth(2)


leg1 = TLegend(0.60, 0.65, 0.95, 0.9)
leg1.SetFillColor(0)
leg1.SetFillStyle(0)
leg1.SetShadowColor(0)
leg1.SetBorderSize(0)
leg1.SetTextFont(62)
leg1.SetTextSize(0.035)
leg1.AddEntry(h1, "Data", "pl")
leg1.AddEntry(fitSB1, "Bkg Model", "l")
leg1.AddEntry(sigma1, "#pm 1 #sigma", "f")
leg1.AddEntry(sigma2, "#pm 2 #sigma", "f")
leg1.Draw()
'''
if __name__=="__main__":
  doCombinedBG()
