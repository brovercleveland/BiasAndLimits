#!/usr/bin/env python
import os
import sys
import shutil

def produceLimits(inputFolder = None, outPutFolder = None, mass = '125.0'):
  fullCombo = True
  byParts = False
  MVATest = False
  suffix = 'Proper'

  if inputFolder == None:
    inputFolder = 'outputDir/'+suffix+'/'+mass+'/'
  if outPutFolder == None:
    outPutFolder = 'outputDir/'+suffix+'/'+mass+'/limitOutput/'
  if not os.path.isdir(outPutFolder): os.mkdir(outPutFolder)

  shutil.copy('outputDir/'+suffix+'/'+'CardBackground_'+suffix+'.root',outPutFolder+'CardBackground_'+suffix+'.root')



  leptonList = ['mu','el']
  yearList = ['2012','2011']
  catListBig = ['1','2','3','4','5','6','7','8','9']
  catListSmall = ['1','2','3','4','5']

  if fullCombo:
    cardNames = ''
    #comboName = outPutFolder+'_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    #outputName = outPutFolder+'_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    comboName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
    outputName = '_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    for year in yearList:
      if MVATest and year == '2012': catList = catListBig
      else: catList = catListSmall
      for lepton in leptonList:
        for cat in catList:
          if year is '2011' and cat is '5' and lepton is 'mu': continue
          elif year is '2011' and cat is '5' and lepton is 'el': lepton='all'
          cardNames = cardNames+' '+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass,suffix])+'.txt'
          sigFileName = '_'.join(['SignalOutput',lepton,year,'cat'+cat,mass])+'.root'
          if not os.path.isfile(outPutFolder+sigFileName):
             shutil.copy(inputFolder+sigFileName,outPutFolder+sigFileName)
          else:
            print 'using existing', sigFileName
    os.chdir(inputFolder)
    print 'making combined cards'
    print 'combineCards.py '+cardNames+' > '+comboName
    os.system('combineCards.py '+cardNames+' > '+comboName)
    shutil.move(comboName, 'limitOutput/'+comboName)
    os.chdir('limitOutput')
    #print 'running limit software, M:',mass
    #os.system('combine -M Asymptotic '+comboName+' > '+outputName)
    #os.system('combine -M ProfileLikelihood '+comboName+' > '+outputName)

if __name__ == "__main__":
  print sys.argv
  if len(sys.argv)<2:
    produceLimits()
  elif len(sys.argv) is 2:
    produceLimits('testCards/','',str(sys.argv[1]))
  elif len(sys.argv) is 4:
    produceLimits(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))
  else:
    'you did something wrong'
