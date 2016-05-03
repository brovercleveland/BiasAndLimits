#!/usr/bin/env python
import os
import configLimits as cfl

suffix = cfl.suffixPostFix
mode = cfl.mode
doMVA = cfl.doMVA

#massList = cfl.massListBig
massList = ['1200.0']

YR = cfl.YR

sigFit = cfl.sigFit

syst = cfl.syst
if cfl.method == 'CLs':
  limExe = 'limitExeCLs.py'
else:
  limExe = 'limitExe.py'

for mass in massList:
  outPutFolder = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass
  os.chdir(outPutFolder)
  os.system('hadd -f grid.root higgsCombineTest.*')
