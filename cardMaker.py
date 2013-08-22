#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
from systematics import *
import numpy as np
#import pdb
from rooFitBuilder import *
from collections import defaultdict

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

#################################################
# We're finally ready to make the datacards     #
# Pull the info out, make the cards, write them #
# Run with: combine -M Asymptotic datacard.txt  #
#################################################

def makeCards():
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
  sigNameList = ['gg','vbf','wh','zh','tth']

  bgFile = TFile('testCards/testCardBackground.root')
  bgWs = bgFile.Get('ws_card')
  bgFileName = 'testCardBackground.root'

  for year in yearList:
    for lepton in leptonList:
      for cat in catList:

        if cat in ['1','4']: phoGeom = 'EB'
        else: phoGeom = 'EE'
        channel = '_'.join([lepton,year,'cat'+cat])
        if cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
          bkgParams = ['p1','p2','p3','p4','sigma','step','norm']
        else:
          bkgParams = ['p1','p2','p3','p4','p5','sigma','step','norm']

        for mass in massList:
          sigFileName = 'testCardSignal_'+mass+'.root'
          sigFile = TFile('testCards/'+sigFileName)
          sigWs = sigFile.Get('ws_card')
          prefixSigList = ['sig_'+sig for sig in sigNameList]

          card = open('testCards/'+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass])+'.txt','w')
          card.write('#some bullshit\n')
          card.write('#more comments\n')
          card.write('imax *\n')
          card.write('jmax *\n')
          card.write('kmax *\n')
          card.write('---------------\n')
          card.write('shapes {0:<8} * {1:<20} ws_card:$PROCESS_$CHANNEL\n'.format('*',bgFileName))
          card.write('shapes {0:<8} * {1:<20} ws_card:bkg_$CHANNEL\n'.format('bkg',bgFileName))
          for sig in prefixSigList:
            card.write('shapes {0:<8} * {1:<20} ws_card:{2}_$CHANNEL\n'.format(sig,sigFileName,sig))
          card.write('---------------\n')
          bgYield = bgWs.var('data_yield_'+channel).getVal()
          card.write('{0:<12} {1}\n'.format('bin',channel))
          card.write('{0:<12} {1}\n'.format('observation',int(bgYield)))
          card.write('------------------------------\n')
          card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['bin']+[channel]*6)))
          card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process']+prefixSigList[::-1]+['bkg'])))
          card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process',-4,-3,-2,-1,0,1])))
          card.write('-----------------------------------------------------------------------------------------------------------------------\n')
          sigYields = []
          for sig in prefixSigList[::-1]:
            sigYields.append(sigWs.var(sig+'_yield_'+channel).getVal())
          card.write('{0:<25} {1:^15.5} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15}\n'.format(*(['rate']+sigYields+[1])))
          card.write('-----------------------------------------------------------------------------------------------------------------------\n')
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_gg','lnN']+[pdf_tth[year][mass]]+['-']*3+[pdf_gg[year][mass]]+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_qqbar','lnN']+['-']+[pdf_zh[year][mass]]+[pdf_wh[year][mass]]+[pdf_vbf[year][mass]]+['-']*2)))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ggH','lnN']+['-']*4+[qcd_gg[year][mass]]+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_qqH','lnN']+['-']*3+[qcd_vbf[year][mass]]+['-']*2)))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_VH','lnN']+['-']+[qcd_zh[year][mass]]+[qcd_wh[year][mass]]+['-']*3)))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ttH','lnN']+[qcd_tth[year][mass]]+['-']*5)))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['lumi_'+year,'lnN']+[lumi[year]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_'+lepton+'_'+year,'lnN']+[eff_l[year][lepton]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_trig_'+lepton+'_'+year,'lnN']+[eff_trig[year][lepton]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_PU_'+lepton+'_'+year,'lnN']+[eff_PU[year][lepton]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_g_'+phoGeom+'_'+year,'lnN']+[eff_g[year][phoGeom]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_R9_'+year,'lnN']+[eff_R9[year]]*5+['-'])))
          card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['err_BR_'+year,'lnN']+[err_BR[mass]]*5+['-'])))

          for sig in prefixSigList:
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_mShift_'+channel,'param', 1, 0.01))
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_sigmaShift_'+channel,'param', 1, 0.05))

          for param in bkgParams[:-1]:
            card.write('{0:<45} {1:<15}\n'.format('bkg_'+param+'_'+channel,'flatParam'))
          card.write('{0:<45} {1:<15}\n'.format('bkg_'+channel+'_'+bkgParams[-1],'flatParam'))


          card.close()




if __name__=="__main__":
  makeCards()


