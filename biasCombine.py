#!/usr/bin/env python
import sys, os
import argparse
import configLimits as cfl

# use it like this: ./hadd.py data/higgsHistograms_EE_allBG-05-23-12.root eeGamma Histograms ZJets ZG

def getArgs():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v","--verbose",action = "store_true")
  group.add_argument("-q","--quiet",action = "store_true")
  subparser = parser.add_subparsers(dest = 'command')
  parser_a = subparser.add_parser("all", help="Loop through all of the tev, lepton, cat, genFunc, mass")
  #parser_a.add_argument("--all", help="Loop through all of the tev, lepton, cat, genFunc, mass", action="store_true")
  parser_b = subparser.add_parser("single", help="Only combine a single set of jobs")
  parser_b.add_argument("--tev", help="CoM Energy", default = cfl.tevList[0], choices = ['7TeV','8TeV'] )
  parser_b.add_argument("--lepton", help="Lepton Flavor", default = cfl.leptonList[0], choices = ['mu','el'])
  parser_b.add_argument("--cat", help="Cat Number", default = cfl.catListSmall[0], type = int)
  parser_b.add_argument("--genFunc", help="PDF used to generate toy data", default = cfl.genFuncs[0], type = str)
  parser_b.add_argument("--mass", help="Mass of signal template", default = cfl.massList[0], type = int)
  args = parser.parse_args()
  return args

def hadd(tev,lepton,cat,genFunc,mass):
  biasPath = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'
  biasPath = biasPath+cfl.suffix+'_'+cfl.YR+'_'+cfl.sigFit+'/biasStudy'

  if not os.path.isdir(biasPath+'/combine/'): os.mkdir(biasPath+'/combine/')

  outName = biasPath+'/combine/'+'_'.join(['combined',tev,lepton,cat,genFunc,mass])+'.root'
  inName = biasPath+'/'+'_'.join(['biasToys',tev,lepton,'cat'+cat,genFunc,mass,'job*'])+'.root'
  os.system('hadd -f '+outName+' '+inName)
  #print output, inputs

#hadd -f otherHistos/eleSmear2011.root ~/nobackup/BatchOutput/eeGamma_Combined/eleSmearFile_*




if __name__=="__main__":
  args = getArgs()
  if args.command == 'single':
    hadd(args.tev,args.lepton,str(args.cat),args.genFunc,str(args.mass))
  elif args.command == 'all':
    for tev in cfl.tevList:
      for lepton in cfl.leptonList:
        for cat in cfl.catListSmall:
          for func in cfl.genFuncs:
            for mass in cfl.massList:
              hadd(tev,lepton,cat,func,mass)


