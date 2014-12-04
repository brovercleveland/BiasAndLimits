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

class FitBuilder:
  FitColorDict = {
      'GaussBern3':kViolet,
      'SechBern3':kMagenta,
      'GaussExp':kGray,
      'GaussPow':kCyan,
      'SechExp':kRed,
      'SechPow':kYellow,
      'GaussBern4':kPink,
      'GaussBern5':kBlue,
      'SechBern4':kBlack,
      'SechBern5':kGreen,
      'Bern2':kViolet,
      'Bern3':kPink,
      'Bern4':kGray,
      'Bern5':kGreen,
      'Exp':kBlue,
      'Exp2':kBlue,
      'ExpSum':kGreen+2,
      'PowExpSum':kOrange,
      'TripExpSum':kBlack,
      'Laurent':kMagenta,
      'Pow':kCyan,
      'PowDecay':kYellow+1,
      'PowLog':kRed+1,
      'PowDecayExp':kGray,
    }

  FitNdofDict = {
    'GaussBern3':5,
    'SechBern3':5,
    'GaussExp':3,
    'GaussPow':3,
    'SechExp':3,
    'SechPow':3,
    'GaussBern4':6,
    'GaussBern5':7,
    'SechBern4':6,
    'SechBern5':7,
    'Exp':1,
    'Exp2':2,
    'ExpSum':3,
    'PowExpSum':3,
    'TripExpSum':5,
    'Laurent':1,
    'Pow':2,
    'Bern2':2,
    'Bern3':3,
    'Bern4':4,
    'Bern5':5,
    'PowDecay':2,
    'PowDecayExp':3,
    'PowLog':3
  }

  def __init__(self,mzg,tev,lepton,cat,sig=None,mass=None):
    if sig == None:
      self.suffix = '_'.join([tev,lepton,'cat'+cat])
    else:
      self.suffix = '_'.join([tev,lepton,'cat'+cat,sig,mass])
      self.sig = sig
      self.mass = mass

    self.mzg = mzg
    self.tev = tev
    self.lepton = lepton
    self.cat = cat
    self.BuildDict = {'BB':self.BuildBetaAndBern,
        'GB': self.BuildGaussAndBern,
        'BetaFunc': self.BuildBetaFunc,
        'Kumaraswamy': self.BuildKumaraswamy,
        'GaussExp': self.BuildGaussExp,
        'GaussPow': self.BuildGaussPow,
        'SechExp': self.BuildSechExp,
        'SechPow': self.BuildSechPow,
        'GaussBern3': self.BuildGaussStepBern3,
        'GaussBern4': self.BuildGaussStepBern4,
        'GaussBern5': self.BuildGaussStepBern5,
        'GaussBern6': self.BuildGaussStepBern6,
        'SechBern3': self.BuildSechStepBern3,
        'SechBern4': self.BuildSechStepBern4,
        'SechBern5': self.BuildSechStepBern5,
        'Exp': self.BuildExp,
        'Pow': self.BuildPow,
        'PowDecay': self.BuildPowDecay,
        'PowDecayExp': self.BuildPowDecayExp,
        'PowLog': self.BuildPowLog,
        'Exp2': self.BuildExp2,
        'ExpSum': self.BuildExpSum,
        'PowExpSum': self.BuildPowExpSum,
        'TripExpSum': self.BuildTripExpSum,
        'Laurent': self.BuildLaurent,
        'Bern2': self.BuildBern2,
        'Bern3': self.BuildBern3,
        'Bern4': self.BuildBern4,
        'Bern5': self.BuildBern5,
        'CBG': self.BuildCrystalBallGauss,
        'DCB': self.BuildDoubleCrystalBall,
        'DCB2': self.BuildDoubleCrystalBall2,
        'TripG': self.BuildTripleGauss}




  def Build(self, funcName, **kargs):
    return self.BuildDict[funcName](**kargs)

  def BuildBetaAndBern(self,rangeName,frac = 0.1, fracLow = 0, fracHigh = 0.9):

    beta = BuildBetaFunc(tev,lepton,cat+'BB',self.mzg,rangeName)
    bern = BuildBern4(tev,lepton,cat+'BB',self.mzg)
    fracVar = RooRealVar('fracBB_'+self.suffix,'fracBB_'+self.suffix,frac,fracLow,fracHigh)
    bbArgs = RooArgList(beta,bern)
    fracArg = RooArgList(fracVar)

    BB = RooAddPdf('BB_'+self.suffix,'BB_'+self.suffix,bbArgs,fracArg,True)
    #BB = RooFFTConvPdf('BB_'+self.suffix,'BB_'+self.suffix,self.mzg,beta,bern)
    SetOwnership(beta,0)
    SetOwnership(bern,0)
    SetOwnership(fracVar,0)
    return BB

  def BuildGaussAndBern(self,rangeName,frac = 0.1, fracLow = 0, fracHigh = 0.9):

    gauss = BuildRooGaussian(tev,lepton,cat+'GB',self.mzg)
    bern = BuildBern3(tev,lepton,cat+'GB',self.mzg)
    fracVar = RooRealVar('fracGB_'+self.suffix,'fracGB_'+self.suffix,frac,fracLow,fracHigh)
    gbArgs = RooArgList(gauss,bern)
    fracArg = RooArgList(fracVar)

    GB = RooAddPdf('GB_'+self.suffix,'GB_'+self.suffix,gbArgs,fracArg,True)
    #BB = RooFFTConvPdf('BB_'+self.suffix,'BB_'+self.suffix,self.mzg,beta,bern)
    SetOwnership(gauss,0)
    SetOwnership(bern,0)
    SetOwnership(fracVar,0)
    return GB


  def BuildBetaFunc(self,rangeName,alpha = 2, alphaLow = 1, alphaHigh = 10, beta = 5, betaLow = 1, betaHigh = 10):

    alphaVar = RooRealVar('alphaBetaFunc_'+self.suffix,'alphaBetaFunc_'+self.suffix, alpha, alphaLow, alphaHigh)
    betaVar = RooRealVar('betaBetaFunc_'+self.suffix,'betaBetaFunc_'+self.suffix, beta, betaLow, betaHigh)
    xLow = self.mzg.getMin(rangeName)
    xRange = self.mzg.getMax(rangeName) - self.mzg.getMin(rangeName)
    gROOT.ProcessLine('.L betaWrapper.cxx+')
    from ROOT import makeBetaPdf
    BetaFunc = makeBetaPdf('BetaFunc_'+self.suffix,self.mzg,alphaVar,betaVar)

    SetOwnership(alphaVar,0)
    SetOwnership(betaVar,0)
    return BetaFunc

  def BuildKumaraswamy(self,rangeName,alpha = 2, alphaLow = 1, alphaHigh = 10, beta = 5, betaLow = 1, betaHigh = 10):

    alphaVar = RooRealVar('alphaKumaraswamy_'+self.suffix,'alphaKumaraswamy_'+self.suffix, alpha, alphaLow, alphaHigh)
    betaVar = RooRealVar('betaKumaraswamy_'+self.suffix,'betaKumaraswamy_'+self.suffix, beta, betaLow, betaHigh)
    xLow = RooRealVar('xLowKumaraswamy_'+self.suffix, 'xLowKumaraswamy_'+self.suffix, self.mzg.getMin(rangeName))
    xRange = RooRealVar('xRangeKumaraswamy_'+self.suffix, 'xReangeKumaraswamy_'+self.suffix,self.mzg.getMax(rangeName) - self.mzg.getMin(rangeName))
    Kumaraswamy = RooGenericPdf('Kumaraswamy_'+self.suffix, 'Kumaraswamy_'+self.suffix, '(@0>@3)*(@0<(@3+@4))*@1*@2*((@0-@3)/@4)**(@1-1)*(1-((@0-@3)/@4)**@1)**(@2)', RooArgList(self.mzg,alphaVar,betaVar,xLow,xRange))

    SetOwnership(alphaVar,0)
    SetOwnership(betaVar,0)
    SetOwnership(xLow,0)
    SetOwnership(xRange,0)
    return Kumaraswamy

  def BuildGaussExp(self,mean = 120, meanLow = 90, meanHigh = 150, sigma = 1, sigmaLow = 0.01, sigmaHigh = 10, tau = 5, tauLow = 0, tauHigh = 50):

    meanVar = RooRealVar('meanGaussExp_'+self.suffix,'meanGaussExp_'+self.suffix, mean, meanLow, meanHigh)
    sigmaVar = RooRealVar('sigmaGaussExp_'+self.suffix,'sigmaGaussExp_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    tauVar = RooRealVar('tauGaussExp_'+self.suffix,'tauGaussExp_'+self.suffix,tau,tauLow,tauHigh)

    turnOn = RooGaussModel('turnOnGaussExp_'+self.suffix,'turnOnGaussExp_'+self.suffix,self.mzg,meanVar,sigmaVar)
    GaussExp = RooDecay('GaussExp_'+self.suffix,'GaussExp_'+self.suffix,self.mzg,tauVar,turnOn,RooDecay.SingleSided)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(tauVar,0)
    SetOwnership(turnOn,0)
    return GaussExp
    #sprintf(sbuffer1, "GaussExpFullExt_cat%i",i+1);
    #GaussExpFullExt[i] = new RooExtendPdf(sbuffer1,sbuffer1,*GaussExpFull[i],*nGaussExp[i]);
    #nGaussExp[i] = new RooRealVar(sbuffer1,sbuffer1,ntcat[i]->GetEntries(),0,3*ntcat[i]->GetEntries());


  def BuildGaussPow(self,mean = 0, sigma = 2, sigmaLow = 0.01, sigmaHigh = 10, alpha = 105 , alphaLow = 50, alphaHigh = 200,beta = 6, betaLow = 0, betaHigh = 20):

    meanVar = RooRealVar('meanGaussPow_'+self.suffix,'meanGaussPow_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussPow_'+self.suffix,'sigmaGaussPow_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    alphaVar = RooRealVar('alphaGaussPow_'+self.suffix,'alphaGaussPow_'+self.suffix,alpha,alphaLow,alphaHigh)
    betaVar = RooRealVar('betaGaussPow_'+self.suffix,'betaGaussPow_'+self.suffix,beta,betaLow,betaHigh)

    turnOn = RooGaussModel('turnOnGaussPow_'+self.suffix,'turnOnGaussPow_'+self.suffix,self.mzg,meanVar,sigmaVar)
    tail = RooGenericPdf('tailGaussPow_'+self.suffix,'tailGaussPow_'+self.suffix,'1e-20 + (@0 > @1)*((@0)^(-@2))',RooArgList(self.mzg,alphaVar,betaVar))
    GaussPow = RooFFTConvPdf('GaussPow_'+self.suffix,'GaussPow_'+self.suffix, self.mzg, tail, turnOn)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(alphaVar,0)
    SetOwnership(betaVar,0)
    SetOwnership(turnOn,0)
    SetOwnership(tail,0)
    return GaussPow

  def BuildSechExp(self,mean = 0, sigma = 5, sigmaLow = 0.01, sigmaHigh = 20, tau = 35, tauLow = 0, tauHigh = 100, alpha = 105, alphaLow = 50, alphaHigh = 200):

    meanVar = RooRealVar('meanSechExp_'+self.suffix,'meanSechExp_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaSechExp_'+self.suffix,'sigmaSechExp_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    tauVar = RooRealVar('tauSechExp_'+self.suffix,'tauSechExp_'+self.suffix,tau,tauLow,tauHigh)
    alphaVar = RooRealVar('alphaSechExp_'+self.suffix,'alphaSechExp_'+self.suffix,alpha,alphaLow,alphaHigh)

    turnOn  = RooGenericPdf('turnOnSechExp_'+self.suffix,'turnOnSechExp_'+self.suffix, 'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(self.mzg,meanVar,sigmaVar))
    tail    = RooGenericPdf('tailSechExp_'+self.suffix,'tailSechExp_'+self.suffix,'1e-20 + (@0 > @1)*(exp(-@0/@2))',RooArgList(self.mzg,alphaVar,tauVar))
    SechExp = RooFFTConvPdf('SechExp_'+self.suffix,'SechExp_'+self.suffix,self.mzg,tail,turnOn)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(alphaVar,0)
    SetOwnership(tauVar,0)
    SetOwnership(turnOn,0)
    SetOwnership(tail,0)
    return SechExp

  def BuildSechPow(self,mean = 0, sigma = 4, sigmaLow = 0.01, sigmaHigh = 20, alpha = 107, alphaLow = 50, alphaHigh = 200, beta = 5, betaLow = 0, betaHigh = 20):

    meanVar = RooRealVar('meanSechPow_'+self.suffix,'meanSechPow_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaSechPow_'+self.suffix,'sigmaSechPow_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    alphaVar = RooRealVar('alphaSechPow_'+self.suffix,'alphaSechPow_'+self.suffix,alpha,alphaLow,alphaHigh)
    betaVar = RooRealVar('betaSechPow_'+self.suffix,'betaSechPow_'+self.suffix,beta,betaLow,betaHigh)

    turnOn = RooGenericPdf('turnOnSechPow_'+self.suffix,'turnOnSechPow_'+self.suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(self.mzg,meanVar,sigmaVar))
    tail = RooGenericPdf('tailSechPow_'+self.suffix,'tailSechPow_'+self.suffix,'1e-20 + (@0 > @1)*((@0)^(-@2))',RooArgList(self.mzg,alphaVar,betaVar))
    SechPow = RooFFTConvPdf('SechPow_'+self.suffix,'SechPow_'+self.suffix, self.mzg, tail, turnOn)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(alphaVar,0)
    SetOwnership(betaVar,0)
    SetOwnership(turnOn,0)
    SetOwnership(tail,0)
    return SechPow

  def BuildGaussStepBern3(self,mean = 0, sigma = 3, sigmaLow = 0.01, sigmaHigh = 20, step = 110, stepLow = 100, stepHigh = 130,
      p0 = 15, p1 = 0.3, p1Low = -1e-6, p1High = 900,p2 = 0.3, p2Low = -1e-6, p2High = 900,p3 = 0.3, p3Low = -1e-6, p3High = 900):

    meanVar = RooRealVar('meanGaussBern3_'+self.suffix,'meanGaussBern3_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussBern3_'+self.suffix,'sigmaGaussBern3_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepGaussBern3_'+self.suffix,'stepGaussBern3_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0GaussBern3_'+self.suffix,'p0GaussBern3_'+self.suffix, p0)
    p1Var = RooRealVar('p1GaussBern3_'+self.suffix,'p1GaussBern3_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2GaussBern3_'+self.suffix,'p2GaussBern3_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3GaussBern3_'+self.suffix,'p3GaussBern3_'+self.suffix,p3,p3Low,p3High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
    GaussBern3 = RooGaussStepBernstein('GaussBern3_'+self.suffix,'GaussBern3_'+self.suffix,self.mzg,meanVar,sigmaVar,stepVar,pArgs)

    returnArgs = [meanVar,sigmaVar,stepVar,p0Var,p1Var,p2Var,p3Var]
    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(stepVar,0)
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return GaussBern3,returnArgs

  def BuildGaussStepBern3Const(self,mean = 0, sigma = 4, step = 115,
      p0 = 15, p1 = 0.3, p2 = 0.3, p3 = 0.3):

    meanVar = RooRealVar('meanGaussBern3_'+self.suffix,'meanGaussBern3_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussBern3_'+self.suffix,'sigmaGaussBern3_'+self.suffix,sigma)
    stepVar = RooRealVar('stepGaussBern3_'+self.suffix,'stepGaussBern3_'+self.suffix,step)
    p0Var = RooRealVar('p0GaussBern3_'+self.suffix,'p0GaussBern3_'+self.suffix,p0)
    p1Var = RooRealVar('p1GaussBern3_'+self.suffix,'p1GaussBern3_'+self.suffix,p1)
    p2Var = RooRealVar('p2GaussBern3_'+self.suffix,'p2GaussBern3_'+self.suffix,p2)
    p3Var = RooRealVar('p3GaussBern3_'+self.suffix,'p3GaussBern3_'+self.suffix,p3)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
    GaussBern3 = RooGaussStepBernstein('GaussBern3_'+self.suffix,'GaussBern3_'+self.suffix,self.mzg,meanVar,sigmaVar,stepVar,pArgs)

    returnArgs = [meanVar,sigmaVar,stepVar,p0Var,p1Var,p2Var,p3Var]
    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(stepVar,0)
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return GaussBern3,returnArgs

  def BuildGaussStepBern4(self,mean = 0, sigma = 4, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
      p0 = 15, p1 = 0.4, p1Low = -1e-6, p1High = 900,p2 = 0.4, p2Low = -1e-6, p2High = 900,p3 = 0.4, p3Low = -1e-6, p3High = 900, p4 = 0.4, p4Low = -1e-6, p4High = 900):
    #def BuildGaussStepBern4(self,mean = 0, sigma = 4, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
      #p0 = 15, p1 = 0.4, p1Low = -1e2, p1High = 900,p2 = 0.4, p2Low = -1e2, p2High = 900,p3 = 0.4, p3Low = -1e2, p3High = 900, p4 = 0.4, p4Low = -1e2, p4High = 900):

    meanVar = RooRealVar('meanGaussBern4_'+self.suffix,'meanGaussBern4_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussBern4_'+self.suffix,'sigmaGaussBern4_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepGaussBern4_'+self.suffix,'stepGaussBern4_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0GaussBern4_'+self.suffix,'p0GaussBern4_'+self.suffix, p0)
    p1Var = RooRealVar('p1GaussBern4_'+self.suffix,'p1GaussBern4_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2GaussBern4_'+self.suffix,'p2GaussBern4_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3GaussBern4_'+self.suffix,'p3GaussBern4_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4GaussBern4_'+self.suffix,'p4GaussBern4_'+self.suffix,p4,p4Low,p4High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var)
    GaussBern4 = RooGaussStepBernstein('GaussBern4_'+self.suffix,'GaussBern4_'+self.suffix,self.mzg,meanVar,sigmaVar,stepVar,pArgs)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(stepVar,0)
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    SetOwnership(p4Var,0)
    return GaussBern4

  def BuildGaussStepBern5(self,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
      p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900, p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900):
    #def BuildGaussStepBern5(self,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
     # p0 = 15, p1 = 0.5, p1Low = -1e2, p1High = 900,p2 = 0.5, p2Low = -1e2, p2High = 900,p3 = 0.5, p3Low = -1e2, p3High = 900, p4 = 0.5, p4Low = -1e2, p4High = 900, p5 = 0.5, p5Low = -1e2, p5High = 900):

    meanVar = RooRealVar('meanGaussBern5_'+self.suffix,'meanGaussBern5_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussBern5_'+self.suffix,'sigmaGaussBern5_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepGaussBern5_'+self.suffix,'stepGaussBern5_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0GaussBern5_'+self.suffix,'p0GaussBern5_'+self.suffix, p0)
    p1Var = RooRealVar('p1GaussBern5_'+self.suffix,'p1GaussBern5_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2GaussBern5_'+self.suffix,'p2GaussBern5_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3GaussBern5_'+self.suffix,'p3GaussBern5_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4GaussBern5_'+self.suffix,'p4GaussBern5_'+self.suffix,p4,p4Low,p4High)
    p5Var = RooRealVar('p5GaussBern5_'+self.suffix,'p5GaussBern5_'+self.suffix,p5,p5Low,p5High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var)
    GaussBern5 = RooGaussStepBernstein('GaussBern5_'+self.suffix,'GaussBern5_'+self.suffix,self.mzg,meanVar,sigmaVar,stepVar,pArgs)

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

#def BuildGaussStepBern6(self,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
#    p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900,
#    p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900, p6 = 0.5, p6Low = -1e-6, p6High = 900):
  def BuildGaussStepBern6(self,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 115, stepLow = 100, stepHigh = 130,
      p0 = 15, p1 = 0.5, p1Low = -1e2, p1High = 900,p2 = 0.5, p2Low = -1e2, p2High = 900,p3 = 0.5, p3Low = -1e2, p3High = 900,
      p4 = 0.5, p4Low = -1e2, p4High = 900, p5 = 0.5, p5Low = -1e2, p5High = 900, p6 = 0.5, p6Low = -1e2, p6High = 900):

    meanVar = RooRealVar('meanGaussBern6_'+self.suffix,'meanGaussBern6_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaGaussBern6_'+self.suffix,'sigmaGaussBern6_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepGaussBern6_'+self.suffix,'stepGaussBern6_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0GaussBern6_'+self.suffix,'p0GaussBern6_'+self.suffix, p0)
    p1Var = RooRealVar('p1GaussBern6_'+self.suffix,'p1GaussBern6_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2GaussBern6_'+self.suffix,'p2GaussBern6_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3GaussBern6_'+self.suffix,'p3GaussBern6_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4GaussBern6_'+self.suffix,'p4GaussBern6_'+self.suffix,p4,p4Low,p4High)
    p5Var = RooRealVar('p5GaussBern6_'+self.suffix,'p5GaussBern6_'+self.suffix,p5,p5Low,p5High)
    p6Var = RooRealVar('p6GaussBern6_'+self.suffix,'p6GaussBern6_'+self.suffix,p6,p6Low,p6High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var,p6Var)
    GaussBern6 = RooGaussStepBernstein('GaussBern6_'+self.suffix,'GaussBern6_'+self.suffix,self.mzg,meanVar,sigmaVar,stepVar,pArgs)

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

  def BuildSechStepBern3(self,mean = 0, sigma = 10, sigmaLow = 0.01, sigmaHigh = 20, step = 0.1, stepLow = 0, stepHigh = 10,
      p0 = 15, p1 = 0.3, p1Low = -1e-6, p1High = 900,p2 = 0.3, p2Low = -1e-6, p2High = 900,p3 = 0.3, p3Low = -1e-6, p3High = 900):

    meanVar = RooRealVar('meanSechBern3_'+self.suffix,'meanSechBern3_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaSechBern3_'+self.suffix,'sigmaSechBern3_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepSechBern3_'+self.suffix,'stepSechBern3_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0SechBern3_'+self.suffix,'p0SechBern3_'+self.suffix, p0)
    p1Var = RooRealVar('p1SechBern3_'+self.suffix,'p1SechBern3_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2SechBern3_'+self.suffix,'p2SechBern3_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3SechBern3_'+self.suffix,'p3SechBern3_'+self.suffix,p3,p3Low,p3High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var)
    turnOn = RooGenericPdf('turnOnSechBern3_'+self.suffix,'turnOnSechBern3_'+self.suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(self.mzg,meanVar,sigmaVar))
    tail = RooStepBernstein('tailSechBern3_'+self.suffix,'tailSechBern3_'+self.suffix,self.mzg,stepVar,pArgs)
    SechBern3 = RooFFTConvPdf('SechBern3_'+self.suffix,'SechBern3_'+self.suffix,self.mzg,tail,turnOn)

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

  def BuildSechStepBern4(self,mean = 0, sigma = 3, sigmaLow = 0.01, sigmaHigh = 20, step = 0.1, stepLow = 0, stepHigh = 10,
      p0 = 15, p1 = 0.4, p1Low = -1e-6, p1High = 900,p2 = 0.4, p2Low = -1e-6, p2High = 900,p3 = 0.4, p3Low = -1e-6, p3High = 900, p4 = 0.4, p4Low = -1e-6, p4High = 900):

    meanVar = RooRealVar('meanSechBern4_'+self.suffix,'meanSechBern4_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaSechBern4_'+self.suffix,'sigmaSechBern4_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepSechBern4_'+self.suffix,'stepSechBern4_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0SechBern4_'+self.suffix,'p0SechBern4_'+self.suffix, p0)
    p1Var = RooRealVar('p1SechBern4_'+self.suffix,'p1SechBern4_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2SechBern4_'+self.suffix,'p2SechBern4_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3SechBern4_'+self.suffix,'p3SechBern4_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4SechBern4_'+self.suffix,'p4SechBern4_'+self.suffix,p4,p4Low,p4High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var)
    turnOn = RooGenericPdf('turnOnSechBern4_'+self.suffix,'turnOnSechBern4_'+self.suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(self.mzg,meanVar,sigmaVar))
    tail = RooStepBernstein('tailSechBern4_'+self.suffix,'tailSechBern4_'+self.suffix,self.mzg,stepVar,pArgs)
    SechBern4 = RooFFTConvPdf('SechBern4_'+self.suffix,'SechBern4_'+self.suffix,self.mzg,tail,turnOn)

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

  def BuildSechStepBern5(self,mean = 0, sigma = 5, sigmaLow = 0.001, sigmaHigh = 60, step = 0.1, stepLow = 0, stepHigh = 10,
      p0 = 15, p1 = 0.5, p1Low = -1e-6, p1High = 900,p2 = 0.5, p2Low = -1e-6, p2High = 900,p3 = 0.5, p3Low = -1e-6, p3High = 900, p4 = 0.5, p4Low = -1e-6, p4High = 900, p5 = 0.5, p5Low = -1e-6, p5High = 900):

    meanVar = RooRealVar('meanSechBern5_'+self.suffix,'meanSechBern5_'+self.suffix, mean)
    sigmaVar = RooRealVar('sigmaSechBern5_'+self.suffix,'sigmaSechBern5_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    stepVar = RooRealVar('stepSechBern5_'+self.suffix,'stepSechBern5_'+self.suffix,step,stepLow,stepHigh)
    p0Var = RooRealVar('p0SechBern5_'+self.suffix,'p0SechBern5_'+self.suffix, p0)
    p1Var = RooRealVar('p1SechBern5_'+self.suffix,'p1SechBern5_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2SechBern5_'+self.suffix,'p2SechBern5_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3SechBern5_'+self.suffix,'p3SechBern5_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4SechBern5_'+self.suffix,'p4SechBern5_'+self.suffix,p4,p4Low,p4High)
    p5Var = RooRealVar('p5SechBern5_'+self.suffix,'p5SechBern5_'+self.suffix,p5,p5Low,p5High)

    pArgs = RooArgList(p0Var,p1Var,p2Var,p3Var,p4Var,p5Var)
    turnOn = RooGenericPdf('turnOnSechBern5_'+self.suffix,'turnOnSechBern5_'+self.suffix,'exp(-(@0-@1)/@2)/(@2*(1.0+exp(-(@0-@1)/@2))**2)',RooArgList(self.mzg,meanVar,sigmaVar))
    tail = RooStepBernstein('tailSechBern5_'+self.suffix,'tailSechBern5_'+self.suffix,self.mzg,stepVar,pArgs)
    SechBern5 = RooFFTConvPdf('SechBern5_'+self.suffix,'SechBern5_'+self.suffix,self.mzg,tail,turnOn)

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

  def BuildExp(self,tau = 1, tauLow = -50, tauHigh = 50):

    tauVar = RooRealVar('tauExp_'+self.suffix,'tauExp_'+self.suffix,tau,tauLow,tauHigh)
    Exp = RooExponential('Exp_'+self.suffix,'Exp_'+self.suffix,self.mzg,tauVar)
    SetOwnership(tauVar,0)
    return Exp

  def BuildPow(self,alpha = 115, alphaLow = 1e-6, alphaHigh = 200, beta = 2, betaLow = 1e-4, betaHigh = 20):

    alphaVar = RooRealVar('alphaPow_'+self.suffix,'alphaPow_'+self.suffix,alpha,alphaLow,alphaHigh)
    betaVar = RooRealVar('betaPow_'+self.suffix,'betaPow_'+self.suffix,beta,betaLow,betaHigh)
    Pow = RooGenericPdf('Pow_'+self.suffix,'Pow_'+self.suffix,'1e-20 + (@1)*((@0)^(-@2))',RooArgList(self.mzg,alphaVar,betaVar))
    SetOwnership(alphaVar,0)
    SetOwnership(betaVar,0)
    return Pow

  def BuildPowDecay(self,p1 = 1, p1Low = 0, p1High = 20, p2 = 1, p2Low = 0, p2High = 20):

    p1Var = RooRealVar('p1PowDecay_'+self.suffix,'p1PowDecay_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2PowDecay_'+self.suffix,'p2PowDecay_'+self.suffix,p2,p2Low,p2High)
    PowDecay = RooGenericPdf('PowDecay_'+self.suffix,'PowDecay_'+self.suffix,'exp(-@1*@0)*((@0)^(-@2))',RooArgList(self.mzg,p1Var,p2Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    return PowDecay

  def BuildPowDecayExp(self,p1 = 1, p1Low = 0, p1High = 10, p2 = 2, p2Low = 0, p2High = 10, p3 = 0.3, p3Low = 0, p3High = 2000):

    p1Var = RooRealVar('p1PowDecayExp_'+self.suffix,'p1PowDecayExp_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2PowDecayExp_'+self.suffix,'p2PowDecayExp_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3PowDecayExp_'+self.suffix,'p3PowDecayExp_'+self.suffix,p3,p3Low,p3High)
    PowDecayExp = RooGenericPdf('PowDecayExp_'+self.suffix,'PowDecayExp_'+self.suffix,'exp(-@1*@0)*((@0)^(-@2))*(@3)^(-@0)',RooArgList(self.mzg,p1Var,p2Var,p3Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return PowDecayExp

  def BuildPowLog(self,p1 = 2, p1Low = -2, p1High = 2, p2 = -1, p2Low = -2, p2High = 2, p3 = 0.5, p3Low = -2, p3High = 2):

    p1Var = RooRealVar('p1PowLog_'+self.suffix,'p1PowLog_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2PowLog_'+self.suffix,'p2PowLog_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3PowLog_'+self.suffix,'p3PowLog_'+self.suffix,p3,p3Low,p3High)
    PowLog = RooGenericPdf('PowLog_'+self.suffix,'PowLog_'+self.suffix,'fabs(1-@0)^(@1)/(@0)^(@2+@3*log(@0))',RooArgList(self.mzg,p1Var,p2Var,p3Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return PowLog

  def BuildExp2(self,p1 = 1, p1Low = 0, p1High = 20, p2 = 1, p2Low = 0, p2High = 20):

    p1Var = RooRealVar('p1Exp2_'+self.suffix,'p1Exp2_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2Exp2_'+self.suffix,'p2Exp2_'+self.suffix,p2,p2Low,p2High)
    Exp2 = RooGenericPdf('Exp2_'+self.suffix,'Exp2_'+self.suffix,'(@2+@1*@0>0)*exp((-@0)/(@2+@1*@0))',RooArgList(self.mzg,p1Var,p2Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    return Exp2

  def BuildExpSum(self,p1 = 0.1, p1Low = 0, p1High = 1, p2 = 0.01, p2Low = 0.00001, p2High = 20, p3 = 0.2, p3Low = 0.00001, p3High = 20):

    p1Var = RooRealVar('p1ExpSum_'+self.suffix,'p1ExpSum_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2ExpSum_'+self.suffix,'p2ExpSum_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3ExpSum_'+self.suffix,'p3ExpSum_'+self.suffix,p3,p3Low,p3High)
    ExpSum = RooGenericPdf('ExpSum_'+self.suffix,'ExpSum_'+self.suffix,'(1-@1)*exp(-@2*@0)+@1*exp(-@3*@0)',RooArgList(self.mzg,p1Var,p2Var,p3Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return ExpSum

  def BuildPowExpSum(self,p1 = 0.1, p1Low = 0, p1High = 1, p2 = 0.01, p2Low = 0.00001, p2High = 20, p3 = 0.2, p3Low = 0.00001, p3High = 20):

    p1Var = RooRealVar('p1PowExpSum_'+self.suffix,'p1PowExpSum_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2PowExpSum_'+self.suffix,'p2PowExpSum_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3PowExpSum_'+self.suffix,'p3PowExpSum_'+self.suffix,p3,p3Low,p3High)
    PowExpSum = RooGenericPdf('PowExpSum_'+self.suffix,'PowExpSum_'+self.suffix,'(1-@1)*@0^(-@2)+@1*exp(-@3*@0)',RooArgList(self.mzg,p1Var,p2Var,p3Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return PowExpSum

  def BuildTripExpSum(self,p1 = 0.1, p1Low = 0.0001, p1High = 0.9999, p2 = 0.1, p2Low = 0.0001, p2High = 0.9999, p3 = 0.2, p3Low = 0.0001, p3High = 1,
      p4 = 0.1, p4Low = 0.0001, p4High = 1, p5 = 0.1, p5Low = 0.0001, p5High = 1):

    p1Var = RooRealVar('p1TripExpSum_'+self.suffix,'p1TripExpSum_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2TripExpSum_'+self.suffix,'p2TripExpSum_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3TripExpSum_'+self.suffix,'p3TripExpSum_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4TripExpSum_'+self.suffix,'p4TripExpSum_'+self.suffix,p4,p4Low,p4High)
    p5Var = RooRealVar('p5TripExpSum_'+self.suffix,'p5TripExpSum_'+self.suffix,p5,p5Low,p5High)
    TripExpSum = RooGenericPdf('TripExpSum_'+self.suffix,'TripExpSum_'+self.suffix,'(2-@1-@2)*exp(-@3*@0)+@1*exp(-@4*@0)+@2*exp(-@5*@0)*(@1+@2<2)',
        RooArgList(self.mzg,p1Var,p2Var,p3Var,p4Var,p5Var))
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    SetOwnership(p4Var,0)
    SetOwnership(p5Var,0)
    return TripExpSum

  def BuildLaurent(self,p1 = 0.5, p1Low = 0, p1High = 1):

    p1Var = RooRealVar('p1Laurent_'+self.suffix,'p1Laurent_'+self.suffix,p1,p1Low,p1High)
    Laurent = RooGenericPdf('Laurent_'+self.suffix,'Laurent_'+self.suffix,'(1-@1)*@0^(-4)+@1*@0^(-5)',RooArgList(self.mzg,p1Var))
    SetOwnership(p1Var,0)
    return Laurent

  def BuildBern2(self,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30):
#def BuildBern2(self,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30):

    p0Var = RooRealVar('p0Bern2_'+self.suffix, 'p0Bern2_'+self.suffix,p0)
    p1Var = RooRealVar('p1Bern2_'+self.suffix, 'p1Bern2_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2Bern2_'+self.suffix, 'p2Bern2_'+self.suffix,p2,p2Low,p2High)
    Bern2 = RooBernstein('Bern2_'+self.suffix,'Bern2_'+self.suffix,self.mzg,RooArgList(p0Var,p1Var,p2Var))
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    return Bern2

  def BuildBern3(self,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30):
#def BuildBern3(self,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30):

    p0Var = RooRealVar('p0Bern3_'+self.suffix, 'p0Bern3_'+self.suffix,p0)
    #p1Var = RooRealVar('p1Bern3_'+self.suffix, 'p1Bern3_'+self.suffix,p1,p1Low,p1High)
    #p2Var = RooRealVar('p2Bern3_'+self.suffix, 'p2Bern3_'+self.suffix,p2,p2Low,p2High)
    #p3Var = RooRealVar('p3Bern3_'+self.suffix, 'p3Bern3_'+self.suffix,p3,p3Low,p3High)
    p1Var = RooRealVar('p1Bern3_'+self.suffix, 'p1Bern3_'+self.suffix,p1)
    p2Var = RooRealVar('p2Bern3_'+self.suffix, 'p2Bern3_'+self.suffix,p2)
    p3Var = RooRealVar('p3Bern3_'+self.suffix, 'p3Bern3_'+self.suffix,p3)
    Bern3 = RooBernstein('Bern3_'+self.suffix,'Bern3_'+self.suffix,self.mzg,RooArgList(p0Var,p1Var,p2Var, p3Var))
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return Bern3

  def BuildPoly3(self,p0 = 1 ,p1 = 5, p1Low = -3000, p1High = 3000, p2 = 5, p2Low = -3000, p2High = 3000, p3 = 5, p3Low = -3000, p3High = 3000):
#def BuildPoly3(self,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30):

    p0Var = RooRealVar('p0Poly3_'+self.suffix, 'p0Poly3_'+self.suffix,p0)
    p1Var = RooRealVar('p1Poly3_'+self.suffix, 'p1Poly3_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2Poly3_'+self.suffix, 'p2Poly3_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3Poly3_'+self.suffix, 'p3Poly3_'+self.suffix,p3,p3Low,p3High)
    Poly3 = RooPolynomial('Poly3_'+self.suffix,'Poly3_'+self.suffix,self.mzg,RooArgList(p0Var,p1Var,p2Var, p3Var))
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    return Poly3

  def BuildBern4(self,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30, p4 = 5, p4Low = -1e-6, p4High = 30):
#def BuildBern4(self,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30, p4 = 5, p4Low =1e-3, p4High = 30):

    p0Var = RooRealVar('p0Bern4_'+self.suffix, 'p0Bern4_'+self.suffix,p0)
    p1Var = RooRealVar('p1Bern4_'+self.suffix, 'p1Bern4_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2Bern4_'+self.suffix, 'p2Bern4_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3Bern4_'+self.suffix, 'p3Bern4_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4Bern4_'+self.suffix, 'p4Bern4_'+self.suffix,p4,p4Low,p4High)
    Bern4 = RooBernstein('Bern4_'+self.suffix,'Bern4_'+self.suffix,self.mzg,RooArgList(p0Var,p1Var,p2Var, p3Var, p4Var))
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    SetOwnership(p4Var,0)
    return Bern4

  def BuildBern5(self,p0 = 1 ,p1 = 5, p1Low = -1e-6, p1High = 30, p2 = 5, p2Low = -1e-6, p2High = 30, p3 = 5, p3Low = -1e-6, p3High = 30, p4 = 5, p4Low = -1e-6, p4High = 30, p5 = 5, p5Low = -1e-6, p5High = 30):
#def BuildBern5(self,p0 = 1 ,p1 = 5, p1Low =1e-3, p1High = 30, p2 = 5, p2Low =1e-3, p2High = 30, p3 = 5, p3Low =1e-3, p3High = 30, p4 = 5, p4Low =1e-3, p4High = 30, p5 = 5, p5Low =1e-3, p5High = 30):

    p0Var = RooRealVar('p0Bern5_'+self.suffix, 'p0Bern5_'+self.suffix,p0)
    p1Var = RooRealVar('p1Bern5_'+self.suffix, 'p1Bern5_'+self.suffix,p1,p1Low,p1High)
    p2Var = RooRealVar('p2Bern5_'+self.suffix, 'p2Bern5_'+self.suffix,p2,p2Low,p2High)
    p3Var = RooRealVar('p3Bern5_'+self.suffix, 'p3Bern5_'+self.suffix,p3,p3Low,p3High)
    p4Var = RooRealVar('p4Bern5_'+self.suffix, 'p4Bern5_'+self.suffix,p4,p4Low,p4High)
    p5Var = RooRealVar('p5Bern5_'+self.suffix, 'p5Bern5_'+self.suffix,p5,p5Low,p5High)
    Bern5 = RooBernstein('Bern5_'+self.suffix,'Bern5_'+self.suffix,self.mzg,RooArgList(p0Var,p1Var,p2Var, p3Var, p4Var, p5Var))
    SetOwnership(p0Var,0)
    SetOwnership(p1Var,0)
    SetOwnership(p2Var,0)
    SetOwnership(p3Var,0)
    SetOwnership(p4Var,0)
    SetOwnership(p5Var,0)
    return Bern5

  def BuildRooGaussian(self, mean = 125,meanLow = 100, meanHigh = 150, sigma = 1.5, sigmaLow = 0.3, sigmaHigh = 70):

    meanVar = RooRealVar('mean_'+self.suffix,'mean_'+self.suffix, mean, meanLow, meanHigh)
    sigmaVar = RooRealVar('sigma_'+self.suffix,'sigma_'+self.suffix,sigma,sigmaLow,sigmaHigh)
    gauss = RooGaussian('gauss_'+self.suffix,'gauss_'+self.suffix,self.mzg,meanVar,sigmaVar)
    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    return gauss

  def BuildCrystalBallGauss(self, piece, mean = 125, meanG = -1, meanGLow = -1, meanGHigh = -1, meanCB = -1, meanCBLow = -1, meanCBHigh = -1,sigmaCB = 1.5, sigmaCBLow = -1, sigmaCBHigh = -1, alpha = 1, alphaLow = 0.1, alphaHigh = 5,
      n = 1, nLow = 0.001, nHigh = 7, sigmaG = 6, sigmaGLow = 0, sigmaGHigh = -1, frac = 0.1, fracLow = 0.01, fracHigh = 0.3):

# good fit params for m=125, cat1, el, new proper
    #  meanGCBG_8TeV_el_cat1_ggH_125_Low 122.628199189
    #  meanCBCBG_8TeV_el_cat1_ggH_125_Low 124.755722062
    #  sigmaGCBG_8TeV_el_cat1_ggH_125_Low 3.27087912216
    #  sigmaCBCBG_8TeV_el_cat1_ggH_125_Low 1.49900133978
    #  alphaCBG_8TeV_el_cat1_ggH_125_Low 0.944616084705
    #  nCBG_8TeV_el_cat1_ggH_125_Low 16.4081813986
    #  fracCBG_8TeV_el_cat1_ggH_125_Low 0.299323090074
    if sigmaCB > sigmaCBHigh:
      sigmaCBHigh = sigmaCB *1.5
      sigmaCBLow = sigmaCB * 0.5
    if sigmaG > sigmaGHigh:
      sigmaGHigh = sigmaG * 1.5
      sigmaGLow = sigmaG * 0.8

    suffix = self.suffix+'_'+piece
    if meanG == -1: meanG = mean
    if meanCB == -1: meanCB = mean

    if meanGLow is -1: meanGLow = meanG*0.8
    if meanGHigh is -1: meanGHigh = meanG*1.2
    if meanCBLow is -1: meanCBLow = meanCB*0.8
    if meanCBHigh is -1: meanCBHigh = meanCB*1.2


    meanGVar = RooRealVar('meanGCBG_'+suffix,'meanGCBG_'+suffix, meanG, meanGLow, meanGHigh)
    meanCBVar = RooRealVar('meanCBCBG_'+suffix,'meanCBCBG_'+suffix, meanCB, meanCBLow, meanCBHigh)
    sigmaCBVar = RooRealVar('sigmaCBCBG_'+suffix,'sigmaCBCBG_'+suffix,sigmaCB,sigmaCBLow,sigmaCBHigh)
    alphaVar = RooRealVar('alphaCBG_'+suffix,'alphaCBG_'+suffix,alpha,alphaLow,alphaHigh)
    nVar = RooRealVar('nCBG_'+suffix,'nCBG_'+suffix,n,nLow,nHigh)
    sigmaGVar = RooRealVar('sigmaGCBG_'+suffix,'sigmaGCBG_'+suffix,sigmaG,sigmaGLow,sigmaGHigh)
    fracVar = RooRealVar('fracCBG_'+suffix,'fracCBG_'+suffix,frac,fracLow,fracHigh)

    crystal = RooCBShape('crystalCBG_'+suffix,'crystalCBG_'+suffix,self.mzg,meanCBVar,sigmaCBVar,alphaVar,nVar)
    #gauss = RooGaussian('gaussCBG_'+suffix,'gaussCBG_'+suffix,self.mzg,meanGVar,sigmaGVar)
    gauss = RooGaussian('gaussCBG_'+suffix,'gaussCBG_'+suffix,self.mzg,meanCBVar,sigmaGVar)
    #gauss = RooGaussian('gaussCBG_'+suffix,'gaussCBG_'+suffix,self.mzg,meanCBVar,sigmaCBVar)
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
    paramList = [meanGVar,meanCBVar,sigmaGVar,sigmaCBVar,alphaVar,nVar,fracVar]
    return CBG, paramList

  def BuildDoubleCrystalBall(self, piece, mean = 125,  meanLow = -1, meanHigh = -1, sigma = 1.5, sigmaLow = 0, sigmaHigh = -1,
      alphaCB1 = 0.6, alphaCB1Low = 0.4, alphaCB1High = 1,
      alphaCB2 = -0.6, alphaCB2Low = -2, alphaCB2High = -0.001,
      nCB1 = 5, nCB1Low = 4, nCB1High = 6,
      nCB2 = 7, nCB2Low = 6, nCB2High =20,
      frac = 0.5, fracLow = 0.4, fracHigh = 0.9):

    if sigma > sigmaHigh:
      sigmaHigh = sigma * 2
      sigmaLow = sigma * 0.5

    suffix = self.suffix+'_'+piece

    if meanLow is -1: meanLow = mean*0.8
    if meanHigh is -1: meanHigh = mean*1.2


    meanVar = RooRealVar('meanDCB_'+suffix,'meanDCB_'+suffix, mean, meanLow, meanHigh)
    alphaCB1Var = RooRealVar('alphaCB1DCB_'+suffix,'alphaCB1DCB_'+suffix,alphaCB1,alphaCB1Low,alphaCB1High)
    alphaCB2Var = RooRealVar('alphaCB2DCB_'+suffix,'alphaCB2DCB_'+suffix,alphaCB2,alphaCB2Low,alphaCB2High)
    nCB1Var = RooRealVar('nCB1DCB_'+suffix,'nCB1DCB_'+suffix,nCB1,nCB1Low,nCB1High)
    nCB2Var = RooRealVar('nCB2DCB_'+suffix,'nCB2DCB_'+suffix,nCB2,nCB2Low,nCB2High)
    sigmaVar = RooRealVar('sigmaDCB_'+suffix,'sigmaDCB_'+suffix,sigma,sigmaLow,sigmaHigh)
    fracVar = RooRealVar('fracDCB_'+suffix,'fracDCB_'+suffix,frac,fracLow,fracHigh)

    crystal1 = RooCBShape('crystal1DCB_'+suffix,'crystal1DCB_'+suffix,self.mzg,meanVar,sigmaVar,alphaCB1Var,nCB1Var)
    crystal2 = RooCBShape('crystal2DCB_'+suffix,'crystal2DCB_'+suffix,self.mzg,meanVar,sigmaVar,alphaCB2Var,nCB2Var)
    cbArgs = RooArgList(crystal1,crystal2)
    fracArg = RooArgList(fracVar)
    DCB = RooAddPdf('DCB_'+suffix,'DCB_'+suffix,cbArgs,fracArg,True)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaVar,0)
    SetOwnership(alphaCB1Var,0)
    SetOwnership(alphaCB2Var,0)
    SetOwnership(nCB1Var,0)
    SetOwnership(nCB2Var,0)
    SetOwnership(fracVar,0)
    SetOwnership(crystal1,0)
    SetOwnership(crystal2,0)
    paramList = [meanVar,sigmaVar,alphaCB1Var,alphaCB2Var,nCB1Var,nCB2Var,fracVar]
    return DCB, paramList

  def BuildDoubleCrystalBall2(self, piece, mean = 125,  meanLow = -1, meanHigh = -1, sigmaCB1 = 1.5, sigmaCB1Low = 0.3, sigmaCB1High = 10, sigmaCB2 = 1.5, sigmaCB2Low = 0.3, sigmaCB2High = 10,
      alphaCB1 = 1, alphaCB1Low = 0, alphaCB1High = 8,
      alphaCB2 = -1, alphaCB2Low = -8, alphaCB2High = 0,
      nCB1 = 5, nCB1Low = 0, nCB1High = 10,
      nCB2 = 5, nCB2Low = 0, nCB2High =10,
      frac = 0.5, fracLow = 0, fracHigh = 1):

    if sigmaCB1 > sigmaCB1High:
      sigmaCB1High = sigmaCB1 * 5
      sigmaCB1Low = sigmaCB1 * 0.2
    if sigmaCB2 > sigmaCB2High:
      sigmaCB2High = sigmaCB2 * 5
      sigmaCB2Low = sigmaCB2 * 0.2

    suffix = self.suffix+'_'+piece

    if meanLow is -1: meanLow = mean*0.8
    if meanHigh is -1: meanHigh = mean*1.2


    meanVar = RooRealVar('meanDCB_'+suffix,'meanDCB_'+suffix, mean, meanLow, meanHigh)
    alphaCB1Var = RooRealVar('alphaCB1DCB_'+suffix,'alphaCB1DCB_'+suffix,alphaCB1,alphaCB1Low,alphaCB1High)
    alphaCB2Var = RooRealVar('alphaCB2DCB_'+suffix,'alphaCB2DCB_'+suffix,alphaCB2,alphaCB2Low,alphaCB2High)
    nCB1Var = RooRealVar('nCB1DCB_'+suffix,'nCB1DCB_'+suffix,nCB1,nCB1Low,nCB1High)
    nCB2Var = RooRealVar('nCB2DCB_'+suffix,'nCB2DCB_'+suffix,nCB2,nCB2Low,nCB2High)
    sigmaCB1Var = RooRealVar('sigmaCB1DCB_'+suffix,'sigmaCB1DCB_'+suffix,sigmaCB1,sigmaCB1Low,sigmaCB1High)
    sigmaCB2Var = RooRealVar('sigmaCB2DCB_'+suffix,'sigmaCB2DCB_'+suffix,sigmaCB2,sigmaCB2Low,sigmaCB2High)
    fracVar = RooRealVar('fracDCB_'+suffix,'fracDCB_'+suffix,frac,fracLow,fracHigh)

    crystal1 = RooCBShape('crystal1DCB_'+suffix,'crystal1DCB_'+suffix,self.mzg,meanVar,sigmaCB1Var,alphaCB1Var,nCB1Var)
    crystal2 = RooCBShape('crystal2DCB_'+suffix,'crystal2DCB_'+suffix,self.mzg,meanVar,sigmaCB2Var,alphaCB2Var,nCB2Var)
    cbArgs = RooArgList(crystal1,crystal2)
    fracArg = RooArgList(fracVar)
    DCB = RooAddPdf('DCB_'+suffix,'DCB_'+suffix,cbArgs,fracArg,True)

    SetOwnership(meanVar,0)
    SetOwnership(sigmaCB1Var,0)
    SetOwnership(sigmaCB2Var,0)
    SetOwnership(alphaCB1Var,0)
    SetOwnership(alphaCB2Var,0)
    SetOwnership(nCB1Var,0)
    SetOwnership(nCB2Var,0)
    SetOwnership(fracVar,0)
    SetOwnership(crystal1,0)
    SetOwnership(crystal2,0)
    paramList = [meanVar,sigmaCB1Var,sigmaCB2Var,alphaCB1Var,alphaCB2Var,nCB1Var,nCB2Var,fracVar]
    return DCB, paramList


  def BuildTripleGauss(self, piece, mean = 125, mean1 = -1, mean1Low = -1, mean1High = -1, sigma1 = 2, sigma1Low = 1, sigma1High = 8,
      delta21 = 0, delta21Low = -2, delta21High = 2, s21 = 3, s21Low = 1, s21High = 30, delta31 = 0, delta31Low = -2, delta31High = 2,
      s32 = 3, s32Low = 1, s32High = 30, frac23 = 0.9, frac23Low = 0, frac23High = 1, frac123 = 0.9, frac123Low = 0, frac123High = 1):

    suffix = self.suffix+'_'+piece
    mean1 = mean
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

    gauss1 = RooGaussian('gauss1TripG_'+suffix,'gauss1TripG_'+suffix,self.mzg,mean1Var,sigma1Var)
    gauss2 = RooGaussian('gauss2TripG_'+suffix,'gauss2TripG_'+suffix,self.mzg,mean2Var,sigma2Var)
    gauss3 = RooGaussian('gauss3TripG_'+suffix,'gauss3TripG_'+suffix,self.mzg,mean3Var,sigma3Var)
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

  def SignalNameParamFixer(self, ws, fitName):

    if fitName == 'CBG':

      fitName = '_'.join(['CBG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      newFitName = '_'.join([self.sig,'hzg',self.lepton,'cat'+self.cat,self.tev])
      meanG = '_'.join(['meanGCBG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      meanCB = '_'.join(['meanCBCBG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigmaCB = '_'.join(['sigmaCBCBG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigmaG = '_'.join(['sigmaGCBG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      meanGNew = '_'.join(['sig',self.sig,'meanG',self.lepton,self.tev,'cat'+self.cat])
      meanCBNew = '_'.join(['sig',self.sig,'meanCB',self.lepton,self.tev,'cat'+self.cat])
      sigmaCBNew = '_'.join(['sig',self.sig,'sigmaCB',self.lepton,self.tev,'cat'+self.cat])
      sigmaGNew = '_'.join(['sig',self.sig,'sigmaG',self.lepton,self.tev,'cat'+self.cat])
      mShift = '_'.join(['sig',self.sig,'mShift',self.lepton,self.tev,'cat'+self.cat])
      sigmaShift = '_'.join(['sig',self.sig,'sigmaShift',self.lepton,self.tev,'cat'+self.cat])
      ws.factory(mShift+'[1]')
      ws.factory(sigmaShift+'[1]')
      #ws.factory('prod::'+meanGNew+'('+meanG+','+mShift+')')
      ws.factory('prod::'+meanCBNew+'('+meanCB+','+mShift+')')
      ws.factory('prod::'+sigmaCBNew+'('+sigmaCB+','+sigmaShift+')')
      ws.factory('prod::'+sigmaGNew+'('+sigmaG+','+sigmaShift+')')
      #ws.factory('EDIT::'+newFitName+'('+fitName+','+meanG+'='+meanGNew+','+meanCB+'='+meanCBNew+','+sigmaCB+'='+sigmaCBNew+','+sigmaG+'='+sigmaGNew+')')
      ws.factory('EDIT::'+newFitName+'('+fitName+','+meanCB+'='+meanCBNew+','+sigmaCB+'='+sigmaCBNew+','+sigmaG+'='+sigmaGNew+')')
      #ws.factory('EDIT::'+newFitName+'('+fitName+','+meanCB+'='+meanCBNew+','+sigmaCB+'='+sigmaCBNew+')')

    elif fitName == 'DCB':

      fitName = '_'.join(['DCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      newFitName = '_'.join([self.sig,'hzg',self.lepton,'cat'+self.cat,self.tev])
      mean = '_'.join(['meanDCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma = '_'.join(['sigmaDCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      meanNew = '_'.join(['sig',self.sig,'mean',self.lepton,self.tev,'cat'+self.cat])
      sigmaNew = '_'.join(['sig',self.sig,'sigma',self.lepton,self.tev,'cat'+self.cat])
      mShift = '_'.join(['sig',self.sig,'mShift',self.lepton,self.tev,'cat'+self.cat])
      sigmaShift = '_'.join(['sig',self.sig,'sigmaShift',self.lepton,self.tev,'cat'+self.cat])
      ws.factory(mShift+'[1]')
      ws.factory(sigmaShift+'[1]')
      ws.factory('prod::'+meanNew+'('+mean+','+mShift+')')
      ws.factory('prod::'+sigmaNew+'('+sigma+','+sigmaShift+')')
      ws.factory('EDIT::'+newFitName+'('+fitName+','+mean+'='+meanNew+','+sigma+'='+sigmaNew+')')

    elif fitName == 'DCB2':

      fitName = '_'.join(['DCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      newFitName = '_'.join([self.sig,'hzg',self.lepton,'cat'+self.cat,self.tev])
      mean = '_'.join(['meanDCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma1 = '_'.join(['sigmaCB1DCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma2 = '_'.join(['sigmaCB2DCB',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      meanNew = '_'.join(['sig',self.sig,'mean',self.lepton,self.tev,'cat'+self.cat])
      sigma1New = '_'.join(['sig',self.sig,'sigma1',self.lepton,self.tev,'cat'+self.cat])
      sigma2New = '_'.join(['sig',self.sig,'sigma2',self.lepton,self.tev,'cat'+self.cat])
      mShift = '_'.join(['sig',self.sig,'mShift',self.lepton,self.tev,'cat'+self.cat])
      sigmaShift = '_'.join(['sig',self.sig,'sigmaShift',self.lepton,self.tev,'cat'+self.cat])
      ws.factory(mShift+'[1]')
      ws.factory(sigmaShift+'[1]')
      ws.factory('prod::'+meanNew+'('+mean+','+mShift+')')
      ws.factory('prod::'+sigma1New+'('+sigma1+','+sigmaShift+')')
      ws.factory('prod::'+sigma2New+'('+sigma2+','+sigmaShift+')')
      ws.factory('EDIT::'+newFitName+'('+fitName+','+mean+'='+meanNew+','+sigma1+'='+sigma1New+','+sigma2+'='+sigma2New+')')

    elif fitName == 'TripG':

      fitName = '_'.join(['TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      newFitName = '_'.join([self.sig,'hzg',self.lepton,'cat'+self.cat,self.tev])

      mean1 = '_'.join(['mean1TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      mean2 = '_'.join(['mean2TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      mean3 = '_'.join(['mean3TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma1 = '_'.join(['sigma1TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma2 = '_'.join(['sigma2TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      sigma3 = '_'.join(['sigma3TripG',self.tev,self.lepton,'cat'+self.cat,self.sig,self.mass,'Interp'])
      mean1New = '_'.join(['sig',self.sig,'mean1',self.lepton,self.tev,'cat'+self.cat])
      mean2New = '_'.join(['sig',self.sig,'mean2',self.lepton,self.tev,'cat'+self.cat])
      mean3New = '_'.join(['sig',self.sig,'mean3',self.lepton,self.tev,'cat'+self.cat])
      sigma1New = '_'.join(['sig',self.sig,'sigma1',self.lepton,self.tev,'cat'+self.cat])
      sigma2New = '_'.join(['sig',self.sig,'sigma2',self.lepton,self.tev,'cat'+self.cat])
      sigma3New = '_'.join(['sig',self.sig,'sigma3',self.lepton,self.tev,'cat'+self.cat])

      mShift = '_'.join(['sig',self.sig,'mShift',self.lepton,self.tev,'cat'+self.cat])
      sigmaShift = '_'.join(['sig',self.sig,'sigmaShift',self.lepton,self.tev,'cat'+self.cat])

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
    else:
      raise NameError('Cannot fix signal name "{0}"'.format(fitName))

  def BackgroundNameFixer(self,ws,fitName,Ext = True):
    dataName = '_'.join(['data',self.suffix])
    dataNameNew = '_'.join(['data','obs',self.suffix])
    if Ext:
      fitExtName = '_'.join(['bkgTmp',self.suffix])
    else:
      fitExtName = fitName+'_'+self.suffix

    newSuffix = '_'.join([self.lepton,self.tev,'cat'+self.cat])
    fitExtNameNew = '_'.join(['bkg',newSuffix])

    if fitName[0:-1] == 'GaussBern':
      pNames = []
      pNamesNew = []
      if Ext:
        normName = 'norm'+fitName+'_'+self.suffix
        normNameNew  = '_'.join(['bkg',newSuffix,'norm'])

      meanName = 'mean'+fitName+'_'+self.suffix
      sigmaName = 'sigma'+fitName+'_'+self.suffix
      stepName = 'step'+fitName+'_'+self.suffix
      p0Name = 'p0'+fitName+'_'+self.suffix
      meanNameNew  = '_'.join(['bkg','mean',newSuffix])
      sigmaNameNew  = '_'.join(['bkg','sigma',newSuffix])
      stepNameNew  = '_'.join(['bkg','step',newSuffix])
      p0NameNew  = '_'.join(['bkg','p0',newSuffix])
      for p in range(1,int(fitName[-1])+1):
        pNames.append('p'+str(p)+fitName+'_'+self.suffix)
        pNamesNew.append('_'.join(['bkg','p'+str(p),newSuffix]))

      if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
      ws.factory(meanNameNew+'[{0}]'.format(ws.function(meanName).getVal()))
      ws.factory(sigmaNameNew+'[{0},{1},{2}]'.format(ws.function(sigmaName).getVal(),ws.function(sigmaName).getMin(),ws.function(sigmaName).getMax()))
      ws.factory(stepNameNew+'[{0},{1},{2}]'.format(ws.function(stepName).getVal(),ws.function(stepName).getMin(),ws.function(stepName).getMax()))
      ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
      for i in range(int(fitName[-1])):
        ws.factory(pNamesNew[i]+'[{0},{1},{2}]'.format(ws.function(pNames[i]).getVal(),ws.function(pNames[i]).getMin(),ws.function(pNames[i]).getMax()))

      editString = 'EDIT::'+fitExtNameNew+'('+fitExtName+','+meanName+'='+meanNameNew+','+sigmaName+'='+sigmaNameNew+','+stepName+'='+stepNameNew
      if Ext: editString += ','+normName+'='+normNameNew
      editString += ','+p0Name+'='+p0NameNew
      for i in range (int(fitName[-1])):
        editString += ','+pNames[i]+'='+pNamesNew[i]
      editString += ')'

      ws.factory(editString)


    elif fitName[0:-1] == 'Bern':
      pNames = []
      pNamesNew= []
      if Ext:
        normName = 'norm'+fitName+'_'+self.suffix
        normNameNew  = '_'.join(['bkg',newSuffix,'norm'])

      p0Name = 'p0'+fitName+'_'+self.suffix
      p0NameNew  = '_'.join(['bkg','p0',newSuffix])
      for p in range(1,int(fitName[-1])+1):
        pNames.append('p'+str(p)+fitName+'_'+self.suffix)
        pNamesNew.append('_'.join(['bkg','p'+str(p),newSuffix]))

      if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
      ws.factory(p0NameNew+'[{0}]'.format(ws.function(p0Name).getVal()))
      for i in range(int(fitName[-1])):
        ws.factory(pNamesNew[i]+'[{0},{1},{2}]'.format(ws.function(pNames[i]).getVal(),ws.function(pNames[i]).getMin(),ws.function(pNames[i]).getMax()))

      editString = 'EDIT::'+fitExtNameNew+'('+fitExtName
      if Ext: editString += ','+normName+'='+normNameNew
      editString += ','+p0Name+'='+p0NameNew
      for i in range (int(fitName[-1])):
        editString += ','+pNames[i]+'='+pNamesNew[i]
      editString += ')'

      ws.factory(editString)


    elif fitName == 'PowDecay':
      if Ext:
        normName = 'norm'+fitName+'_'+self.suffix
        normNameNew  = '_'.join(['bkg',newSuffix,'norm'])

      p1Name = 'p1'+fitName+'_'+self.suffix
      p1NameNew  = '_'.join(['bkg','p1',newSuffix])
      p2Name = 'p2'+fitName+'_'+self.suffix
      p2NameNew  = '_'.join(['bkg','p2',newSuffix])

      if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
      ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(), ws.function(p1Name).getMax()))
      ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(), ws.function(p2Name).getMax()))

      editString = 'EDIT::'+fitExtNameNew+'('+fitExtName
      if Ext: editString += ','+normName+'='+normNameNew
      editString += ','+p1Name+'='+p1NameNew
      editString += ','+p2Name+'='+p2NameNew
      editString += ')'

      ws.factory(editString)

    elif fitName == 'TripExpSum':
      if Ext:
        normName = 'norm'+fitName+'_'+self.suffix
        normNameNew  = '_'.join(['bkg',newSuffix,'norm'])

      p1Name = 'p1'+fitName+'_'+self.suffix
      p1NameNew  = '_'.join(['bkg','p1',newSuffix])
      p2Name = 'p2'+fitName+'_'+self.suffix
      p2NameNew  = '_'.join(['bkg','p2',newSuffix])
      p3Name = 'p3'+fitName+'_'+self.suffix
      p3NameNew  = '_'.join(['bkg','p3',newSuffix])
      p4Name = 'p4'+fitName+'_'+self.suffix
      p4NameNew  = '_'.join(['bkg','p4',newSuffix])
      p5Name = 'p5'+fitName+'_'+self.suffix
      p5NameNew  = '_'.join(['bkg','p5',newSuffix])

      if Ext: ws.factory(normNameNew+'[{0},{1},{2}]'.format(ws.function(normName).getVal(),ws.function(normName).getMin(), ws.function(normName).getMax()))
      ws.factory(p1NameNew+'[{0},{1},{2}]'.format(ws.function(p1Name).getVal(),ws.function(p1Name).getMin(), ws.function(p1Name).getMax()))
      ws.factory(p2NameNew+'[{0},{1},{2}]'.format(ws.function(p2Name).getVal(),ws.function(p2Name).getMin(), ws.function(p2Name).getMax()))
      ws.factory(p3NameNew+'[{0},{1},{2}]'.format(ws.function(p3Name).getVal(),ws.function(p3Name).getMin(), ws.function(p3Name).getMax()))
      ws.factory(p4NameNew+'[{0},{1},{2}]'.format(ws.function(p4Name).getVal(),ws.function(p4Name).getMin(), ws.function(p4Name).getMax()))
      ws.factory(p5NameNew+'[{0},{1},{2}]'.format(ws.function(p5Name).getVal(),ws.function(p5Name).getMin(), ws.function(p5Name).getMax()))

      editString = 'EDIT::'+fitExtNameNew+'('+fitExtName
      if Ext: editString += ','+normName+'='+normNameNew
      editString += ','+p1Name+'='+p1NameNew
      editString += ','+p2Name+'='+p2NameNew
      editString += ','+p3Name+'='+p3NameNew
      editString += ','+p4Name+'='+p4NameNew
      editString += ','+p5Name+'='+p5NameNew
      editString += ')'

      ws.factory(editString)

    else:
      raise NameError('Cannot fix params for '+fitName)
