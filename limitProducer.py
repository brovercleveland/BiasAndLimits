#!/usr/bin/env python
import os
import sys
import shutil
import time

def produceLimits(inputFolder = None, outPutFolder = None, mass = '125.0'):
  fullCombo = True
  byParts = False
  MVATest = False
  suffix = 'Proper'

  owd = os.getcwd()
  if inputFolder == None:
    inputFolder = 'outputDir/'+suffix+'/'+mass+'/'
  if outPutFolder == None:
    outPutFolder = 'outputDir/'+suffix+'/'+mass+'/limitOutput/'
  if not os.path.exists(outPutFolder):
    os.mkdir(outPutFolder)

  shutil.copy('outputDir/'+suffix+'/'+'CardBackground_'+suffix+'.root',inputFolder+'CardBackground_'+suffix+'.root')



  leptonList = ['mu','el']
  tevList = ['8TeV','7TeV']
  catListBig = ['1','2','3','4','5','6','7','8','9']
  catListSmall = ['1','2','3','4','5']

  if fullCombo:
    cardNames = ''
    #comboName = outPutFolder+'_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    #outputName = outPutFolder+'_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    comboName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    outputName = '_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    for tev in tevList:
      if MVATest and tev == '8TeV': catList = catListBig
      else: catList = catListSmall
      for lepton in leptonList:
        for cat in catList:
          if tev is '7TeV' and cat is '5' and lepton is 'mu': continue
          elif tev is '7TeV' and cat is '5' and lepton is 'el': lepton='all'
          cardNames = cardNames+' '+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
          sigFileName = '_'.join(['SignalOutput',lepton,tev,'cat'+cat,mass])+'.root'
    os.chdir(inputFolder)
    print 'making combined cards'
    print 'combineCards.py '+cardNames+' > '+comboName
    os.system('combineCards.py '+cardNames+' > '+comboName)
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
    massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
     '124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
     '125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
     '127.0','127.5','128.0','128.5','129.0','129.5','130.0',
     '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
     '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
     '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
     '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
    for mass in massList:
      produceLimits(mass = mass)
  else:
    'you did something wrong, syntax has been changed'
