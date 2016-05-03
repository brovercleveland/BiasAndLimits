#!/usr/bin/env python
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os,sys
import argparse
from toyStructs import makeToyStucts
makeToyStucts()
from ROOT import *
import numpy as np
import configLimits as cfl
from rooFitBuilder import FitBuilder
from numpy import genfromtxt
import numpy as np

gROOT.SetBatch()
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

verbose = cfl.verbose

doMVA = cfl.doMVA

allBiasFits= cfl.allBiasFits# Turn on extra fits used in bias studies

YR = cfl.YR

sigFit = cfl.sigFit

highMass = cfl.highMass

testFuncs = cfl.testFuncs

suffix = cfl.suffixPostFix

yearToTeV = {'2011':'7TeV','2012':'8TeV'}

if cfl.rootrace: RooTrace.active(kTRUE)

def getArgs():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v","--verbose",action = "store_true")
  group.add_argument("-q","--quiet",action = "store_true")
  parser.add_argument("--tev", help="CoM Energy", default = cfl.tevList[0], choices = ['7TeV','8TeV'] )
  parser.add_argument("--lepton", help="Lepton Flavor", default = cfl.leptonList[0], choices = ['mu','el'])
  parser.add_argument("--cat", help="Cat Number", default = cfl.catListSmall[0], type = int)
  parser.add_argument("--genFunc", help="PDF used to generate toy data", default = cfl.genFuncs[0], type = str)
  parser.add_argument("--mass", help="Mass of signal template", default = cfl.massList[0], type = int)
  parser.add_argument("--trials", help="Number of trials", default = 1, type = int)
  parser.add_argument("--job", help="Job number", default = -1, type = int)
  parser.add_argument("--plotEvery", help="Plot every N trials", default = 1, type = int)
  args = parser.parse_args()
  return args



