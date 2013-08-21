#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

#################################################
# We're finally ready to make the datacards     #
# Pull the info out, make the cards, write them #
# Run with: combine -M Asymptotic datacard.txt  #
#################################################


'''
leptonList = ['mu','el']
yearList = ['2012','2011']
catList = ['1','2','3','4']
massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0']
sigNameList = ['gg','vbf','tth','wh','zh']
'''
leptonList = ['mu']
yearList = ['2012']
catList = ['1']
massList = ['120.0']
sigNameList = ['gg','vbf','tth','wh','zh']

bgFile = TFile('testCards/testCardBackground.root')
bgWs = bgFile.Get('ws_card')
bgFileName = 'testCardBackground.root'

for year in yearList:
  for lepton in leptonList:
    for cat in catList:
      channel = '_'.join([lepton,year,'cat'+cat])
      for mass in massList:
        sigFileName = 'testCardSignal_'+mass+'.root'
        sigFile = TFile('testCards/'+sigFileName)
        sigWs = bgFile.Get('ws_card')

        card = open('testCards/'+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass])+'.txt','w')
        card.write('imax *\n')
        card.write('jmax *\n')
        card.write('kmax *\n')
        card.write('---------------\n')
        card.write('shapes {0:<8} * {1:<20} ws_card:$PROCESS_$CHANNEL\n'.format('*',bgFileName))
        card.write('shapes {0:<8} * {1:<20} ws_card:bkg_$CHANNEL\n'.format('bkg',bgFileName))
        for sig in sigNameList:
          card.write('shapes {0:<8} * {1:<20} ws_card:{2}_$CHANNEL\n'.format('sig_'+sig,sigFileName,'sig_'+sig))
        card.write('---------------\n')
        bgYield = bgWs.var('data_yield_'+channel).getVal()
        card.write('{0:<12} {1}\n'.format('bin',channel))
        card.write('{0:<12} {1}\n'.format('observation',int(bgYield)))

        card.close()



