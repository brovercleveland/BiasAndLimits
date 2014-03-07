#!/usr/bin/env python
import os

suffix = 'Proper'
mode = 'noCombo'
#mode = 'Combo'


#massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0',
# '125.5','126.0','126.5','127.0','127.5','128.0','128.5','129.0','129.5','130.0',
# '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
# '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
# '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
# '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
massList = ['125.0']

for mass in massList:
  outPutFolder = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'/'+mass
  os.chdir(outPutFolder)
  if not os.path.isdir('limitOutput/res'):
    os.mkdir('limitOutput/res')
  os.system('rm limitOutput/res/*')

  os.system('tar cvzf limitFiles.tgz Signal* Card* hzg*')

  consub = open('submit.cmd','w')
  consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = /tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/limitExe.py
Arguments               = {0} {1} {2}
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
'''.format(mass,suffix,mode))
  consub.close()

  os.system('condor_submit submit.cmd')
  os.system('rm submit.cmd')