def doBiasStudy(tev, lepton, cat, genFunc, mass, trials, job, plotEvery):
  #get all the starting objects
  print genFunc

  c = TCanvas("c","c",0,0,500,400)
  c.cd()
  c.SetLogy(True)

  injectedSignalSize = 0


  rooWsFile = TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix.rstrip('_Cut')+'.root','r')
  myWs = rooWsFile.Get('ws')
  rooWsFile.Close()
  sigRangeName = '_'.join(['range',lepton,tev,'cat'+cat,'M'+mass])

  # get the x-axis
  mzg = myWs.var('CMS_hzg_mass')
  weight  = RooRealVar('Weight','Weight',0,100)
  binning = (mzg.getMax()-mzg.getMin())/8
  if verbose:
    mzg.Print()
    print sigRangeName, mzg.getMin(sigRangeName), mzg.getMax(sigRangeName)
  #if genFunc == 'boot':
  #  mzg_boot  = myWs.var('CMS_hzg_mass_boot')


  # get the data
  dataName = '_'.join(['data',lepton,tev,'cat'+cat])
  print dataName
  data = myWs.data(dataName)
  realDataYield = data.sumEntries()
  bkgInSigWin= data.sumEntries('1',sigRangeName)
  if verbose: data.Print()
  if verbose: print 'total data:', realDataYield, 'total data2:', data.numEntries(),'total data in sig window:', bkgInSigWin


  # get the gen pdf
  #genFitName = '_'.join([genFunc,tev,lepton,'cat'+cat])
  #print genFitName
  #genFit = myWs.pdf(genFitName)
  #if verbose:
  #  print genFitName
  #  genFit.Print()

  # get the signal
  #if genFunc == 'boot':
  #  sigName = '_'.join(['pdf_boot','sig',lepton,tev,'cat'+cat,'M'+mass])
  #else:
  sigName = '_'.join(['pdf','sig',lepton,tev,'cat'+cat,'M'+mass])
  sig = myWs.pdf(sigName)
  if verbose:
    print sigName
    sig.Print()

  # get the test functions, turn them into extended pdfs with signal models.
  testPdfs = []
  testBkgNorms = []
  testPdfs_ext = []
  testSigNorms = []
  testSig_ext = []
  testModels = []

  fitName = '_'.join([genFunc,tev,lepton,'cat'+cat])
  if genFunc == 'boot':
    myGenFunc = 'boot'
  else:
    myGenFunc = myWs.pdf(fitName).Clone()
    myGenFunc.Print()
  for func in testFuncs:
    fitName = '_'.join([func,tev,lepton,'cat'+cat])
    if myGenFunc == 'boot':
        #fitBuilder = FitBuilder(mzg_boot, '8TeV', lepton, cat)
        fitBuilder = FitBuilder(mzg, '8TeV', lepton, cat)
        if lepton == 'el':
          fit = fitBuilder.Build('TripExpSum',
              p1Low=1e-7,p2Low=1e-7,p3Low=1e-7,p4Low=1e-7,p5Low=1e-7, p1High=0.5,p2High=0.5,p3High=1,p4High=1,p5High=1,
              p1 = myWs.var('p1TripExpSum_8TeV_el_cat0').getValV(),
              p2 = myWs.var('p2TripExpSum_8TeV_el_cat0').getValV(),
              p3 = myWs.var('p3TripExpSum_8TeV_el_cat0').getValV(),
              p4 = myWs.var('p4TripExpSum_8TeV_el_cat0').getValV(),
              p5 = myWs.var('p5TripExpSum_8TeV_el_cat0').getValV())
        else:
          fit = fitBuilder.Build('TripExpSum',
              p1 = myWs.var('p1TripExpSum_8TeV_mu_cat0').getValV(),
              p2 = myWs.var('p2TripExpSum_8TeV_mu_cat0').getValV(),
              p3 = myWs.var('p3TripExpSum_8TeV_mu_cat0').getValV(),
              p4 = myWs.var('p4TripExpSum_8TeV_mu_cat0').getValV(),
              p5 = myWs.var('p5TripExpSum_8TeV_mu_cat0').getValV())
        testPdfs.append(fit)
    else:
      testPdfs.append(myWs.pdf(fitName))
    if verbose:
      print fitName
      testPdfs[-1].Print()
      print bkgInSigWin
      print sigRangeName
      print -bkgInSigWin*3-0.1, bkgInSigWin*3+0.1
      raw_input()
    if mass=='800':
      bgUp = max(bkgInSigWin*3,10)
      bgDown = -2
    elif mass =='1200':
      bgUp = max(bkgInSigWin*3,2)
      bgDown = -2
    else:
      bgUp = bkgInSigWin*3
      bgDown = -bkgInSigWin*3
    testBkgNorms.append(RooRealVar('norm'+fitName,'norm'+fitName,bkgInSigWin,bgDown,bgUp))
    testPdfs_ext.append(RooExtendPdf('ext'+fitName,'ext'+fitName,testPdfs[-1],testBkgNorms[-1],sigRangeName))
    #testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,0,-5*bkgInSigWin,5*bkgInSigWin))
    if cfl.injectedSignalSize:
      if mass=='800':
        sigUp = injectedSignalSize*3
        sigDown = -injectedSignalSize*3
      elif mass =='1200':
        sigUp = injectedSignalSize*3
        sigDown = -injectedSignalSize*3
      else:
        sigUp = injectedSignalSize*5
        sigDown = -injectedSignalSize*5
      injectedSignalSize = max(5,int(3*np.sqrt(float(bkgInSigWin))))
      #testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,injectedSignalSize,-5*injectedSignalSize, 5*injectedSignalSize))
      testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,injectedSignalSize,-injectedSignalSize*1.5, injectedSignalSize*3))
    else:
      if mass=='800':
        sigUp = 1
        sigDown = -1
      elif mass =='1200':
        sigUp = 0.1
        sigDown = -0.1
      else:
        sigUp = bkgInSigWin*2
        sigDown = -bkgInSigWin*2
      #print sigDown,sigUp
      #raw_input()
      #testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,0,min(-bkgInSigWin*10,-10),max(bkgInSigWin*10 ,10)))
      testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,0,sigDown,sigUp))
      #testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,0,-0.1,0.1))
    testSig_ext.append(RooExtendPdf('extSig'+fitName,'ext'+fitName,sig,testSigNorms[-1]))
    testModels.append(RooAddPdf('model'+fitName,'model'+fitName,RooArgList(testSig_ext[-1],testPdfs_ext[-1])))
    if verbose:
      print 'model'+fitName
      testModels[-1].Print()

  testModelsDict = dict(zip(testFuncs,testModels))
  testBkgNormsDict = dict(zip(testFuncs,testBkgNorms))
  testSigNormsDict = dict(zip(testFuncs,testSigNorms))


  # prep the outputs
  if not os.path.isdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/biasStudy'): os.mkdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/biasStudy')

  if cfl.injectedSignalSize:
    biasToysName = 'biasToysInj'
  else:
    biasToysName = 'biasToys'
  outName = '_'.join([biasToysName,tev,lepton,'cat'+cat,genFunc,mass,'job'+str(job)])+'.root'
  outName = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/biasStudy/'+outName
  outFile = TFile(outName, 'RECREATE')
  tree = TTree('toys','toys')
  #makeToyStucts()


  #set up branches
  toyDataStruct = getattr(sys.modules[__name__], 'TOYDATA')()
  #toyDataStruct = TOYDATA()
  tree.Branch('toyData', toyDataStruct, 'totalData/I:sigWindowData:sigWindowInject')
  structDict = {}
  for func in testFuncs:
    structDict[func]= getattr(sys.modules[__name__], func.upper())()
    if func in ['GaussBern3']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['GaussBern4']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['GaussBern5']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:paramP5:paramP5Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Pow']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramAlpha:paramAlphaErr:paramBeta:paramBetaErr:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Exp2','PowDecay','Dijet']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Laguerre2']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramK:paramKErr:paramP1:paramP1Err:paramP2:paramP2Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Laguerre3']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramK:paramKErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['PowLog','ExpSum','ExpSum2','PowDecayExp','PowExpSum']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['TripExpSum','TripPowSum']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:paramP5:paramP5Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['TripExpSumv2']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:paramP5:paramP5Err:paramP6:paramP6Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Laurent']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Hill','Weibull']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramK:paramKErr:paramL:paramLErr:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Gamma']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramGamma:paramGammaErr:paramBeta:paramBetaErr:paramMu:paramMuErr:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    else:
      raise Exception('{0} is not defined for structDicts'.format(func))

  #structDict = dict(zip(testFuncs,[GaussBern3Struct,GaussBern4Struct,GaussBern5Struct]))

  r = TRandom3(1024+31*job)
  RooRandom.randomGenerator().SetSeed(1024+31*job)

  if myGenFunc == 'boot':
    np.random.seed(1024+31*job)
    if lepton == 'mu':
      toyData_init = genfromtxt('m_mumugamma.csv')
    elif lepton =='el':
      toyData_init = genfromtxt('m_eegamma.csv')


  ############################
  # time to throw some toys! #
  ############################

  for i in range(1,trials+1):
    if cfl.rootrace:
      RooTrace.dump()
      raw_input()
    print 'doing trial:',i

    #genBkgYield = r.Poisson(data.numEntries())
    genBkgYield = data.numEntries()
    print'bg yield'
    #toyData = genFit.generate(RooArgSet(mzg),genBkgYield)

    if myGenFunc == 'boot':
      toyData_np_int = np.random.randint(0, high=genBkgYield, size=genBkgYield)
      toyData_np = []
      for j in toyData_np_int:
        toyData_np.append(toyData_init[j])
      #data_argS = RooArgSet(mzg_boot)
      data_argS = RooArgSet(mzg,weight)
      toyData = RooDataSet('toyData','toyData',data_argS,'Weight')
      #print toyData_np
      #raw_input()
      for j in toyData_np:
        #mzg_boot.setVal(j)
        mzg.setVal(j)
        toyData.add(data_argS,1)
      #toyData.Print()
      #raw_input()
    else:
      toyData = myGenFunc.generate(RooArgSet(mzg),genBkgYield,RooFit.Verbose(True), RooFit.AllBinned())
    #toyData = data.generate(RooArgSet(mzg),genBkgYield,RooFit.Verbose(True), RooFit.AllBinned())
    bkg_est = toyData.sumEntries('1',sigRangeName)
    if cfl.injectedSignalSize:
      print 'injecting signal!!!!!'
      print injectedSignalSize
      if myGenFunc == 'boot':
        #toySignal = sig.generate(RooArgSet(mzg_boot),injectedSignalSize,RooFit.Verbose(True), RooFit.AllBinned())
        toySignal = sig.generate(RooArgSet(mzg),injectedSignalSize,RooFit.Verbose(True), RooFit.AllBinned())
      else:
        toySignal = sig.generate(RooArgSet(mzg),injectedSignalSize,RooFit.Verbose(True), RooFit.AllBinned())
      #toySignal.Print()
      toyData.append(toySignal)
      #toyData.Print()
      #raw_input()
    print'toy made'
    if verbose: print 'bkg_est',bkg_est

    for func in testFuncs:
      testSigNormsDict[func].setVal(injectedSignalSize)
      testBkgNormsDict[func].setVal(bkg_est)
      #testBkgNormsDict[func].setVal(-0.1)

      #nll = testModelsDict[func].createNLL(toyData,RooFit.Extended())
      #m = RooMinuit(nll)
      #m.migrad()
      #resMigrad = m.save()
      #m.hesse()
      #resHesse = m.save()
      #m.setPrintLevel(-100000)
      #m.minos()
      #res = m.save()

      RooMsgService.instance().setGlobalKillBelow(RooFit.ERROR)
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.InitialHesse(True),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE),RooFit.Minos(RooArgSet(testBkgNormsDict[func],testSigNormsDict[func])))
      #testModelsDict[func].fitTo(toyData,RooFit.PrintLevel(-1000000),RooFit.InitialHesse(True),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE),RooFit.Minos(True))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.InitialHesse(True),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE),RooFit.Minos(True))
      res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-10000000),RooFit.Strategy(1),RooFit.SumW2Error(True),RooFit.Minos(True))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE),RooFit.Minos(RooArgSet(testBkgNormsDict[func],testSigNormsDict[func])))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE))

      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE),RooFit.Minos(True))

      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.NumCPU(6),RooFit.SumW2Error(kTRUE),RooFit.Minos(True))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.InitialHesse(True),RooFit.Strategy(1),RooFit.SumW2Error(kTRUE), RooFit.Minos(True))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.InitialHesse(True),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE), RooFit.Minos(True),RooFit.Minimizer("Minuit"))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE), RooFit.Minimizer("Minuit"))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(2),RooFit.SumW2Error(kTRUE))
      #res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1000000),RooFit.Strategy(1),RooFit.SumW2Error(kTRUE), RooFit.Minimizer("Minuit"),RooFit.Minos(RooArgSet(testBkgNormsDict[func],testSigNormsDict[func])))

      statusAll = res.status()
      try:
        statusMIGRAD = resMigrad.status()
      except:
        statusMIGRAD = 0
      try:
        statusHESSE = resHesse.status()
      except:
        statusHESSE = 0
      numInvalidNLL = res.numInvalidNLL()
      edm = res.edm()
      minNll = res.minNll()
      covQual = res.covQual()

      if verbose:
        print 'statusAll', statusAll
        print 'statusMIGRAD', statusMIGRAD
        print 'statusHESSE', statusHESSE
        print 'numInvalidNLL', numInvalidNLL
        print 'edm', edm
        print 'minNll', minNll
        print 'covQual', covQual
        print 'yieldBkg', testBkgNormsDict[func].getVal()
        print 'yieldSig', testSigNormsDict[func].getVal()
        testModelsDict[func].getParameters(toyData).Print('v')

      selection = '_'.join([func,tev,lepton,'cat'+cat])
      structDict[func].yieldBkg = testBkgNormsDict[func].getVal()
      structDict[func].yieldBkgErr = testBkgNormsDict[func].getError()
      structDict[func].yieldSig = testSigNormsDict[func].getVal()
      structDict[func].yieldSigErr = testSigNormsDict[func].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5']:
        structDict[func].paramSigma = testModelsDict[func].getParameters(toyData)['sigma'+selection].getVal()
        structDict[func].paramSigmaErr = testModelsDict[func].getParameters(toyData)['sigma'+selection].getError()
        structDict[func].paramStep = testModelsDict[func].getParameters(toyData)['step'+selection].getVal()
        structDict[func].paramStepErr = testModelsDict[func].getParameters(toyData)['step'+selection].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5','Exp2','Dijet','PowDecay','ExpSum','ExpSum2','PowLog','Laurent','TripExpSum','PowDecayExp','PowExpSum','Laguerre2','Laguerre3']:
        structDict[func].paramP1 = testModelsDict[func].getParameters(toyData)['p1'+selection].getVal()
        structDict[func].paramP1Err = testModelsDict[func].getParameters(toyData)['p1'+selection].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5','Exp2','Dijet','PowDecay','ExpSum','ExpSum2','PowLog','TripExpSum','PowDecayExp','PowExpSum','Laguerre2','Laguerre3']:
        structDict[func].paramP2 = testModelsDict[func].getParameters(toyData)['p2'+selection].getVal()
        structDict[func].paramP2Err = testModelsDict[func].getParameters(toyData)['p2'+selection].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5','ExpSum','ExpSum2','PowLog','TripExpSum','PowDecayExp','PowExpSum','Laguerre3']:
        structDict[func].paramP3 = testModelsDict[func].getParameters(toyData)['p3'+selection].getVal()
        structDict[func].paramP3Err = testModelsDict[func].getParameters(toyData)['p3'+selection].getError()
      if func in ['GaussBern4','GaussBern5','TripExpSum']:
        structDict[func].paramP4 = testModelsDict[func].getParameters(toyData)['p4'+selection].getVal()
        structDict[func].paramP4Err = testModelsDict[func].getParameters(toyData)['p4'+selection].getError()
      if func in ['GaussBern5','TripExpSum']:
        structDict[func].paramP5 = testModelsDict[func].getParameters(toyData)['p5'+selection].getVal()
        structDict[func].paramP5Err = testModelsDict[func].getParameters(toyData)['p5'+selection].getError()
      if func in ['Pow']:
        structDict[func].paramAlpha = testModelsDict[func].getParameters(toyData)['alpha'+selection].getVal()
        structDict[func].paramAlphaErr = testModelsDict[func].getParameters(toyData)['alpha'+selection].getError()
        structDict[func].paramBeta = testModelsDict[func].getParameters(toyData)['beta'+selection].getVal()
        structDict[func].paramBetaErr = testModelsDict[func].getParameters(toyData)['beta'+selection].getError()
      if func in ['Laguerre2','Laguerre3']:
        structDict[func].paramK = testModelsDict[func].getParameters(toyData)['k'+selection].getVal()
        structDict[func].paramKErr = testModelsDict[func].getParameters(toyData)['k'+selection].getError()
      structDict[func].statusAll = statusAll
      structDict[func].statusMIGRAD = statusMIGRAD
      structDict[func].statusHESSE = statusHESSE
      structDict[func].numInvalidNLL = numInvalidNLL
      structDict[func].edm = edm
      structDict[func].minNll = minNll
      structDict[func].covQual = covQual

      res.IsA().Destructor(res)
      try: resHesse.IsA().Destructor(resHesse)
      except: pass
      try: resMigrad.IsA().Destructor(resMigrad)
      except: pass
      try: m.IsA().Destructor(m)
      except: pass
      try: nll.IsA().Destructor(nll)
      except: pass





    toyDataStruct.totalData = toyData.numEntries()
    toyDataStruct.sigWindowData = bkg_est
    toyDataStruct.sigWindowInject =injectedSignalSize

    if (i%plotEvery == 0) or (i == 1):
      if myGenFunc == 'boot':
        #testFrame = mzg_boot.frame()
        testFrame = mzg.frame()
      else:
        testFrame = mzg.frame()

      print binning
      toyData.plotOn(testFrame, RooFit.Binning(int(binning)), RooFit.Name('toyData'))
      for func in testFuncs:
        print func
        testModelsDict[func].plotOn(testFrame, RooFit.LineColor(FitBuilder.FitColorDict[func]), RooFit.Range('fullRange'))
      testFrame.SetMinimum(0.001)
      testFrame.Draw()
      plotDir = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/biasFits/'+lepton+'/'+func+'/'+genFunc+'/'+mass
      if not os.path.isdir(plotDir): os.makedirs(plotDir)
      toyFitsName = 'toyFits'
      if injectedSignalSize == 0: toyFitsName = toyFitsName + 'NoSig'
      else: toyFitsName = toyFitsName + 'InjSig'
      c.Print(plotDir+'/'+'_'.join([toyFitsName,suffix,lepton,tev,'cat'+cat,genFunc,'M'+mass,'job'+str(job),'trial'+str(i)])+'.pdf')

    tree.Fill()
    toyData.IsA().Destructor(toyData)

  outFile.cd()
  tree.Write()
  outFile.Close()

  print 'so many toys!'



if __name__=="__main__":
  args = getArgs()
  print args
  #if len(sys.argv) == 1:
  #  doBiasStudy(tev = cfl.tevList[0], lepton = cfl.leptonList[0], cat = cfl.catListSmall[0], genFunc = cfl.testFuncs[1], mass = cfl.massList[0])
  #else:
  #  doBiasStudy(*sys.argv[1:])
  doBiasStudy(args.tev, args.lepton, str(args.cat),args.genFunc, str(args.mass), args.trials, args.job, args.plotEvery)


