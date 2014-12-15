#!/usr/bin/env python
import os
import sys
import shutil
import time
import configLimits as cfl

def produceLimits(inputFolder = None, outPutFolder = None, mass = '125.0'):
  fullCombo = cfl.fullCombo
  byParts = cfl.byParts
  doMVA = cfl.doMVA

  suffix = cfl.suffixPostFix

  leptonList = cfl.leptonList
  tevList = cfl.tevList
  noCats = cfl.noCats

  YR = cfl.YR
  sigFit = cfl.sigFit
  highMass = cfl.highMass

  if noCats:
    catListBig = ['0']
    catListSmall = ['0']
  else:
    catListBig = cfl.catListBig[1:]
    catListSmall = cfl.catListSmall[1:]


  owd = os.getcwd()
  if inputFolder == None:
    inputFolder = 'outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'
  if outPutFolder == None:
    outPutFolder = 'outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/limitOutput/'
  if not os.path.exists(outPutFolder):
    os.mkdir(outPutFolder)

  shutil.copy('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+'CardBackground_'+suffix+'.root',inputFolder+'CardBackground_'+suffix+'.root')




  if fullCombo:
    cardNames = ''
    cardNames7TeV = ''
    cardNames8TeV = ''
    #comboName = outPutFolder+'_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    #outputName = outPutFolder+'_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    comboName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    comboName7TeV = '_'.join(['hzg','7TeVCombo','M'+mass,suffix])+'.txt'
    comboName8TeV = '_'.join(['hzg','8TeVCombo','M'+mass,suffix])+'.txt'
    outputName = '_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    for tev in tevList:
      if doMVA and tev == '8TeV': catList = catListBig
      if highMass and tev == '7TeV': continue
      else: catList = catListSmall
      for lepton in leptonList:
        for cat in catList:
          if tev is '7TeV' and cat is '5' and lepton is 'mu': continue
          elif tev is '7TeV' and cat is '5' and lepton is 'el': lepton='all'
          cardNames = cardNames+' '+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
          if tev == '7TeV':
            cardNames7TeV = cardNames7TeV+' '+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
          elif tev == '8TeV':
            cardNames8TeV = cardNames8TeV+' '+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
    os.chdir(inputFolder)
    print 'making combined cards'
    print 'combineCards.py '+cardNames+' > '+comboName
    os.system('combineCards.py '+cardNames+' > '+comboName)
    if not highMass: os.system('combineCards.py '+cardNames7TeV+' > '+comboName7TeV)
    os.system('combineCards.py '+cardNames8TeV+' > '+comboName8TeV)
    #os.chdir('limitOutput')
    #print 'running limit software, M:',mass
    #os.system('combine -M Asymptotic '+comboName+' > '+outputName)
    #os.system('combine -M ProfileLikelihood '+comboName+' > '+outputName)
    os.chdir(owd)

if __name__ == "__main__":
  print sys.argv
  if len(sys.argv)<2:
    produceLimits()
  elif len(sys.argv) is 2 and str(sys.argv[1]).lower() != 'all':
    produceLimits(mass = str(sys.argv[1]))
  elif len(sys.argv) is 2 and str(sys.argv[1]).lower() == 'all':
    massList = cfl.massListBig
    for mass in massList:
      produceLimits(mass = mass)
  else:
    'you did something wrong, syntax has been changed'
