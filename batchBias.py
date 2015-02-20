#!/usr/bin/env python
import os
import configLimits as cfl

suffix = cfl.suffixPostFix
doMVA = cfl.doMVA
highMass = cfl.highMass
YR = cfl.YR

leptonList = cfl.leptonList
tevList = cfl.tevList
catListBig = cfl.catListBig
catListSmall = cfl.catListSmall

genFuncs = cfl.genFuncs
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
        for func in genFuncs:
          for job in range(jobs):
            consub = open('submit.cmd','w')
            consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = biasStudy_toyMaker.py
Arguments               = --tev {0} --lepton {1} --cat {2} --genFunc {3} --mass {4} --trials {5} --job {6} --plotEvery {7}
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (Disk >= DiskUsage) && ((Memory * 1024) >= ImageSize) && (HasFileTransfer) && (machine!="ttnode0008")
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = biasRes/job_{0}_{1}_{2}_{3}_{4}_{6}_{8}.out
Error                   = biasRes/job_{0}_{1}_{2}_{3}_{4}_{6}_{8}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = rooFitBuilder.py, CMSStyle.C, RooStepBernstein.cxx, RooGaussStepBernstein.cxx, RooStepBernstein.h, RooGaussStepBernstein.h, configLimits.py, toyStructs.py, biasStudy_toyMaker.py
Queue
            '''.format(tev,myLepton,cat,func,mass,trials,job,plotEvery,suffix))
            consub.close()

            os.system('condor_submit submit.cmd')
            os.system('rm submit.cmd')


