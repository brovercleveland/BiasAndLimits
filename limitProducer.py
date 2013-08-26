#!/usr/bin/env python
import os

fullCombo = True
byParts = False

leptonList = ['mu']
yearList = ['2012']
catList = ['1','2']
massList = ['120.0']

if fullCombo:
  for mass in massList:
    cardNames = ''
    comboName = 'testCards/'+'_'.join(['hzg','FullCombo','M'+mass])+'.txt'
    outputName = 'limitOutputs/'+'_'.join(['Output','FullCombo','M'+mass])+'.txt'
    for year in yearList:
      for lepton in leptonList:
        for cat in catList:
          cardNames = cardNames+' testCards/'+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass])+'.txt'
    print 'making combined cards'
    print 'combineCards.py '+cardNames+' > '+comboName
    os.system('combineCards.py '+cardNames+' > '+comboName)
    print 'running limit software'
    os.system('combine -M Asymptotic '+comboName+' > '+outputName)
