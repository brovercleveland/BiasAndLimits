#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
from systematics import *
import numpy as np
#import pdb
from rooFitBuilder import *
from collections import defaultdict
from signalCBFits import AutoVivification

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

#################################################
# We're finally ready to make the datacards     #
# Pull the info out, make the cards, write them #
# Run with: combine -M Asymptotic datacard.txt  #
#################################################

def makeCards(MVATest = True):
  #still uses old cat ordering
  MVASigScale = AutoVivification()
  MVASigScale['mu']['1'] = 0.64
  MVASigScale['mu']['2'] = 0.63
  MVASigScale['mu']['3'] = 0.89
  MVASigScale['mu']['4'] = 0.86
  MVASigScale['mu']['5'] = 1.0

  MVASigScale['el']['1'] = 0.67
  MVASigScale['el']['2'] = 0.62
  MVASigScale['el']['3'] = 0.73
  MVASigScale['el']['4'] = 0.85
  MVASigScale['el']['5'] = 1.0
  '''
  leptonList = ['mu','el']
  yearList = ['2012','2011']
  catList = ['1','2','3','4']
  massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0']
  sigNameList = ['gg','vbf','tth','wh','zh']
  '''
  leptonList = ['mu','el']
  yearList = ['2011','2012']
  catList = ['1','2','3','4','5']
  #catList = ['1']
  #massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5','125.0',
  # '125.5','126.0','126.5','127.0','127.5','128.0','128.5','129.0','129.5','130.0',
  # '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
  # '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
  # '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
  # '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
  massList = ['125.0']

  for year in yearList:
    for lepton in leptonList:
      for cat in catList:
        if MVATest and year is '2012' and cat is not '5':
          bgFile = TFile('testCards/testCardBackground_MVA.root')
          bgWs = bgFile.Get('ws_card')
          bgFileName = 'testCardBackground_MVA.root'
        else:
          bgFile = TFile('testCards/testCardBackground.root')
          bgWs = bgFile.Get('ws_card')
          bgFileName = 'testCardBackground.root'
        sigNameList = ['gg','vbf','wh','zh','tth']
        if year is '2011' and cat is '5' and lepton is 'mu': continue
        elif year is '2011' and cat is '5' and lepton is 'el': lepton='all'


        if cat in ['1','4']: phoGeom = 'EB'
        else: phoGeom = 'EE'
        channel = '_'.join([lepton,year,'cat'+cat])
        if cat is '5':
          bkgParams = ['p1','p2','p3','norm']
          sigNameList = sigNameList[0:2]
        elif cat is '1' and (lepton is 'el' or (lepton is 'mu' and year is '2011')):
          bkgParams = ['p1','p2','p3','p4','sigma','step','norm']
        else:
          bkgParams = ['p1','p2','p3','p4','p5','sigma','step','norm']

        for mass in massList:
          sigFileName = '_'.join(['SignalOutput',lepton,year,'cat'+cat,mass])+'.root'
          sigFile = TFile('testCards/'+sigFileName)
          sigWs = sigFile.Get('ws_card')
          prefixSigList = ['sig_'+sig for sig in sigNameList]

          if MVATest:
            card = open('testCards/'+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass,'MVA'])+'.txt','w')
          else:
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
          if cat is not '5':
            card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['bin']+[channel]*6)))
            card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process']+prefixSigList[::-1]+['bkg'])))
            card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process',-4,-3,-2,-1,0,1])))
          else:
            card.write('{0:<25} {1:^15} {2:^15} {3:^15}\n'.format(*(['bin']+[channel]*3)))
            card.write('{0:<25} {1:^15} {2:^15} {3:^15}\n'.format(*(['process']+prefixSigList[::-1]+['bkg'])))
            card.write('{0:<25} {1:^15} {2:^15} {3:^15}\n'.format(*(['process',-1,0,1])))
          card.write('-----------------------------------------------------------------------------------------------------------------------\n')
          sigYields = []
          for sig in prefixSigList[::-1]:
            if MVATest and year is '2012' and cat is not '5':
              sigYields.append(sigWs.var(sig+'_yield_'+channel).getVal()*MVASigScale[lepton][cat])
            else:
              sigYields.append(sigWs.var(sig+'_yield_'+channel).getVal())
          if cat is not '5':
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
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['JES','lnN']+['-']*3+[jes_vbf[cat]]+[jes_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['JER','lnN']+['-']*3+[jer_vbf[cat]]+[jer_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['UEPS','lnN']+['-']*3+[ueps_vbf[cat]]+[ueps_gg[cat]]+['-'])))
            if cat in['1','4']:
              card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['eff_R9_'+year,'lnN']+[eff_R9[year]]*5+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['err_BR_'+year,'lnN']+[err_BR[mass]]*5+['-'])))
          else:
            card.write('{0:<25} {1:^15.5} {2:^15.5} {3:^15}\n'.format(*(['rate']+sigYields+[1])))
            card.write('-----------------------------------------------------------------------------------------------------------------------\n')
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['pdf_gg','lnN']+['-']+[pdf_gg[year][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['pdf_qqbar','lnN']+[pdf_vbf[year][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['QCDscale_ggH','lnN']+['-']+[qcd_gg[year][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['QCDscale_qqH','lnN']+[qcd_vbf[year][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['lumi_'+year,'lnN']+[lumi[year]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['eff_'+lepton+'_'+year,'lnN']+[eff_l[year][lepton]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['eff_trig_'+lepton+'_'+year,'lnN']+[eff_trig[year][lepton]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['eff_PU_'+lepton+'_'+year,'lnN']+[eff_PU[year][lepton]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['eff_g_'+phoGeom+'_'+year,'lnN']+[eff_g[year][phoGeom]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['JES','lnN']+[jes_vbf[cat]]+[jes_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['JER','lnN']+[jer_vbf[cat]]+[jer_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['UEPS','lnN']+[ueps_vbf[cat]]+[ueps_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['JetID','lnN']+jetId+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['JetAcc','lnN']+jetAcc+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['err_BR_'+year,'lnN']+[err_BR[mass]]*2+['-'])))

          for sig in prefixSigList:
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_mShift_'+channel,'param', 1, 0.01))
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_sigmaShift_'+channel,'param', 1, 0.05))

          for param in bkgParams[:-1]:
            card.write('{0:<45} {1:<15}\n'.format('bkg_'+param+'_'+channel,'flatParam'))
          card.write('{0:<45} {1:<15}\n'.format('bkg_'+channel+'_'+bkgParams[-1],'flatParam'))


          card.close()




if __name__=="__main__":
  makeCards()


