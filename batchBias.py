#!/usr/bin/env python
import os
import configLimits as cfl

suffix = cfl.suffix
doMVA = cfl.doMVA
highMass = cfl.highMass
YR = cfl.YR

leptonList = cfl.leptonList
tevList = cfl.tevList
catListBig = cfl.catListBig
catListSmall = cfl.catListSmall

testFuncs = cfl.testFuncs
massList = cfl.massList
trials = cfl.trials
plotEvery = cfl.plotEvery
jobs = cfl.jobs

for lepton in leptonList:
  for tev in tevList:
    if highMass: catList = ['0']
    elif doMVA and tev == '8TeV': catList = catListBig
    else: catList = catListSmall
    for cat in catList:
      if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
      elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
      else: myLepton = lepton
      for mass in massList:
        for func in testFuncs:
          for job in range(jobs):
            consub = open('submit.cmd','w')
            consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/biasStudy_toyMaker.py
Arguments               = {0} {1} {2} {3} {4} {5} {6} {7}
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (Disk >= DiskUsage) && ((Memory * 1024) >= ImageSize) && (HasFileTransfer)
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = biasRes/job_{0}_{1}_{2}_{3}_{4}_{6}_{8}.out
Error                   = biasRes/job_{0}_{1}_{2}_{3}_{4}_{6}_{8}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = rooFitBuilder.py, CMSStyle.C, RooStepBernstein.cxx, RooGaussStepBernstein.cxx, RooStepBernstein.h, RooGaussStepBernstein.h, configLimits.py, toyStructs.py
Queue
            '''.format(tev,myLepton,cat,func,mass,trials,job,plotEvery,suffix))
            consub.close()

            os.system('condor_submit submit.cmd')
            os.system('rm submit.cmd')


