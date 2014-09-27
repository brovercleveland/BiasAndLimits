#!/usr/bin/env python
import sys
from toyStructs import makeToyStucts
makeToyStucts()
from ROOT import *
import numpy as np
import configLimits as cfl

gROOT.SetBatch()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.x RooStepBernstein.cxx+')
gROOT.ProcessLine('.x RooGaussStepBernstein.cxx+')
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

colors = [kRed,kBlue,kGreen]

verbose = cfl.verbose

doMVA = cfl.doMVA

allBiasFits= cfl.allBiasFits# Turn on extra fits used in bias studies

YR = cfl.YR

sigFit = cfl.sigFit

highMass = cfl.highMass

testFuncs = cfl.testFuncs

suffix = cfl.suffix

def doBiasStudy(tev = '8TeV', lepton = 'mu', cat = '1', genFunc = 'GaussExp', mass = '125', trials = 5, job = 0, plotEvery = 1):
  #get all the starting objects
  c = TCanvas("c","c",0,0,500,400)
  c.cd()
  print YR
  print suffix

  rooWsFile = TFile('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix.rstrip('_Cut')+'.root','r')
  myWs = rooWsFile.Get('ws')
  sigRangeName = '_'.join(['range',lepton,tev,'cat'+cat,'M'+mass])

  # get the x-axis
  mzg = myWs.var('CMS_hzg_mass')
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
  genFitName = '_'.join([genFunc,tev,lepton,'cat'+cat])
  print genFitName
  genFit = myWs.pdf(genFitName)
  if verbose:
    print genFitName
    genFit.Print()

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
  for func in testFuncs:
    fitName = '_'.join([func,tev,lepton,'cat'+cat])
    if func is genFunc:
      testPdfs.append(genFit)
    else:
      testPdfs.append(myWs.pdf(fitName))
    if verbose:
      print fitName
      testPdfs[-1].Print()
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
  ColorDict = dict(zip(testFuncs,colors))


  # prep the outputs
  outName = '_'.join(['biasToys',tev,lepton,'cat'+cat,genFunc,mass,'job'+str(job)])+'.root'
  outFile = TFile(outName, 'RECREATE')
  tree = TTree('toys','toys')
  #makeToyStucts()


  #set up branches
  toyDataStruct = getattr(sys.modules[__name__], 'TOYDATA')()
  #toyDataStruct = TOYDATA()
  tree.Branch('toyData', toyDataStruct, 'totalData/I:sigWindowData')
  genStruct = GEN()
  tree.Branch('gen',genStruct, 'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
  for func in testFuncs:
    if func is 'GaussBern3':
      from ROOT import GAUSSBERN3
      GaussBern3Struct = GAUSSBERN3()
      tree.Branch('GaussBern3',GaussBern3Struct,'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    if func is 'GaussBern4':
      from ROOT import GAUSSBERN4
      GaussBern4Struct = GAUSSBERN4()
      tree.Branch('GaussBern4',GaussBern4Struct,'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')
    if func is 'GaussBern5':
      from ROOT import GAUSSBERN5
      GaussBern5Struct = GAUSSBERN5()
      tree.Branch('GaussBern5',GaussBern5Struct,'yieldBkg/D:yieldBkgErr:yieldSig:yieldSigErr:paramSigma:paramSigmaErr:paramStep:paramStepErr:paramP1:paramP1Err:paramP2:paramP2Err:paramP3:paramP3Err:paramP4:paramP4Err:paramP5:paramP5Err:edm:minNll:statusAll/I:statusMIGRAD:statusHESSE:covQual:numInvalidNLL')

  structDict = dict(zip(testFuncs,[GaussBern3Struct,GaussBern4Struct,GaussBern5Struct]))

  r = TRandom3(1024+31*job)
  RooRandom.randomGenerator().SetSeed(1024+31*job)

  """

  ############################
  # time to throw some toys! #
  ############################

  for i in range(0,trials):
    print 'doing trial:',i

    genBkgYield = r.Poisson(data.numEntries())
    toyData = genFit.generate(RooArgSet(mzg),genBkgYield)
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

      res = testModelsDict[func].fitTo(toyData,RooFit.Save(),RooFit.PrintLevel(-1))

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

      suffix = '_'.join([func,tev,lepton,'cat'+cat])
      structDict[func].yieldBkg = testBkgNormsDict[func].getVal()
      structDict[func].yieldBkgErr = testBkgNormsDict[func].getError()
      structDict[func].yieldSig = testSigNormsDict[func].getVal()
      structDict[func].yieldSigErr = testSigNormsDict[func].getError()
      if func in ['GaussBern3','GaussBern4','GaussBern5']:
        structDict[func].paramSigma = testModelsDict[func].getParameters(toyData)['sigma'+suffix].getVal()
        structDict[func].paramSigmaErr = testModelsDict[func].getParameters(toyData)['sigma'+suffix].getError()
        structDict[func].paramStep = testModelsDict[func].getParameters(toyData)['step'+suffix].getVal()
        structDict[func].paramStepErr = testModelsDict[func].getParameters(toyData)['step'+suffix].getError()
        structDict[func].paramP1 = testModelsDict[func].getParameters(toyData)['p1'+suffix].getVal()
        structDict[func].paramP1Err = testModelsDict[func].getParameters(toyData)['p1'+suffix].getError()
        structDict[func].paramP2 = testModelsDict[func].getParameters(toyData)['p2'+suffix].getVal()
        structDict[func].paramP2Err = testModelsDict[func].getParameters(toyData)['p2'+suffix].getError()
        structDict[func].paramP3 = testModelsDict[func].getParameters(toyData)['p3'+suffix].getVal()
        structDict[func].paramP3Err = testModelsDict[func].getParameters(toyData)['p3'+suffix].getError()
      if func in ['GaussBern4','GaussBern5']:
        structDict[func].paramP4 = testModelsDict[func].getParameters(toyData)['p4'+suffix].getVal()
        structDict[func].paramP4Err = testModelsDict[func].getParameters(toyData)['p4'+suffix].getError()
      if func in ['GaussBern5']:
        structDict[func].paramP5 = testModelsDict[func].getParameters(toyData)['p5'+suffix].getVal()
        structDict[func].paramP5Err = testModelsDict[func].getParameters(toyData)['p5'+suffix].getError()
      structDict[func].statusAll = statusAll
      structDict[func].statusMIGRAD = statusMIGRAD
      structDict[func].statusHESSE = statusHESSE
      structDict[func].numInvalidNLL = numInvalidNLL
      structDict[func].edm = edm
      structDict[func].minNll = minNll
      structDict[func].covQual = covQual



    toyDataStruct.totalData = toyData.numEntries()
    toyDataStruct.sigWindowData = bkg_est

    if i%plotEvery is 0:
      testFrame = mzg.frame()
      toyData.plotOn(testFrame)
      for func in testFuncs:
        testModelsDict[func].plotOn(testFrame, RooFit.LineColor(ColorDict[func]), RooFit.Range('fullRange'))
      testFrame.Draw()
      c.Print('debugPlots/'+'_'.join(['toyFits',lepton,tev,'cat'+cat,genFunc,'M'+mass,'job'+str(job),'trial'+str(i)])+'.pdf')

    tree.Fill()

  outFile.cd()
  tree.Write()
  outFile.Close()

  print 'so many toys!'
  """



if __name__=="__main__":
  doBiasStudy(tev = cfl.tevList[0], lepton = cfl.leptonList[0], cat = cfl.catListSmall[0], genFunc = cfl.testFuncs[0], mass = cfl.massList[0])


