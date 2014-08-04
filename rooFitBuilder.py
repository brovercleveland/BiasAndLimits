#!/usr/bin/env python
import sys
from ROOT import gSystem
gSystem.Load("libRooFit")
from ROOT import *
import numpy as np

gROOT.SetBatch()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.x RooStepBernstein.cxx+')
gROOT.ProcessLine('.x RooGaussStepBernstein.cxx+')
#gROOT.ProcessLine('.x HZGRooPdfs.cxx++')

def BuildBetaAndBern(tev,lepton,cat,mzg,rangeName,frac = 0.1, fracLow = 0, fracHigh = 0.9):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  beta = BuildBetaFunc(tev,lepton,cat+'BB',mzg,rangeName)
  bern = BuildBern4(tev,lepton,cat+'BB',mzg)
  fracVar = RooRealVar('fracBB_'+suffix,'fracBB_'+suffix,frac,fracLow,fracHigh)
  bbArgs = RooArgList(beta,bern)
  fracArg = RooArgList(fracVar)

  BB = RooAddPdf('BB_'+suffix,'BB_'+suffix,bbArgs,fracArg,True)
  #BB = RooFFTConvPdf('BB_'+suffix,'BB_'+suffix,mzg,beta,bern)
  SetOwnership(beta,0)
  SetOwnership(bern,0)
  SetOwnership(fracVar,0)
  return BB

def BuildGaussAndBern(tev,lepton,cat,mzg,rangeName,frac = 0.1, fracLow = 0, fracHigh = 0.9):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  gauss = BuildRooGaussian(tev,lepton,cat+'GB',mzg)
  bern = BuildBern3(tev,lepton,cat+'GB',mzg)
  fracVar = RooRealVar('fracGB_'+suffix,'fracGB_'+suffix,frac,fracLow,fracHigh)
  gbArgs = RooArgList(gauss,bern)
  fracArg = RooArgList(fracVar)

  GB = RooAddPdf('GB_'+suffix,'GB_'+suffix,gbArgs,fracArg,True)
  #BB = RooFFTConvPdf('BB_'+suffix,'BB_'+suffix,mzg,beta,bern)
  SetOwnership(gauss,0)
  SetOwnership(bern,0)
  SetOwnership(fracVar,0)
  return GB


def BuildBetaFunc(tev,lepton,cat,mzg,rangeName,alpha = 2, alphaLow = 1, alphaHigh = 10, beta = 5, betaLow = 1, betaHigh = 10):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  alphaVar = RooRealVar('alphaBetaFunc_'+suffix,'alphaBetaFunc_'+suffix, alpha, alphaLow, alphaHigh)
  betaVar = RooRealVar('betaBetaFunc_'+suffix,'betaBetaFunc_'+suffix, beta, betaLow, betaHigh)
  xLow = mzg.getMin(rangeName)
  xRange = mzg.getMax(rangeName) - mzg.getMin(rangeName)
  gROOT.ProcessLine('.L betaWrapper.cxx+')
  from ROOT import makeBetaPdf
  BetaFunc = makeBetaPdf('BetaFunc_'+suffix,mzg,alphaVar,betaVar)

  SetOwnership(alphaVar,0)
  SetOwnership(betaVar,0)
  return BetaFunc

def BuildKumaraswamy(tev,lepton,cat,mzg,rangeName,alpha = 2, alphaLow = 1, alphaHigh = 10, beta = 5, betaLow = 1, betaHigh = 10):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  alphaVar = RooRealVar('alphaKumaraswamy_'+suffix,'alphaKumaraswamy_'+suffix, alpha, alphaLow, alphaHigh)
  betaVar = RooRealVar('betaKumaraswamy_'+suffix,'betaKumaraswamy_'+suffix, beta, betaLow, betaHigh)
  xLow = RooRealVar('xLowKumaraswamy_'+suffix, 'xLowKumaraswamy_'+suffix, mzg.getMin(rangeName))
  xRange = RooRealVar('xRangeKumaraswamy_'+suffix, 'xReangeKumaraswamy_'+suffix,mzg.getMax(rangeName) - mzg.getMin(rangeName))
  Kumaraswamy = RooGenericPdf('Kumaraswamy_'+suffix, 'Kumaraswamy_'+suffix, '(@0>@3)*(@0<(@3+@4))*@1*@2*((@0-@3)/@4)**(@1-1)*(1-((@0-@3)/@4)**@1)**(@2)', RooArgList(mzg,alphaVar,betaVar,xLow,xRange))

  SetOwnership(alphaVar,0)
  SetOwnership(betaVar,0)
  SetOwnership(xLow,0)
  SetOwnership(xRange,0)
  return Kumaraswamy

def BuildGaussExp(tev,lepton,cat,mzg,mean = 120, meanLow = 90, meanHigh = 150, sigma = 1, sigmaLow = 0.01, sigmaHigh = 10, tau = 5, tauLow = 0, tauHigh = 50):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussExp_'+suffix,'meanGaussExp_'+suffix, mean, meanLow, meanHigh)
  sigmaVar = RooRealVar('sigmaGaussExp_'+suffix,'sigmaGaussExp_'+suffix,sigma,sigmaLow,sigmaHigh)
  tauVar = RooRealVar('tauGaussExp_'+suffix,'tauGaussExp_'+suffix,tau,tauLow,tauHigh)

  turnOn = RooGaussModel('turnOnGaussExp_'+suffix,'turnOnGaussExp_'+suffix,mzg,meanVar,sigmaVar)
  GaussExp = RooDecay('GaussExp_'+suffix,'GaussExp_'+suffix,mzg,tauVar,turnOn,RooDecay.SingleSided)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(tauVar,0)
  SetOwnership(turnOn,0)
  return GaussExp
  #sprintf(sbuffer1, "GaussExpFullExt_cat%i",i+1);
  #GaussExpFullExt[i] = new RooExtendPdf(sbuffer1,sbuffer1,*GaussExpFull[i],*nGaussExp[i]);
  #nGaussExp[i] = new RooRealVar(sbuffer1,sbuffer1,ntcat[i]->GetEntries(),0,3*ntcat[i]->GetEntries());


