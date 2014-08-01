#!/usr/bin/env python
import sys
sys.argv.append('-b')
import numpy as np
#import pdb
from signalCBFits import AutoVivification
from rooFitBuilder import *
from xsWeighterNew import *
from ROOT import *
import os
import configLimits as cfl

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

debugPlots = cfl.debugPlots

verbose = cfl.verbose

rootrace = cfl.rootrace

doMVA = cfl.doMVA

allBiasFits= cfl.allBiasFits# Turn on extra fits used in bias studies

suffix = cfl.suffix

YR = cfl.YR

sigFit = cfl.sigFit

highMass = cfl.highMass

dataDict = {'mu2012_4cat':TFile('inputFiles/m_llgFile_MuMu2012ABCD_'+suffix+'.root','r'),'el2012_4cat':TFile('inputFiles/m_llgFile_EE2012ABCD_'+suffix+'.root','r'),'mu2011_4cat':TFile('inputFiles/m_llgFile_MuMu2011ABCD_Proper.root','r'),'el2011_4cat':TFile('inputFiles/m_llgFile_EE2011ABCD_Proper.root','r'),'all2011_4cat':TFile('inputFiles/m_llgFile_All2011ABCD_Proper.root','r')}

signalDict = dataDict

lepton = cfl.leptonList[0]
year = cfl.yearList[0]
cat= cfl.catListSmall[0]
mass = cfl.massList[0]

yearToTeV = {'2011':'7TeV','2012':'8TeV'}

xmin = 100
xmax = 500
binning = (xmin-xmax)/2

weight  = RooRealVar('Weight','Weight',0,100)
mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',xmin,xmax)
#mzg.setRange('full',100,190)
#mzg.setBins(50000,'cache')
#mzg.setBins(1600)

c = TCanvas("c","c",0,0,500,400)
c.cd()


################
# get the data #
################


dataName = '_'.join(['data',lepton,yearToTeV[year],'cat'+cat])
dataTree = dataDict[lepton+year+'_4cat'].Get('m_llg_DATA')
#tmpMassEventOld = np.zeros(1,dtype = 'f')
tmpMassEventOld = np.zeros(1,dtype = 'd')
if cat is '0':
  dataTree.SetBranchAddress('m_llg_DATA',tmpMassEventOld)
else:
  dataTree.SetBranchAddress('m_llgCAT'+cat+'_DATA',tmpMassEventOld)
data_argS = RooArgSet(mzg)
if cat == '5':
  data_ds = RooDataSet(dataName,dataName,data_argS)
else:
  data_ds = RooDataHist(dataName,dataName,data_argS)
for i in range(0,dataTree.GetEntries()):
  dataTree.GetEntry(i)
  if tmpMassEventOld[0]> xmin and tmpMassEventOld[0]<xmax:
    mzg.setVal(tmpMassEventOld[0])
    data_ds.add(data_argS)
dataTree.ResetBranchAddresses()

#############
# make fits #
#############
GaussExp = BuildGaussExp(yearToTeV[year], lepton, cat, mzg)
#GaussBern3,GB3Vars = BuildGaussStepBern3(yearToTeV[year], lepton, cat, mzg, step = 110, sigma = 3)
GaussBern3,GB3Vars = BuildGaussStepBern3Const(yearToTeV[year], lepton, cat, mzg, step = 106.544770522, sigma = 4.09614596913,
 p1 = 7.65736763241e-06, p2 = 2.66641416582, p3 = 0.472714504074   )

GaussExp.Print()
GaussBern3.Print()

GaussExp.fitTo(data_ds,RooFit.Range('full'), RooFit.Strategy(2))
#GaussBern3.fitTo(data_ds, RooFit.Strategy(2))
for arg in GB3Vars:
  print arg.GetName(), arg.getVal()
#mzg.setRange(100,500)

leg  = TLegend(0.7,0.7,1.0,1.0)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetBorderSize(1)
leg.SetHeader('_'.join(['test','fits',year,lepton,'cat'+cat]))
testFrame = mzg.frame()
#data_ds.plotOn(testFrame,RooFit.Binning(binning))
data_ds.plotOn(testFrame)

#GaussExp.plotOn(testFrame,RooFit.Name('GaussExp'))
GaussBern3.plotOn(testFrame,RooFit.LineColor(kViolet),RooFit.Name('GaussBern3'))

testFrame.Draw()
#leg.AddEntry(testFrame.findObject('GaussExp'),'GaussExp','l')
leg.AddEntry(testFrame.findObject('GaussBern3'),'GaussBern3','l')
testFrame.Draw()
c.Print('debugPlots/'+'_'.join(['DEBUG','fits',suffix,year,lepton,'cat'+cat])+'.pdf')


