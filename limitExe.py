#!/usr/bin/env python
import os
import sys

os.chdir(os.environ.get('_CONDOR_SCRATCH_DIR'))
os.system('tar xvzf limitFiles.tgz')

mass=sys.argv[1]
suffix=sys.argv[2]
if sys.argv[3].lower() == 'combo':
  cardName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
  outputName = 'limitOutput/'+'_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
  print 'running limitProducer, FullCombo,  mass: {0}'.format(mass)
  os.system('combine -M Asymptotic '+cardName+' > '+outputName)
else:
  leptonList = ['mu','el']
  yearList = ['2012','2011']
  catListBig = ['1','2','3','4','5','6','7','8','9']
  catListSmall = ['1','2','3','4','5']
  for lepton in leptonList:
    for year in yearList:
      for cat in catListSmall:
        cardName = '_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass,suffix])+'.txt'
        outputName = 'limitOutput/'+'_'.join(['Output',lepton,year,'cat'+cat,'M'+mass,suffix])+'.txt'
        print 'running limitProducer, {1}, {2}, cat{3}, mass: {0}'.format(mass,lepton,year,cat)
        os.system('combine -M Asymptotic '+cardName+' > '+outputName)



print 'Done'
