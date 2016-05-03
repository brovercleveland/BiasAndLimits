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
  os.system('combine {1} -M HybridNew --freq --grid=grid.root -v9 -m {0} --expectedFromGrid='.format(mass,cardName))
  os.system('combine {1} -M HybridNew -m {0} --rMin={3} --rMax={4} --freq --fullBToys -s -1 -T 1000 -i 5 --saveToys --saveHybridResult --clsAcc 0 -v9 --singlePoint={2}'.format(mass,cardName,point,rMin,rMax))
