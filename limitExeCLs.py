#!/usr/bin/env python
import os
import sys
import numpy as np

os.chdir(os.environ.get('_CONDOR_SCRATCH_DIR'))
os.system('tar xvzf limitFiles.tgz')


mass=sys.argv[1]
suffix=sys.argv[2]
outPutFolder = sys.argv[4]
syst = sys.argv[5]

cardName = sys.argv[3]

if float(mass)>=800:
  rMin = 0
  rMax = 1
  singlePoints = np.linspace(0.1,0.6,8)
elif float(mass)>=600:
  rMin = 0
  rMax = 1.5
  singlePoints = np.linspace(0.1,1,8)
elif float(mass)>=500:
  rMin = 0
  rMax = 2
  singlePoints = np.linspace(0.2,1.5,8)
elif float(mass)>=400:
  rMin = 0
  rMax = 2.2
  singlePoints = np.linspace(0.2,2,8)
elif float(mass)>=300:
  rMin = 0
  rMax = 3.5
  singlePoints = np.linspace(0.4,3,8)
else:
  rMin = 0
  rMax = 7
  singlePoints = np.linspace(0.7,6,8)


outputName = 'Output'+cardName[3:]
print 'running limitExe, {0}, mass: {1}'.format(cardName,mass)
for point in singlePoints:
  os.system('combine {1} -M HybridNew -m {0} --rMin={3} --rMax={4} --freq --fullBToys -s -1 -T 1000 -i 5 --saveToys --saveHybridResult --clsAcc 0 -v9 --singlePoint={2}'.format(mass,cardName,point,rMin,rMax))
#os.system('combine -M Asymptotic --minimizerStrategy 0 -m {0} -n {2} {1}'.format(mass,cardName,outputName.replace('M'+mass,'').replace('.txt','')))


print 'Done'
