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
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/signalFits.py
Arguments               = --lepton {0} --tev {1} --cat {2} --suffix {3} --cores {5}
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (Disk >= DiskUsage) && ((Memory * 1024) >= ImageSize) && (HasFileTransfer)
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = signalRes/job_{0}_{1}_{2}_{3}_{4}_{6}.out
Error                   = signalRes/job_{0}_{1}_{2}_{3}_{4}_{6}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = rooFitBuilder.py, CMSStyle.C, RooStepBernstein.cxx, RooGaussStepBernstein.cxx, RooStepBernstein.h, RooGaussStepBernstein.h, configLimits.py
Queue
      '''.format(myLepton,tev,cat,suffix,YR,12,sigFit))
      consub.close()

      os.system('condor_submit submit.cmd')
      os.system('rm submit.cmd')


