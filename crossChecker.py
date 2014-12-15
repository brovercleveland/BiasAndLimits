#! /usr/bin/env python
import subprocess, os

def doCrossChecks(inputname,inputmass):
  print 'combine -M MaxLikelihoodFit -t -1 --expectSignal 0 outputDir/{0}/{1}/hzg_FullCombo_M{1}_{2}.txt > crossCheckOutputs/{0}_{1}_check.txt'.format(inputname, inputmass, '_'.join(inputname.split('_')[0:2]))
  sp = subprocess.check_call('combine -M MaxLikelihoodFit -t -1 --expectSignal 0 outputDir/{0}/{1}/hzg_FullCombo_M{1}_{2}.txt > crossCheckOutputs/{0}_{1}_checkNoSig.txt &'.format(inputname, inputmass, '_'.join(inputname.split('_')[0:2])),shell=True)
  #sp.check_call()
  #os.system('wait')
  #os.system('python diffNuisances.py -a mlfit.root -g plots.root  > crossCheckOutputs/{0}_{1}_checkNuisanceNoSig.txt &'.format(inputname, inputmass, '_'.join(inputname.split('_')[0:2])))
  #os.system('wait')
  #os.system('combine -M MaxLikelihoodFit -t -1 --expectSignal 1 outputDir/{0}/{1}/hzg_FullCombo_M{1}_{2}.txt >> crossCheckOutputs/{0}_{1}_checkSig.txt &'.format(inputname, inputmass, '_'.join(inputname.split('_')[0:2])))
  #os.system('wait')
  #os.system('python diffNuisances.py -a mlfit.root -g plots.root  >> crossCheckOutputs/{0}_{1}_checkNuisanceSig.txt &'.format(inputname, inputmass, '_'.join(inputname.split('_')[0:2])))
  #os.system('wait')

if __name__ == '__main__':
  masses = [str(float(x)) for x in range(200,505,5)]
  for mass in ['200.0','205.0']:
    doCrossChecks('12-04-14_HighMass_YR3_DCB',mass)
