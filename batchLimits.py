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
  if not os.path.isdir('limitOutput/res'):
    os.mkdir('limitOutput/res')
  os.system('rm limitOutput/res/*')

  os.system('tar czf limitFiles.tgz Signal* Card* hzg*')
  if mode == 'Combo':
    cardName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'

    consub = open('submit.cmd','w')
    consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/{5}
Arguments               = {0} {1} {2} {3} {4}
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
  '''.format(mass,suffix,cardName,outPutFolder+'/limitOutput/',syst,limExe))
    consub.close()

    os.system('condor_submit submit.cmd')
    os.system('rm submit.cmd')
  else:
    leptonList = cfl.leptonList
    tevList = cfl.tevList
    catListBig = cfl.catListBig
    catListSmall = cfl.catListSmall
    for lepton in leptonList:
      for tev in tevList:
        if doMVA and tev == '8TeV': catList = catListBig
        else: catList = catListSmall
        for cat in catList:
          if cat == '5' and tev == '7TeV' and lepton == 'el': myLepton = 'all'
          elif cat == '5' and tev == '7TeV' and lepton == 'mu': continue
          else: myLepton = lepton
          cardName = '_'.join(['hzg',myLepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
          consub = open('submit.cmd','w')
          consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/{5}
Arguments               = {0} {1} {2} {3} {4}
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
          '''.format(mass,suffix,cardName,outPutFolder+'/limitOutput/',syst,limExe))
          consub.close()

          os.system('condor_submit submit.cmd')
          os.system('rm submit.cmd')


