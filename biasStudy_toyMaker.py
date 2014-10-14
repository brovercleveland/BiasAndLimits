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

suffix = cfl.suffix

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



  rooWsFile = TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix.rstrip('_Cut')+'.root','r')
  myWs = rooWsFile.Get('ws')
  sigRangeName = '_'.join(['range',lepton,tev,'cat'+cat,'M'+mass])

  # get the x-axis
  mzg = myWs.var('CMS_hzg_mass')
  binning = (mzg.getMax()-mzg.getMin())/4
  if verbose:
    mzg.Print()
    print sigRangeName, mzg.getMin(sigRangeName), mzg.getMax(sigRangeName)


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
  myGenFunc = myWs.pdf(fitName).Clone()
  for func in testFuncs:
    fitName = '_'.join([func,tev,lepton,'cat'+cat])
    testPdfs.append(myWs.pdf(fitName))
    if verbose:
      print fitName
      testPdfs[-1].Print()
      print bkgInSigWin
      print sigRangeName
    testBkgNorms.append(RooRealVar('norm'+fitName,'norm'+fitName,bkgInSigWin,0,3*bkgInSigWin))
    testPdfs_ext.append(RooExtendPdf('ext'+fitName,'ext'+fitName,testPdfs[-1],testBkgNorms[-1],sigRangeName))
    testSigNorms.append(RooRealVar('normSig'+fitName,'normSig'+fitName,0,-100,100))
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
  outName = '_'.join(['biasToys',tev,lepton,'cat'+cat,genFunc,mass,'job'+str(job)])+'.root'
  outName = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/biasStudy/'+outName
  outFile = TFile(outName, 'RECREATE')
  tree = TTree('toys','toys')
  #makeToyStucts()


  #set up branches
  toyDataStruct = getattr(sys.modules[__name__], 'TOYDATA')()
  #toyDataStruct = TOYDATA()
  tree.Branch('toyData', toyDataStruct, 'totalData/I:sigWindowData')
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
    elif func in ['Exp2','PowDecay']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['PowLog','ExpSum','PowDecayExp','PowExpSum']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['TripExpSum']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:paramP5:paramP5Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    elif func in ['Laurent']:
      tree.Branch(func,structDict[func],'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramP1:paramP1Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    else:
      raise Exception('{0} is not defined for structDicts'.format(func))

  #structDict = dict(zip(testFuncs,[GaussBern3Struct,GaussBern4Struct,GaussBern5Struct]))

  r = TRandom3(1024+31*job)
  RooRandom.randomGenerator().SetSeed(1024+31*job)



  ############################
  # time to throw some toys! #
  ############################

  for i in range(1,trials+1):
    if cfl.rootrace:
      RooTrace.dump()
      raw_input()
    print 'doing trial:',i

    genBkgYield = r.Poisson(data.numEntries())
    #toyData = genFit.generate(RooArgSet(mzg),genBkgYield)

    toyData = myGenFunc.generate(RooArgSet(mzg),genBkgYield)
    bkg_est = toyData.sumEntries('1',sigRangeName)
    if verbose: print 'bkg_est',bkg_est

    for func in testFuncs:
      testSigNormsDict[func].setVal(0)
      testBkgNormsDict[func].setVal(bkg_est)

      nll = testModelsDict[func].createNLL(toyData,RooFit.Extended())
      m = RooMinuit(nll)
      m.migrad()
      resMigrad = m.save()
      m.hesse()
      resHesse = m.save()

      res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1),RooFit.Strategy(1))

      statusAll = res.status()
      statusMIGRAD = resMigrad.status()
      statusHESSE = resHesse.status()
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
      if func in ['GaussBern3','GaussBern4','GaussBern5','Exp2','PowDecay','ExpSum','PowLog','Laurent','TripExpSum','PowDecayExp','PowExpSum']:
        structDict[func].paramP1 = testModelsDict[func].getParameters(toyData)['p1'+selection].getVal()
        structDict[func].paramP1Err = testModelsDict[func].getParameters(toyData)['p1'+selection].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5','Exp2','PowDecay','ExpSum','PowLog','TripExpSum','PowDecayExp','PowExpSum']:
        structDict[func].paramP2 = testModelsDict[func].getParameters(toyData)['p2'+selection].getVal()
        structDict[func].paramP2Err = testModelsDict[func].getParameters(toyData)['p2'+selection].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5','ExpSum','PowLog','TripExpSum','PowDecayExp','PowExpSum']:
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
      structDict[func].statusAll = statusAll
      structDict[func].statusMIGRAD = statusMIGRAD
      structDict[func].statusHESSE = statusHESSE
      structDict[func].numInvalidNLL = numInvalidNLL
      structDict[func].edm = edm
      structDict[func].minNll = minNll
      structDict[func].covQual = covQual



    toyDataStruct.totalData = toyData.numEntries()
    toyDataStruct.sigWindowData = bkg_est

    if (i%plotEvery == 0) or (i == 1):
      testFrame = mzg.frame()
      print binning
      toyData.plotOn(testFrame, RooFit.Binning(int(binning)), RooFit.Name('toyData'))
      for func in testFuncs:
        print func
        testModelsDict[func].plotOn(testFrame, RooFit.LineColor(FitBuilder.FitColorDict[func]), RooFit.Range('fullRange'))
      testFrame.Draw()
      plotDir = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/biasFits/'+lepton+'/'+genFunc+'/'+mass
      if not os.path.isdir(plotDir): os.makedirs(plotDir)
      c.Print(plotDir+'/'+'_'.join(['toyFits',suffix,lepton,tev,'cat'+cat,genFunc,'M'+mass,'job'+str(job),'trial'+str(i)])+'.pdf')

    tree.Fill()

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


