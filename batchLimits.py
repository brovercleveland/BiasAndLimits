#!/usr/bin/env python
import os

suffix = '03-11-14_Cats'
#mode = 'noCombo'
mode = 'Combo'
doMVA = True

massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
 '124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
 '125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
 '127.0','127.5','128.0','128.5','129.0','129.5','130.0',
 '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
 '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
 '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
 '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
#massList = ['130.5']
#massList = ['130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
# '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0']

for mass in massList:
  outPutFolder = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'/'+mass
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
  else:
    leptonList = ['mu','el']
    tevList = ['8TeV','7TeV']
    catListBig = ['1','2','3','4','5','6','7','8','9']
    catListSmall = ['1','2','3','4','5']
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