def BuildGaussPow(tev,lepton,cat,mzg,mean = 0, sigma = 1, sigmaLow = 0.01, sigmaHigh = 10, alpha = 115, alphaLow = 50, alphaHigh = 200,beta = 2.7, betaLow = 0, betaHigh = 20):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussPow_'+suffix,'meanGaussPow_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussPow_'+suffix,'sigmaGaussPow_'+suffix,sigma,sigmaLow,sigmaHigh)
  alphaVar = RooRealVar('alphaGaussPow_'+suffix,'alphaGaussPow_'+suffix,alpha,alphaLow,alphaHigh)
  betaVar = RooRealVar('betaGaussPow_'+suffix,'betaGaussPow_'+suffix,beta,betaLow,betaHigh)

  turnOn = RooGaussModel('turnOnGaussPow_'+suffix,'turnOnGaussPow_'+suffix,mzg,meanVar,sigmaVar)
  tail = RooGenericPdf('tailGaussPow_'+suffix,'tailGaussPow_'+suffix,'1e-20 + (@0 > @1)*((@0)^(-@2))',RooArgList(mzg,alphaVar,betaVar))
  GaussPow = RooFFTConvPdf('GaussPow_'+suffix,'GaussPow_'+suffix, mzg, tail, turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(alphaVar,0)
  SetOwnership(betaVar,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return GaussPow

def BuildSechExp(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.01, sigmaHigh = 20, tau = 35, tauLow = 0, tauHigh = 100, alpha = 105, alphaLow = 50, alphaHigh = 200):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanSechExp_'+suffix,'meanSechExp_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaSechExp_'+suffix,'sigmaSechExp_'+suffix,sigma,sigmaLow,sigmaHigh)
  tauVar = RooRealVar('tauSechExp_'+suffix,'tauSechExp_'+suffix,tau,tauLow,tauHigh)
  alphaVar = RooRealVar('alphaSechExp_'+suffix,'alphaSechExp_'+suffix,alpha,alphaLow,alphaHigh)

  turnOn  = RooGenericPdf('turnOnSechExp_'+suffix,'turnOnSechExp_'+suffix, 'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(mzg,meanVar,sigmaVar))
  tail    = RooGenericPdf('tailSechExp_'+suffix,'tailSechExp_'+suffix,'1e-20 + (@0 > @1)*(exp(-@0/@2))',RooArgList(mzg,alphaVar,tauVar))
  SechExp = RooFFTConvPdf('SechExp_'+suffix,'SechExp_'+suffix,mzg,tail,turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(alphaVar,0)
  SetOwnership(tauVar,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return SechExp

def BuildSechPow(tev,lepton,cat,mzg,mean = 0, sigma = 4, sigmaLow = 0.01, sigmaHigh = 20, alpha = 107, alphaLow = 50, alphaHigh = 200, beta = 5, betaLow = 0, betaHigh = 20):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanSechPow_'+suffix,'meanSechPow_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaSechPow_'+suffix,'sigmaSechPow_'+suffix,sigma,sigmaLow,sigmaHigh)
  alphaVar = RooRealVar('alphaSechPow_'+suffix,'alphaSechPow_'+suffix,alpha,alphaLow,alphaHigh)
  betaVar = RooRealVar('betaSechPow_'+suffix,'betaSechPow_'+suffix,beta,betaLow,betaHigh)

  turnOn = RooGenericPdf('turnOnSechPow_'+suffix,'turnOnSechPow_'+suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(mzg,meanVar,sigmaVar))
  tail = RooGenericPdf('tailSechPow_'+suffix,'tailSechPow_'+suffix,'1e-20 + (@0 > @1)*((@0)^(-@2))',RooArgList(mzg,alphaVar,betaVar))
  SechPow = RooFFTConvPdf('SechPow_'+suffix,'SechPow_'+suffix, mzg, tail, turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(alphaVar,0)
  SetOwnership(betaVar,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return SechPow

def BuildGaussStepBern3(tev,lepton,cat,mzg,mean = 0, sigma = 4, sigmaLow = 0.01, sigmaHigh = 20, step = 115, stepLow = 100, stepHigh = 130,
    p0 = 15, p1 = 0.3, p1Low = -1e-6, p1High = 900,p2 = 0.3, p2Low = -1e-6, p2High = 900,p3 = 0.3, p3Low = -1e-6, p3High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussBern3_'+suffix,'meanGaussBern3_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussBern3_'+suffix,'sigmaGaussBern3_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepGaussBern3_'+suffix,'stepGaussBern3_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0GaussBern3_'+suffix,'p0GaussBern3_'+suffix, p0)
  p1Var = RooRealVar('p1GaussBern3_'+suffix,'p1GaussBern3_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2GaussBern3_'+suffix,'p2GaussBern3_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3GaussBern3_'+suffix,'p3GaussBern3_'+suffix,p3,p3Low,p3High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
  GaussBern3 = RooGaussStepBernstein('GaussBern3_'+suffix,'GaussBern3_'+suffix,mzg,meanVar,sigmaVar,stepVar,pArgs)

  returnArgs = [meanVar,sigmaVar,stepVar,p0Var,p1Var,p2Var,p3Var]
  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  return GaussBern3,returnArgs

def BuildGaussStepBern3Const(tev,lepton,cat,mzg,mean = 0, sigma = 4, step = 115,
    p0 = 15, p1 = 0.3, p2 = 0.3, p3 = 0.3):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussBern3_'+suffix,'meanGaussBern3_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussBern3_'+suffix,'sigmaGaussBern3_'+suffix,sigma)
  stepVar = RooRealVar('stepGaussBern3_'+suffix,'stepGaussBern3_'+suffix,step)
  p0Var = RooRealVar('p0GaussBern3_'+suffix,'p0GaussBern3_'+suffix,p0)
  p1Var = RooRealVar('p1GaussBern3_'+suffix,'p1GaussBern3_'+suffix,p1)
  p2Var = RooRealVar('p2GaussBern3_'+suffix,'p2GaussBern3_'+suffix,p2)
  p3Var = RooRealVar('p3GaussBern3_'+suffix,'p3GaussBern3_'+suffix,p3)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
  GaussBern3 = RooGaussStepBernstein('GaussBern3_'+suffix,'GaussBern3_'+suffix,mzg,meanVar,sigmaVar,stepVar,pArgs)

  returnArgs = [meanVar,sigmaVar,stepVar,p0Var,p1Var,p2Var,p3Var]
  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  return GaussBern3,returnArgs

def BuildGaussStepBern4(tev,lepton,cat,mzg,mean = 0, sigma = 4, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
    p0 = 15, p1 = 0.4, p1Low = -1e-6, p1High = 900,p2 = 0.4, p2Low = -1e-6, p2High = 900,p3 = 0.4, p3Low = -1e-6, p3High = 900, p4 = 0.4, p4Low = -1e-6, p4High = 900):
  #def BuildGaussStepBern4(tev,lepton,cat,mzg,mean = 0, sigma = 4, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
    #p0 = 15, p1 = 0.4, p1Low = -1e2, p1High = 900,p2 = 0.4, p2Low = -1e2, p2High = 900,p3 = 0.4, p3Low = -1e2, p3High = 900, p4 = 0.4, p4Low = -1e2, p4High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussBern4_'+suffix,'meanGaussBern4_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussBern4_'+suffix,'sigmaGaussBern4_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepGaussBern4_'+suffix,'stepGaussBern4_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0GaussBern4_'+suffix,'p0GaussBern4_'+suffix, p0)
  p1Var = RooRealVar('p1GaussBern4_'+suffix,'p1GaussBern4_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2GaussBern4_'+suffix,'p2GaussBern4_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3GaussBern4_'+suffix,'p3GaussBern4_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4GaussBern4_'+suffix,'p4GaussBern4_'+suffix,p4,p4Low,p4High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var)
  GaussBern4 = RooGaussStepBernstein('GaussBern4_'+suffix,'GaussBern4_'+suffix,mzg,meanVar,sigmaVar,stepVar,pArgs)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  return GaussBern4

def BuildGaussStepBern5(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
    p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900, p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900):
  #def BuildGaussStepBern5(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
   # p0 = 15, p1 = 0.5, p1Low = -1e2, p1High = 900,p2 = 0.5, p2Low = -1e2, p2High = 900,p3 = 0.5, p3Low = -1e2, p3High = 900, p4 = 0.5, p4Low = -1e2, p4High = 900, p5 = 0.5, p5Low = -1e2, p5High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussBern5_'+suffix,'meanGaussBern5_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussBern5_'+suffix,'sigmaGaussBern5_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepGaussBern5_'+suffix,'stepGaussBern5_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0GaussBern5_'+suffix,'p0GaussBern5_'+suffix, p0)
  p1Var = RooRealVar('p1GaussBern5_'+suffix,'p1GaussBern5_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2GaussBern5_'+suffix,'p2GaussBern5_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3GaussBern5_'+suffix,'p3GaussBern5_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4GaussBern5_'+suffix,'p4GaussBern5_'+suffix,p4,p4Low,p4High)
  p5Var = RooRealVar('p5GaussBern5_'+suffix,'p5GaussBern5_'+suffix,p5,p5Low,p5High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var)
  GaussBern5 = RooGaussStepBernstein('GaussBern5_'+suffix,'GaussBern5_'+suffix,mzg,meanVar,sigmaVar,stepVar,pArgs)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  SetOwnership(p5Var,0)
  return GaussBern5

#def BuildGaussStepBern6(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
#    p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900,
#    p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900, p6 = 0.5, p6Low = -1e-6, p6High = 900):
def BuildGaussStepBern6(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
    p0 = 15, p1 = 0.5, p1Low = -1e2, p1High = 900,p2 = 0.5, p2Low = -1e2, p2High = 900,p3 = 0.5, p3Low = -1e2, p3High = 900,
    p4 = 0.5, p4Low = -1e2, p4High = 900, p5 = 0.5, p5Low = -1e2, p5High = 900, p6 = 0.5, p6Low = -1e2, p6High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanGaussBern6_'+suffix,'meanGaussBern6_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaGaussBern6_'+suffix,'sigmaGaussBern6_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepGaussBern6_'+suffix,'stepGaussBern6_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0GaussBern6_'+suffix,'p0GaussBern6_'+suffix, p0)
  p1Var = RooRealVar('p1GaussBern6_'+suffix,'p1GaussBern6_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2GaussBern6_'+suffix,'p2GaussBern6_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3GaussBern6_'+suffix,'p3GaussBern6_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4GaussBern6_'+suffix,'p4GaussBern6_'+suffix,p4,p4Low,p4High)
  p5Var = RooRealVar('p5GaussBern6_'+suffix,'p5GaussBern6_'+suffix,p5,p5Low,p5High)
  p6Var = RooRealVar('p6GaussBern6_'+suffix,'p6GaussBern6_'+suffix,p6,p6Low,p6High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var,p6Var)
  GaussBern6 = RooGaussStepBernstein('GaussBern6_'+suffix,'GaussBern6_'+suffix,mzg,meanVar,sigmaVar,stepVar,pArgs)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  SetOwnership(p5Var,0)
  SetOwnership(p6Var,0)
  return GaussBern6

def BuildSechStepBern3(tev,lepton,cat,mzg,mean = 0, sigma = 3, sigmaLow = 0.01, sigmaHigh = 20, step = 0.1, stepLow = 0, stepHigh = 10,
    p0 = 15, p1 = 0.3, p1Low = -1e-6, p1High = 900,p2 = 0.3, p2Low = -1e-6, p2High = 900,p3 = 0.3, p3Low = -1e-6, p3High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanSechBern3_'+suffix,'meanSechBern3_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaSechBern3_'+suffix,'sigmaSechBern3_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepSechBern3_'+suffix,'stepSechBern3_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0SechBern3_'+suffix,'p0SechBern3_'+suffix, p0)
  p1Var = RooRealVar('p1SechBern3_'+suffix,'p1SechBern3_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2SechBern3_'+suffix,'p2SechBern3_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3SechBern3_'+suffix,'p3SechBern3_'+suffix,p3,p3Low,p3High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
  turnOn = RooGenericPdf('turnOnSechBern3_'+suffix,'turnOnSechBern3_'+suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(mzg,meanVar,sigmaVar))
  tail = RooStepBernstein('tailSechBern3_'+suffix,'tailSechBern3_'+suffix,mzg,stepVar,pArgs)
  SechBern3 = RooFFTConvPdf('SechBern3_'+suffix,'SechBern3_'+suffix,mzg,tail,turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return SechBern3

def BuildSechStepBern4(tev,lepton,cat,mzg,mean = 0, sigma = 3, sigmaLow = 0.01, sigmaHigh = 20, step = 0.1, stepLow = 0, stepHigh = 10,
    p0 = 15, p1 = 0.4, p1Low = -1e-6, p1High = 900,p2 = 0.4, p2Low = -1e-6, p2High = 900,p3 = 0.4, p3Low = -1e-6, p3High = 900, p4 = 0.4, p4Low = -1e-6, p4High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanSechBern4_'+suffix,'meanSechBern4_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaSechBern4_'+suffix,'sigmaSechBern4_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepSechBern4_'+suffix,'stepSechBern4_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0SechBern4_'+suffix,'p0SechBern4_'+suffix, p0)
  p1Var = RooRealVar('p1SechBern4_'+suffix,'p1SechBern4_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2SechBern4_'+suffix,'p2SechBern4_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3SechBern4_'+suffix,'p3SechBern4_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4SechBern4_'+suffix,'p4SechBern4_'+suffix,p4,p4Low,p4High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var)
  turnOn = RooGenericPdf('turnOnSechBern4_'+suffix,'turnOnSechBern4_'+suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(mzg,meanVar,sigmaVar))
  tail = RooStepBernstein('tailSechBern4_'+suffix,'tailSechBern4_'+suffix,mzg,stepVar,pArgs)
  SechBern4 = RooFFTConvPdf('SechBern4_'+suffix,'SechBern4_'+suffix,mzg,tail,turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return SechBern4

def BuildSechStepBern5(tev,lepton,cat,mzg,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 0.1, stepLow = 0, stepHigh = 10,
    p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900, p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('meanSechBern5_'+suffix,'meanSechBern5_'+suffix, mean)
  sigmaVar = RooRealVar('sigmaSechBern5_'+suffix,'sigmaSechBern5_'+suffix,sigma,sigmaLow,sigmaHigh)
  stepVar = RooRealVar('stepSechBern5_'+suffix,'stepSechBern5_'+suffix,step,stepLow,stepHigh)
  p0Var = RooRealVar('p0SechBern5_'+suffix,'p0SechBern5_'+suffix, p0)
  p1Var = RooRealVar('p1SechBern5_'+suffix,'p1SechBern5_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2SechBern5_'+suffix,'p2SechBern5_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3SechBern5_'+suffix,'p3SechBern5_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4SechBern5_'+suffix,'p4SechBern5_'+suffix,p4,p4Low,p4High)
  p5Var = RooRealVar('p5SechBern5_'+suffix,'p5SechBern5_'+suffix,p5,p5Low,p5High)

  pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var)
  turnOn = RooGenericPdf('turnOnSechBern5_'+suffix,'turnOnSechBern5_'+suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(mzg,meanVar,sigmaVar))
  tail = RooStepBernstein('tailSechBern5_'+suffix,'tailSechBern5_'+suffix,mzg,stepVar,pArgs)
  SechBern5 = RooFFTConvPdf('SechBern5_'+suffix,'SechBern5_'+suffix,mzg,tail,turnOn)

  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  SetOwnership(stepVar,0)
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  SetOwnership(p5Var,0)
  SetOwnership(turnOn,0)
  SetOwnership(tail,0)
  return SechBern5

def BuildExp(tev,lepton,cat,mzg,tau = 1, tauLow = -50, tauHigh = 50):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  tauVar = RooRealVar('tauExp_'+suffix,'tauExp_'+suffix,tau,tauLow,tauHigh)
  Exp = RooExponential('Exp_'+suffix,'Exp_'+suffix,mzg,tauVar)
  SetOwnership(tauVar,0)
  return Exp

def BuildPow(tev,lepton,cat,mzg,alpha = 115, alphaLow = 50, alphaHigh = 200, beta = 3, betaLow = -20, betaHigh = 20):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  alphaVar = RooRealVar('alphaPow_'+suffix,'alphaPow_'+suffix,alpha,alphaLow,alphaHigh)
  betaVar = RooRealVar('betaPow_'+suffix,'betaPow_'+suffix,beta,betaLow,betaHigh)
  Pow = RooGenericPdf('Pow_'+suffix,'Pow_'+suffix,'1e-20 + (@1)*((@0)^(-@2))',RooArgList(mzg,alphaVar,betaVar))
  SetOwnership(alphaVar,0)
  SetOwnership(betaVar,0)
  return Pow

def BuildPowDecay(tev,lepton,cat,mzg,p1 = 1, p1Low = -20, p1High = 20, p2 = 1, p2Low = -20, p2High = 20):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p1Var = RooRealVar('p1PowDecay_'+suffix,'p1PowDecay_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2PowDecay_'+suffix,'p2PowDecay_'+suffix,p2,p2Low,p2High)
  PowDecay = RooGenericPdf('PowDecay_'+suffix,'PowDecay_'+suffix,'exp(-@1)*((@0)^(-@2))',RooArgList(mzg,p1Var,p2Var))
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  return PowDecay

def BuildBern2(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30):
#def BuildBern2(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p0Var = RooRealVar('p0Bern2_'+suffix, 'p0Bern2_'+suffix,p0)
  p1Var = RooRealVar('p1Bern2_'+suffix, 'p1Bern2_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2Bern2_'+suffix, 'p2Bern2_'+suffix,p2,p2Low,p2High)
  Bern2 = RooBernstein('Bern2_'+suffix,'Bern2_'+suffix,mzg,RooArgList(p0Var,p1Var,p2Var))
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  return Bern2

def BuildBern3(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30):
#def BuildBern3(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p0Var = RooRealVar('p0Bern3_'+suffix, 'p0Bern3_'+suffix,p0)
  #p1Var = RooRealVar('p1Bern3_'+suffix, 'p1Bern3_'+suffix,p1,p1Low,p1High)
  #p2Var = RooRealVar('p2Bern3_'+suffix, 'p2Bern3_'+suffix,p2,p2Low,p2High)
  #p3Var = RooRealVar('p3Bern3_'+suffix, 'p3Bern3_'+suffix,p3,p3Low,p3High)
  p1Var = RooRealVar('p1Bern3_'+suffix, 'p1Bern3_'+suffix,p1)
  p2Var = RooRealVar('p2Bern3_'+suffix, 'p2Bern3_'+suffix,p2)
  p3Var = RooRealVar('p3Bern3_'+suffix, 'p3Bern3_'+suffix,p3)
  Bern3 = RooBernstein('Bern3_'+suffix,'Bern3_'+suffix,mzg,RooArgList(p0Var,p1Var,p2Var, p3Var))
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  return Bern3

def BuildPoly3(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low = -3000, p1High = 3000, p2 = 5, p2Low = -3000, p2High = 3000, p3 = 5, p3Low = -3000, p3High = 3000):
#def BuildPoly3(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p0Var = RooRealVar('p0Poly3_'+suffix, 'p0Poly3_'+suffix,p0)
  p1Var = RooRealVar('p1Poly3_'+suffix, 'p1Poly3_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2Poly3_'+suffix, 'p2Poly3_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3Poly3_'+suffix, 'p3Poly3_'+suffix,p3,p3Low,p3High)
  Poly3 = RooPolynomial('Poly3_'+suffix,'Poly3_'+suffix,mzg,RooArgList(p0Var,p1Var,p2Var, p3Var))
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  return Poly3

def BuildBern4(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30, p4 = 5, p4Low = -1e-6, p4High = 30):
#def BuildBern4(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30, p4 = 5, p4Low =1e-3, p4High = 30):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p0Var = RooRealVar('p0Bern4_'+suffix, 'p0Bern4_'+suffix,p0)
  p1Var = RooRealVar('p1Bern4_'+suffix, 'p1Bern4_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2Bern4_'+suffix, 'p2Bern4_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3Bern4_'+suffix, 'p3Bern4_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4Bern4_'+suffix, 'p4Bern4_'+suffix,p4,p4Low,p4High)
  Bern4 = RooBernstein('Bern4_'+suffix,'Bern4_'+suffix,mzg,RooArgList(p0Var,p1Var,p2Var, p3Var, p4Var))
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  return Bern4

def BuildBern5(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30, p4 = 5, p4Low = -1e-6, p4High = 30, p5 = 5, p5Low = -1e-6, p5High = 30):
#def BuildBern5(tev,lepton,cat,mzg,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30, p4 = 5, p4Low =1e-3, p4High = 30, p5 = 5, p5Low =1e-3, p5High = 30):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  p0Var = RooRealVar('p0Bern5_'+suffix, 'p0Bern5_'+suffix,p0)
  p1Var = RooRealVar('p1Bern5_'+suffix, 'p1Bern5_'+suffix,p1,p1Low,p1High)
  p2Var = RooRealVar('p2Bern5_'+suffix, 'p2Bern5_'+suffix,p2,p2Low,p2High)
  p3Var = RooRealVar('p3Bern5_'+suffix, 'p3Bern5_'+suffix,p3,p3Low,p3High)
  p4Var = RooRealVar('p4Bern5_'+suffix, 'p4Bern5_'+suffix,p4,p4Low,p4High)
  p5Var = RooRealVar('p5Bern5_'+suffix, 'p5Bern5_'+suffix,p5,p5Low,p5High)
  Bern5 = RooBernstein('Bern5_'+suffix,'Bern5_'+suffix,mzg,RooArgList(p0Var,p1Var,p2Var, p3Var, p4Var, p5Var))
  SetOwnership(p0Var,0)
  SetOwnership(p1Var,0)
  SetOwnership(p2Var,0)
  SetOwnership(p3Var,0)
  SetOwnership(p4Var,0)
  SetOwnership(p5Var,0)
  return Bern5

def BuildRooGaussian(tev,lepton,cat,mzg, mean = 125,meanLow = 100, meanHigh = 150, sigma = 1.5, sigmaLow = 0.3, sigmaHigh = 70):
  suffix = '_'.join([tev,lepton,'cat'+cat])
  meanVar = RooRealVar('mean_'+suffix,'mean_'+suffix, mean, meanLow, meanHigh)
  sigmaVar = RooRealVar('sigma_'+suffix,'sigma_'+suffix,sigma,sigmaLow,sigmaHigh)
  gauss = RooGaussian('gauss_'+suffix,'gauss_'+suffix,mzg,meanVar,sigmaVar)
  SetOwnership(meanVar,0)
  SetOwnership(sigmaVar,0)
  return gauss

def BuildCrystalBallGauss(tev,lepton,cat,sig,mass,piece,mzg, meanG = 125, meanGLow = -1, meanGHigh = -1, meanCB = 125, meanCBLow = -1, meanCBHigh = -1,sigmaCB = 1.5, sigmaCBLow = 0.3, sigmaCBHigh = 20, alpha = 1, alphaLow = 0.5, alphaHigh = 10,
    n = 4, nLow = 0.5, nHigh = 50, sigmaG = 2, sigmaGLow = 0.3, sigmaGHigh = 20, frac = 0.1, fracLow = 0.0, fracHigh = 1.0):
  suffix = '_'.join([tev,lepton,'cat'+cat,sig,mass,piece])
  if meanGLow is -1: meanGLow = meanG-5
  if meanGHigh is -1: meanGHigh = meanG+5
  if meanCBLow is -1: meanCBLow = meanCB-5
  if meanCBHigh is -1: meanCBHigh = meanCB+5
  meanGVar = RooRealVar('meanGCBG_'+suffix,'meanGCBG_'+suffix, meanG, meanGLow, meanGHigh)
  meanCBVar = RooRealVar('meanCBCBG_'+suffix,'meanCBCBG_'+suffix, meanCB, meanCBLow, meanCBHigh)
  sigmaCBVar = RooRealVar('sigmaCBCBG_'+suffix,'sigmaCBCBG_'+suffix,sigmaCB,sigmaCBLow,sigmaCBHigh)
  alphaVar = RooRealVar('alphaCBG_'+suffix,'alphaCBG_'+suffix,alpha,alphaLow,alphaHigh)
  nVar = RooRealVar('nCBG_'+suffix,'nCBG_'+suffix,n,nLow,nHigh)
  sigmaGVar = RooRealVar('sigmaGCBG_'+suffix,'sigmaGCBG_'+suffix,sigmaG,sigmaGLow,sigmaGHigh)
  fracVar = RooRealVar('fracCBG_'+suffix,'fracCBG_'+suffix,frac,fracLow,fracHigh)

  crystal = RooCBShape('crystalCBG_'+suffix,'crystalCBG_'+suffix,mzg,meanCBVar,sigmaCBVar,alphaVar,nVar)
  gauss = RooGaussian('gaussCBG_'+suffix,'gaussCBG_'+suffix,mzg,meanGVar,sigmaGVar)
  cbArgs = RooArgList(gauss,crystal)
  fracArg = RooArgList(fracVar)
  CBG = RooAddPdf('CBG_'+suffix,'CBG_'+suffix,cbArgs,fracArg,True)

  SetOwnership(meanGVar,0)
  SetOwnership(meanCBVar,0)
  SetOwnership(sigmaCBVar,0)
  SetOwnership(alphaVar,0)
  SetOwnership(nVar,0)
  SetOwnership(sigmaGVar,0)
  SetOwnership(fracVar,0)
  SetOwnership(crystal,0)
  SetOwnership(gauss,0)
  paramList = [meanGVar,meanCBVar,sigmaCBVar,alphaVar,nVar,sigmaGVar,fracVar]
  return CBG, paramList
  return CBG

def BuildTripleGauss(tev,lepton,cat,sig,mass,piece,mzg, meanG1 = 125, meanG1Low = -1, meanG1High = -1, meanG2 = 125, meanG2Low = -1, meanG2High = -1, meanG3 = 125, meanG3Low = -1, meanG3High = -1,
    sigmaG1 = 1.5, sigmaG1Low = 0.3, sigmaG1High = 20, sigmaG2 = 1.5, sigmaG2Low = 0.3, sigmaG2High = 20, sigmaG3 = 1.5, sigmaG3Low = 0.3, sigmaG3High = 20,
    frac1 = 0.1, frac1Low = 0.0, frac1High = 1.0, frac2 = 0.1, frac2Low = 0.0, frac2High = 1.0):
  suffix = '_'.join([tev,lepton,'cat'+cat,sig,mass,piece])
  if meanG1Low is -1: meanG1Low = meanG1-5
  if meanG1High is -1: meanG1High = meanG1+5
  if meanG2Low is -1: meanG2Low = meanG2-5
  if meanG2High is -1: meanG2High = meanG2+5
  if meanG3Low is -1: meanG3Low = meanG3-5
  if meanG3High is -1: meanG3High = meanG3+5

  meanG1Var = RooRealVar('meanG1TripG_'+suffix,'meanG1TripG_'+suffix, meanG1, meanG1Low, meanG1High)
  meanG2Var = RooRealVar('meanG2TripG_'+suffix,'meanG2TripG_'+suffix, meanG2, meanG2Low, meanG2High)
  meanG3Var = RooRealVar('meanG3TripG_'+suffix,'meanG3TripG_'+suffix, meanG3, meanG3Low, meanG3High)
  sigmaG1Var = RooRealVar('sigmaG1TripG_'+suffix,'sigmaG1TripG_'+suffix,sigmaG1,sigmaG1Low,sigmaG1High)
  sigmaG2Var = RooRealVar('sigmaG2TripG_'+suffix,'sigmaG2TripG_'+suffix,sigmaG2,sigmaG2Low,sigmaG2High)
  sigmaG3Var = RooRealVar('sigmaG3TripG_'+suffix,'sigmaG3TripG_'+suffix,sigmaG3,sigmaG3Low,sigmaG3High)
  frac1Var = RooRealVar('frac1TripG_'+suffix,'frac1TripG_'+suffix,frac1,frac1Low,frac1High)
  frac2Var = RooRealVar('frac2TripG_'+suffix,'frac2TripG_'+suffix,frac2,frac2Low,frac2High)

  gauss1 = RooGaussian('gauss1TripG_'+suffix,'gauss1TripG_'+suffix,mzg,meanG1Var,sigmaG1Var)
  gauss2 = RooGaussian('gauss2TripG_'+suffix,'gauss2TripG_'+suffix,mzg,meanG2Var,sigmaG2Var)
  gauss3 = RooGaussian('gauss3TripG_'+suffix,'gauss3TripG_'+suffix,mzg,meanG3Var,sigmaG3Var)
  gaussArgs = RooArgList(gauss1,gauss2,gauss3)
  fracArgs = RooArgList(frac1Var, frac2Var)
  TripG = RooAddPdf('TripG_'+suffix,'TripG_'+suffix,gaussArgs,fracArgs,True)

  SetOwnership(meanG1Var,0)
  SetOwnership(sigmaG1Var,0)
  SetOwnership(meanG2Var,0)
  SetOwnership(sigmaG2Var,0)
  SetOwnership(meanG3Var,0)
  SetOwnership(sigmaG3Var,0)
  SetOwnership(frac1Var,0)
  SetOwnership(frac2Var,0)
  SetOwnership(gauss1,0)
  SetOwnership(gauss2,0)
  SetOwnership(gauss3,0)
  paramList = [meanG1Var, meanG2Var, meanG3Var, sigmaG1Var, sigmaG2Var, sigmaG3Var, frac1Var, frac2Var]
  return TripG, paramList
  return TripG

def BuildTripleGaussV2(tev,lepton,cat,sig,mass,piece,mzg, mean1 = 125, mean1Low = -1, mean1High = -1, sigma1 = 2, sigma1Low = 1, sigma1High = 8,
    delta21 = 0, delta21Low = -2, delta21High = 2, s21 = 3, s21Low = 1, s21High = 30, delta31 = 0, delta31Low = -2, delta31High = 2,
    s32 = 3, s32Low = 1, s32High = 30, frac23 = 0.9, frac23Low = 0, frac23High = 1, frac123 = 0.9, frac123Low = 0, frac123High = 1):

  suffix = '_'.join([tev,lepton,'cat'+cat,sig,mass,piece])
  if mean1Low is -1: mean1Low = mean1-1
  if mean1High is -1: mean1High = mean1+1

  mean1Var = RooRealVar('mean1TripG_'+suffix,'mean1TripG_'+suffix, mean1, mean1Low, mean1High)
  sigma1Var = RooRealVar('sigma1TripG_'+suffix,'sigma1TripG_'+suffix, sigma1, sigma1Low, sigma1High)
  delta21Var = RooRealVar('delta21TripG_'+suffix,'delta21TripG_'+suffix, delta21, delta21Low, delta21High)
  s21Var = RooRealVar('s21TripG_'+suffix,'s21TripG_'+suffix,s21,s21Low,s21High)
  delta31Var = RooRealVar('delta31TripG_'+suffix,'delta31TripG_'+suffix,delta31,delta31Low,delta31High)
  s32Var = RooRealVar('s32TripG_'+suffix,'s32TripG_'+suffix,s32,s32Low,s32High)
  frac23Var = RooRealVar('frac23TripG_'+suffix,'frac23TripG_'+suffix,frac23,frac23Low,frac23High)
  frac123Var = RooRealVar('frac123TripG_'+suffix,'frac123TripG_'+suffix,frac123,frac123Low,frac123High)

  mean2Var = RooFormulaVar('mean2TripG_'+suffix,'@0 + @1', RooArgList(mean1Var, delta21Var))
  sigma2Var = RooFormulaVar('sigma2TripG_'+suffix,'@0 * @1', RooArgList(sigma1Var, s21Var))
  mean3Var = RooFormulaVar('mean3TripG_'+suffix,'@0 + @1', RooArgList(mean1Var, delta31Var))
  sigma3Var = RooFormulaVar('sigma3TripG_'+suffix,'@0 * @1', RooArgList(sigma2Var, s32Var))

  gauss1 = RooGaussian('gauss1TripG_'+suffix,'gauss1TripG_'+suffix,mzg,mean1Var,sigma1Var)
  gauss2 = RooGaussian('gauss2TripG_'+suffix,'gauss2TripG_'+suffix,mzg,mean2Var,sigma2Var)
  gauss3 = RooGaussian('gauss3TripG_'+suffix,'gauss3TripG_'+suffix,mzg,mean3Var,sigma3Var)
  #gaussArgs = RooArgList(gauss1,gauss2,gauss3)
  #fracArgs = RooArgList(frac1Var, frac2Var)
  pdf23 = RooAddPdf('pdf23TripG_'+suffix,'pdf12TripG_'+suffix, gauss2, gauss3, frac23Var)
  TripG = RooAddPdf('TripG_'+suffix,'TripG_'+suffix, gauss1, pdf23, frac123Var)

  SetOwnership(mean1Var,0)
  SetOwnership(sigma1Var,0)
  SetOwnership(mean2Var,0)
  SetOwnership(sigma2Var,0)
  SetOwnership(mean3Var,0)
  SetOwnership(sigma3Var,0)
  SetOwnership(frac23Var,0)
  SetOwnership(frac123Var,0)
  SetOwnership(gauss1,0)
  SetOwnership(gauss2,0)
  SetOwnership(gauss3,0)
  SetOwnership(pdf23,0)
  SetOwnership(delta21Var,0)
  SetOwnership(delta31Var,0)
  SetOwnership(s21Var,0)
  SetOwnership(s32Var,0)
  paramList = [mean1Var, sigma1Var, frac23Var, frac123Var, delta21Var, s21Var, s32Var, delta31Var]
  return TripG, paramList
  return TripG

def SignalNameParamFixerCBG(tev,lepton,cat,sig,mass,ws):
  fitName = '_'.join(['CBG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  newFitName = '_'.join([sig,'hzg',lepton,'cat'+cat,tev])
  meanG = '_'.join(['meanGCBG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  meanCB = '_'.join(['meanCBCBG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigmaCB = '_'.join(['sigmaCBCBG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigmaG = '_'.join(['sigmaGCBG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  meanGNew = '_'.join(['sig',sig,'meanG',lepton,tev,'cat'+cat])
  meanCBNew = '_'.join(['sig',sig,'meanCB',lepton,tev,'cat'+cat])
  sigmaCBNew = '_'.join(['sig',sig,'sigmaCB',lepton,tev,'cat'+cat])
  sigmaGNew = '_'.join(['sig',sig,'sigmaG',lepton,tev,'cat'+cat])
  mShift = '_'.join(['sig',sig,'mShift',lepton,tev,'cat'+cat])
  sigmaShift = '_'.join(['sig',sig,'sigmaShift',lepton,tev,'cat'+cat])
  ws.factory(mShift+'[1]')
  ws.factory(sigmaShift+'[1]')
  ws.factory('prod::'+meanGNew+'('+meanG+','+mShift+')')
  ws.factory('prod::'+meanCBNew+'('+meanCB+','+mShift+')')
  ws.factory('prod::'+sigmaCBNew+'('+sigmaCB+','+sigmaShift+')')
  ws.factory('prod::'+sigmaGNew+'('+sigmaG+','+sigmaShift+')')
  ws.factory('EDIT::'+newFitName+'('+fitName+','+meanG+'='+meanGNew+','+meanCB+'='+meanCBNew+','+sigmaCB+'='+sigmaCBNew+','+sigmaG+'='+sigmaGNew+')')

def SignalNameParamFixerTripG(tev,lepton,cat,sig,mass,ws):
  fitName = '_'.join(['TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  newFitName = '_'.join([sig,'hzg',lepton,'cat'+cat,tev])

  meanG1 = '_'.join(['meanG1TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigmaG1 = '_'.join(['sigmaG1TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  meanG1New = '_'.join(['sig',sig,'meanG1',lepton,tev,'cat'+cat])
  sigmaG1New = '_'.join(['sig',sig,'sigmaG1',lepton,tev,'cat'+cat])

  meanG2 = '_'.join(['meanG2TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigmaG2 = '_'.join(['sigmaG2TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  meanG2New = '_'.join(['sig',sig,'meanG2',lepton,tev,'cat'+cat])
  sigmaG2New = '_'.join(['sig',sig,'sigmaG2',lepton,tev,'cat'+cat])

  meanG3 = '_'.join(['meanG3TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigmaG3 = '_'.join(['sigmaG3TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  meanG3New = '_'.join(['sig',sig,'meanG3',lepton,tev,'cat'+cat])
  sigmaG3New = '_'.join(['sig',sig,'sigmaG3',lepton,tev,'cat'+cat])

  mShift = '_'.join(['sig',sig,'mShift',lepton,tev,'cat'+cat])
  sigmaShift = '_'.join(['sig',sig,'sigmaShift',lepton,tev,'cat'+cat])

  ws.factory(mShift+'[1]')
  ws.factory(sigmaShift+'[1]')
  ws.factory('prod::'+meanG1New+'('+meanG1+','+mShift+')')
  ws.factory('prod::'+sigmaG1New+'('+sigmaG1+','+sigmaShift+')')
  ws.factory('prod::'+meanG2New+'('+meanG2+','+mShift+')')
  ws.factory('prod::'+sigmaG2New+'('+sigmaG2+','+sigmaShift+')')
  ws.factory('prod::'+meanG3New+'('+meanG3+','+mShift+')')
  ws.factory('prod::'+sigmaG3New+'('+sigmaG3+','+sigmaShift+')')
  ws.factory('EDIT::'+newFitName+'('+fitName+','+meanG1+'='+meanG1New+','+meanG2+'='+meanG2New+','+meanG3+'='+meanG3New+','+
      sigmaG1+'='+sigmaG1New+','+sigmaG2+'='+sigmaG2New+','+sigmaG3+'='+sigmaG3New+')')

def SignalNameParamFixerTripGV2(tev,lepton,cat,sig,mass,ws):
  fitName = '_'.join(['TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  newFitName = '_'.join([sig,'hzg',lepton,'cat'+cat,tev])

  mean1 = '_'.join(['mean1TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  mean2 = '_'.join(['mean2TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  mean3 = '_'.join(['mean3TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigma1 = '_'.join(['sigma1TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigma2 = '_'.join(['sigma2TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  sigma3 = '_'.join(['sigma3TripG',tev,lepton,'cat'+cat,sig,mass,'Interp'])
  mean1New = '_'.join(['sig',sig,'mean1',lepton,tev,'cat'+cat])
  mean2New = '_'.join(['sig',sig,'mean2',lepton,tev,'cat'+cat])
  mean3New = '_'.join(['sig',sig,'mean3',lepton,tev,'cat'+cat])
  sigma1New = '_'.join(['sig',sig,'sigma1',lepton,tev,'cat'+cat])
  sigma2New = '_'.join(['sig',sig,'sigma2',lepton,tev,'cat'+cat])
  sigma3New = '_'.join(['sig',sig,'sigma3',lepton,tev,'cat'+cat])

  mShift = '_'.join(['sig',sig,'mShift',lepton,tev,'cat'+cat])
  sigmaShift = '_'.join(['sig',sig,'sigmaShift',lepton,tev,'cat'+cat])

  ws.factory(mShift+'[1]')
  ws.factory(sigmaShift+'[1]')
  ws.factory('prod::'+mean1New+'('+mean1+','+mShift+')')
  ws.factory('prod::'+mean2New+'('+mean2+','+mShift+')')
  ws.factory('prod::'+mean3New+'('+mean3+','+mShift+')')
  ws.factory('prod::'+sigma1New+'('+sigma1+','+sigmaShift+')')
  ws.factory('prod::'+sigma2New+'('+sigma2+','+sigmaShift+')')
  ws.factory('prod::'+sigma3New+'('+sigma3+','+sigmaShift+')')
  ws.factory('EDIT::'+newFitName+'('+fitName+','+mean1+'='+mean1New+','+mean2+'='+mean2New+','+mean3+'='+mean3New+','
      +sigma1+'='+sigma1New+','+sigma2+'='+sigma2New+','+sigma3+'='+sigma3New+')')

def BackgroundNameFixer(tev,lepton,cat,ws,newCat = None,Ext = True):
  if newCat == None: newCat = cat
  dataName = '_'.join(['data',lepton,tev,'cat'+cat])
  dataNameNew = '_'.join(['data','obs',lepton,tev,'cat'+newCat])
  if Ext:
    fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
  else:
    if cat is '1' and (lepton is 'el' or (lepton is 'mu' and tev is '7TeV')):
      fitExtName = '_'.join(['GaussBern4',tev,lepton,'cat'+cat])
    elif cat is '0':
      fitExtName = '_'.join(['GaussBern6',tev,lepton,'cat'+cat])
    elif cat is '5':
      fitExtName = '_'.join(['Bern3',tev,lepton,'cat'+cat])
    else:
      fitExtName = '_'.join(['GaussBern5',tev,lepton,'cat'+cat])
  fitExtNameNew = '_'.join(['bkg',lepton,tev,'cat'+newCat])

  if cat is '1' and (lepton is 'el' or (lepton is 'mu' and tev is '7TeV')):
    suffix = '_'.join([tev,lepton,'cat'+cat])
    if Ext: normName = 'normGaussBern4_'+suffix
    meanName = 'meanGaussBern4_'+suffix
    sigmaName = 'sigmaGaussBern4_'+suffix
    stepName = 'stepGaussBern4_'+suffix
    p0Name = 'p0GaussBern4_'+suffix
    p1Name = 'p1GaussBern4_'+suffix
    p2Name = 'p2GaussBern4_'+suffix
    p3Name = 'p3GaussBern4_'+suffix
    p4Name = 'p4GaussBern4_'+suffix

    if Ext: normNameNew  = '_'.join(['bkg',lepton,tev,'cat'+newCat,'norm'])
    meanNameNew  = '_'.join(['bkg','mean',lepton,tev,'cat'+newCat])
    sigmaNameNew  = '_'.join(['bkg','sigma',lepton,tev,'cat'+newCat])
    stepNameNew  = '_'.join(['bkg','step',lepton,tev,'cat'+newCat])
    p0NameNew  = '_'.join(['bkg','p0',lepton,tev,'cat'+newCat])
    p1NameNew  = '_'.join(['bkg','p1',lepton,tev,'cat'+newCat])
    p2NameNew  = '_'.join(['bkg','p2',lepton,tev,'cat'+newCat])
    p3NameNew  = '_'.join(['bkg','p3',lepton,tev,'cat'+newCat])
    p4NameNew  = '_'.join(['bkg','p4',lepton,tev,'cat'+newCat])

    if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
    ws.factory(meanNameNew+'[{0}]'.format(ws.function(meanName).getVal()))
    ws.factory(sigmaNameNew+'[{0},{1},{2}]'.format(ws.function(sigmaName).getVal(),ws.function(sigmaName).getMin(),ws.function(sigmaName).getMax()))
    ws.factory(stepNameNew+'[{0},{1},{2}]'.format(ws.function(stepName).getVal(),ws.function(stepName).getMin(),ws.function(stepName).getMax()))
    ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
    ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(),ws.function(p1Name).getMax()))
    ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(),ws.function(p2Name).getMax()))
    ws.factory(p3NameNew+'[{0},{1},{2}]'.format(ws.function(p3Name).getVal(),ws.function(p3Name).getMin(),ws.function(p3Name).getMax()))
    ws.factory(p4NameNew+'[{0},{1},{2}]'.format(ws.function(p4Name).getVal(),ws.function(p4Name).getMin(),ws.function(p4Name).getMax()))
    if Ext:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','+normName+'='+normNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+')')
    else:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+')')

  elif cat is '0':
    suffix = '_'.join([tev,lepton,'cat'+cat])
    if Ext: normName = 'normGaussBern6_'+suffix
    meanName = 'meanGaussBern6_'+suffix
    sigmaName = 'sigmaGaussBern6_'+suffix
    stepName = 'stepGaussBern6_'+suffix
    p0Name = 'p0GaussBern6_'+suffix
    p1Name = 'p1GaussBern6_'+suffix
    p2Name = 'p2GaussBern6_'+suffix
    p3Name = 'p3GaussBern6_'+suffix
    p4Name = 'p4GaussBern6_'+suffix
    p5Name = 'p5GaussBern6_'+suffix
    p6Name = 'p6GaussBern6_'+suffix

    if Ext: normNameNew  = '_'.join(['bkg',lepton,tev,'cat'+newCat,'norm'])
    meanNameNew  = '_'.join(['bkg','mean',lepton,tev,'cat'+newCat])
    sigmaNameNew  = '_'.join(['bkg','sigma',lepton,tev,'cat'+newCat])
    stepNameNew  = '_'.join(['bkg','step',lepton,tev,'cat'+newCat])
    p0NameNew  = '_'.join(['bkg','p0',lepton,tev,'cat'+newCat])
    p1NameNew  = '_'.join(['bkg','p1',lepton,tev,'cat'+newCat])
    p2NameNew  = '_'.join(['bkg','p2',lepton,tev,'cat'+newCat])
    p3NameNew  = '_'.join(['bkg','p3',lepton,tev,'cat'+newCat])
    p4NameNew  = '_'.join(['bkg','p4',lepton,tev,'cat'+newCat])
    p5NameNew  = '_'.join(['bkg','p5',lepton,tev,'cat'+newCat])
    p6NameNew  = '_'.join(['bkg','p6',lepton,tev,'cat'+newCat])

    if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
    ws.factory(meanNameNew+'[{0}]'.format(ws.function(meanName).getVal()))
    ws.factory(sigmaNameNew+'[{0},{1},{2}]'.format(ws.function(sigmaName).getVal(),ws.function(sigmaName).getMin(),ws.function(sigmaName).getMax()))
    ws.factory(stepNameNew+'[{0},{1},{2}]'.format(ws.function(stepName).getVal(),ws.function(stepName).getMin(),ws.function(stepName).getMax()))
    ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
    ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(),ws.function(p1Name).getMax()))
    ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(),ws.function(p2Name).getMax()))
    ws.factory(p3NameNew+'[{0},{1},{2}]'.format(ws.function(p3Name).getVal(),ws.function(p3Name).getMin(),ws.function(p3Name).getMax()))
    ws.factory(p4NameNew+'[{0},{1},{2}]'.format(ws.function(p4Name).getVal(),ws.function(p4Name).getMin(),ws.function(p4Name).getMax()))
    ws.factory(p5NameNew+'[{0},{1},{2}]'.format(ws.function(p5Name).getVal(),ws.function(p5Name).getMin(),ws.function(p5Name).getMax()))
    ws.factory(p6NameNew+'[{0},{1},{2}]'.format(ws.function(p6Name).getVal(),ws.function(p6Name).getMin(),ws.function(p6Name).getMax()))
    if Ext:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','+normName+'='+normNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+','+p5Name+'='+p5NameNew+','+p6Name+'='+p6NameNew+')')
    else:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+','+p5Name+'='+p5NameNew+','+p6Name+'='+p6NameNew+')')

  elif cat is '5':
    suffix = '_'.join([tev,lepton,'cat'+cat])
    if Ext: normName = 'normBern3_'+suffix
    p0Name = 'p0Bern3_'+suffix
    p1Name = 'p1Bern3_'+suffix
    p2Name = 'p2Bern3_'+suffix
    p3Name = 'p3Bern3_'+suffix

    if Ext: normNameNew  = '_'.join(['bkg',lepton,tev,'cat'+newCat,'norm'])
    p0NameNew  = '_'.join(['bkg','p0',lepton,tev,'cat'+newCat])
    p1NameNew  = '_'.join(['bkg','p1',lepton,tev,'cat'+newCat])
    p2NameNew  = '_'.join(['bkg','p2',lepton,tev,'cat'+newCat])
    p3NameNew  = '_'.join(['bkg','p3',lepton,tev,'cat'+newCat])

    if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
    ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
    ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(),ws.function(p1Name).getMax()))
    ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(),ws.function(p2Name).getMax()))
    ws.factory(p3NameNew+'[{0},{1},{2}]'.format(ws.function(p3Name).getVal(),ws.function(p3Name).getMin(),ws.function(p3Name).getMax()))
    if Ext:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+normName+'='+normNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+')')
    else:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+')')

  else:
    suffix = '_'.join([tev,lepton,'cat'+cat])
    if Ext: normName = 'normGaussBern5_'+suffix
    meanName = 'meanGaussBern5_'+suffix
    sigmaName = 'sigmaGaussBern5_'+suffix
    stepName = 'stepGaussBern5_'+suffix
    p0Name = 'p0GaussBern5_'+suffix
    p1Name = 'p1GaussBern5_'+suffix
    p2Name = 'p2GaussBern5_'+suffix
    p3Name = 'p3GaussBern5_'+suffix
    p4Name = 'p4GaussBern5_'+suffix
    p5Name = 'p5GaussBern5_'+suffix

    if Ext: normNameNew  = '_'.join(['bkg',lepton,tev,'cat'+newCat,'norm'])
    meanNameNew  = '_'.join(['bkg','mean',lepton,tev,'cat'+newCat])
    sigmaNameNew  = '_'.join(['bkg','sigma',lepton,tev,'cat'+newCat])
    stepNameNew  = '_'.join(['bkg','step',lepton,tev,'cat'+newCat])
    p0NameNew  = '_'.join(['bkg','p0',lepton,tev,'cat'+newCat])
    p1NameNew  = '_'.join(['bkg','p1',lepton,tev,'cat'+newCat])
    p2NameNew  = '_'.join(['bkg','p2',lepton,tev,'cat'+newCat])
    p3NameNew  = '_'.join(['bkg','p3',lepton,tev,'cat'+newCat])
    p4NameNew  = '_'.join(['bkg','p4',lepton,tev,'cat'+newCat])
    p5NameNew  = '_'.join(['bkg','p5',lepton,tev,'cat'+newCat])

    if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
    ws.factory(meanNameNew+'[{0}]'.format(ws.function(meanName).getVal()))
    ws.factory(sigmaNameNew+'[{0},{1},{2}]'.format(ws.function(sigmaName).getVal(),ws.function(sigmaName).getMin(),ws.function(sigmaName).getMax()))
    ws.factory(stepNameNew+'[{0},{1},{2}]'.format(ws.function(stepName).getVal(),ws.function(stepName).getMin(),ws.function(stepName).getMax()))
    ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
    ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(),ws.function(p1Name).getMax()))
    ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(),ws.function(p2Name).getMax()))
    ws.factory(p3NameNew+'[{0},{1},{2}]'.format(ws.function(p3Name).getVal(),ws.function(p3Name).getMin(),ws.function(p3Name).getMax()))
    ws.factory(p4NameNew+'[{0},{1},{2}]'.format(ws.function(p4Name).getVal(),ws.function(p4Name).getMin(),ws.function(p4Name).getMax()))
    ws.factory(p5NameNew+'[{0},{1},{2}]'.format(ws.function(p5Name).getVal(),ws.function(p5Name).getMin(),ws.function(p5Name).getMax()))
    if Ext:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','+normName+'='+normNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+','+p5Name+'='+p5NameNew+')')
    else:
      ws.factory('EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew+','
      +p0Name+'='+p0NameNew+','+p1Name+'='+p1NameNew+','+p2Name+'='+p2NameNew+','+p3Name+'='+p3NameNew+','+p4Name+'='+p4NameNew+','+p5Name+'='+p5NameNew+')')




