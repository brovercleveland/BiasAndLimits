#!/usr/bin/env python
import os


massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0',
 '125.5','126.0','126.5','127.0','127.5','128.0','128.5','129.0','129.5','130.0',
 '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
 '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
 '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
 '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']

leptonList = ['mu','el']
yearList = ['2012','2011']
catList = ['1','2','3','4','5']

os.chdir('limitOutputs')

for mass in massList:
  cardNames = []
  sigNames = []
  dataName = '../testCards/testCardBackground.root'
  for lepton in leptonList:
    for cat in catList:
      for year in yearList:
        if year is '2011' and cat is '5' and lepton is 'mu': continue
        elif year is '2011' and cat is '5' and lepton is 'el': lepton='all'
        cardNames.append('../testCards/'+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass])+'.txt')
        sigNames.append('../testCards/'+'_'.join(['SignalOutput',lepton,year,'cat'+cat,mass])+'.root')

  inputFiles = ', '.join(cardNames+sigNames+[dataName,'../limitProducer.py'])
  consub = open('submit.cmd','w')
  consub.write('''
Universe                = vanilla
Notify_user             = brian.pollack@cern.ch
Notification            = Error
Executable              = ../limitExe.sh
Arguments               = {0}
Rank                    = Mips
Requirements            = (OpSys == "LINUX") && (Disk >= DiskUsage) && ((Memory * 1024) >= ImageSize) && (HasFileTransfer)
+LENGTH                 = "LONG"
GetEnv                  = True
Input                   = /dev/null
Output                  = ../res/job_{0}.out
Error                   = ../res/job_{0}.err
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = {1}
Queue
'''.format(mass,inputFiles))
  consub.close()

  os.system('condor_submit submit.cmd')
  os.system('rm submit.cmd')


