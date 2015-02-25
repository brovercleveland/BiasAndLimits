#!/usr/bin/env python
import os
import configLimits as cfl

suffix = cfl.suffixPostFix
doMVA = cfl.doMVA

leptonList = cfl.leptonList
tevList = cfl.tevList
catListBig = cfl.catListBig
catListSmall = cfl.catListSmall

YR = cfl.YR
sigFit = cfl.sigFit
os.chdir('signalStage')

for lepton in leptonList:
  for tev in tevList:
    if doMVA and tev == '8TeV': catList = catListBig
    else: catList = catListSmall
    for cat in catList:
      if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
      elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
      else: myLepton = lepton
      consub = open('submit.cmd','w')
      consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = ../signalWrapper.sh
Arguments               = --lepton {0} --tev {1} --cat {2} --suffix {3} --cores {5} --batch True
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (HasFileTransfer)
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = ../signalRes/job_{0}_{1}_{2}_{3}_{4}_{6}.out
Log                     = ../signalRes/job_{0}_{1}_{2}_{3}_{4}_{6}.log
Error                   = ../signalRes/job_{0}_{1}_{2}_{3}_{4}_{6}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = ../rooFitBuilder.py, ../CMSStyle.C, ../configLimits.py, ../signalFits.py, ../outputDir/02-11-15_HighMass800_YR3_DCB/initRooFitOut_02-11-15_HighMass800.root
Queue
      '''.format(myLepton,tev,cat,suffix,YR,12,sigFit))
      consub.close()

      os.system('condor_submit submit.cmd')
      os.system('rm submit.cmd')


