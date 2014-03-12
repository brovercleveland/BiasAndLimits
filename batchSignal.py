#!/usr/bin/env python
import os

suffix = 'Proper'

leptonList = ['mu','el']
tevList = ['8TeV','7TeV']
catListBig = ['1','2','3','4','5','6','7','8','9']
catListSmall = ['1','2','3','4','5']
for lepton in leptonList:
  for tev in tevList:
    for cat in catListSmall:
      if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
      elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
      else: myLepton = lepton
      cardName = '_'.join(['hzg',myLepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
      consub = open('submit.cmd','w')
      consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/limitExe.py
Arguments               = {0} {1} {2} {3}
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (Disk >= DiskUsage) && ((Memory * 1024) >= ImageSize) && (HasFileTransfer)
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = limitOutput/res/job_{0}_{2}.out
Error                   = limitOutput/res/job_{0}_{2}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = limitFiles.tgz
Queue
      '''.format(mass,suffix,cardName,outPutFolder+'/limitOutput/'))
      consub.close()

      os.system('condor_submit submit.cmd')
      os.system('rm submit.cmd')


