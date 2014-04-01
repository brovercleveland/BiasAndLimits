#!/usr/bin/env python
import sys
import os
import math
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

def makeCards(MVATest = False):
  #suffix = 'Proper'
  suffix = '03-19-14_Proper'
  #suffix = '03-31-14_PhoMVA'
  #suffix = '03-31-14_PhoKinMVA'

  leptonList = ['mu','el']
  #leptonList = ['mu']
  tevList = ['7TeV','8TeV']
  #tevList = ['8TeV']
  catListSmall = ['1','2','3','4','5']
  #catListSmall = ['1']
  catListBig = ['1','2','3','4','5','6','7','8','9']
  massList = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
   '124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
   '125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
   '127.0','127.5','128.0','128.5','129.0','129.5','130.0',
   '130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
   '135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
   '141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
   '151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']
  #massList = ['125.0']

  bgFile = TFile('outputDir/'+suffix+'/CardBackground_'+suffix+'.root')
  bgWs = bgFile.Get('ws_card')
  bgFileName = 'CardBackground_'+suffix+'.root'

  for tev in tevList:
    if tev == '7TeV':
      catList = catListSmall
      TeV = '7TeV'
    else:
      TeV = '8TeV'
    if tev == '8TeV' and not MVATest:
      catList = catListSmall
    elif tev == '8TeV' and MVATest:
      catList = catListBig

    for lepton in leptonList:
      for cat in catList:
        sigNameList = ['ggH','qqH','WH','ZH','ttH']
        if tev is '7TeV' and cat is '5' and lepton is 'mu': continue
        elif tev is '7TeV' and cat is '5' and lepton is 'el': lepton='all'


        if cat in ['1','2','3','6','7','8']: phoGeom = 'EB'
        else: phoGeom = 'EE'
        channel = '_'.join([lepton,tev,'cat'+cat])
        if cat is '5':
          bkgParams = ['p1','p2','p3','norm']
          sigNameList = sigNameList[0:2]
        elif cat is '1' and (lepton is 'el' or (lepton is 'mu' and tev is '7TeV')):
          bkgParams = ['p1','p2','p3','p4','sigma','step','norm']
        else:
          bkgParams = ['p1','p2','p3','p4','p5','sigma','step','norm']

        for mass in massList:
          #if not os.path.isfile('outputDir/'+suffix+'/'+mass+'/'+'SignalOutput_All_'+suffix+'_'+mass+'.root'):
            #os.system('hadd -f outputDir/'+suffix+'/'+mass+'/'+'SignalOutput_All_'+suffix+'_'+mass+'.root outputDir/'+suffix+'/'+mass+'/'+'SignalOutput*.root')
          sigFileName = '_'.join(['SignalOutput',lepton,tev,'cat'+cat,mass])+'.root'
          #sigFileName = 'SignalOutput_All_'+suffix+'_'+mass+'.root'
          sigFile = TFile('outputDir/'+suffix+'/'+mass+'/'+sigFileName)
          sigWs = sigFile.Get('ws_card')
          prefixSigList = [sig+'_hzg' for sig in sigNameList]

          #card = open('testCards/'+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass])+'.txt','w')
          cardName = 'outputDir/'+suffix+'/'+mass+'/'+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'
          card = open(cardName, 'w')
          card.write('#removed vulgarity\n')
          card.write('#cards produced by Brian Pollack\n')
          card.write('imax *\n')
          card.write('jmax *\n')
          card.write('kmax *\n')
          card.write('---------------\n')
          card.write('shapes {0:<8} * {1:<20} ws_card:$PROCESS_$CHANNEL\n'.format('*',bgFileName))
          card.write('shapes {0:<8} * {1:<20} ws_card:bkg_$CHANNEL\n'.format('bkg',bgFileName))
          for sig in prefixSigList:
            card.write('shapes {0:<8} * {1:<20} ws_card:{2}_{3}\n'.format(sig,sigFileName,sig,'_'.join([lepton,'cat'+cat,tev])))
          card.write('---------------\n')
          card.write('{0:<12} {1}\n'.format('bin',channel))
          bgYield = bgWs.var('_'.join(['data','yield',lepton,tev,'cat'+cat])).getVal()
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
            sigYields.append(sigWs.var('_'.join([sig,'yield',lepton,tev,'cat'+cat])).getVal())
          if cat is not '5':
            card.write('{0:<25} {1:^15.5} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15}\n'.format(*(['rate']+sigYields+[1])))
            card.write('-----------------------------------------------------------------------------------------------------------------------\n')
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_gg','lnN']+[KapSwap(pdf_tth[tev][mass])]+['-']*3+[pdf_gg[tev][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_qqbar','lnN']+['-']+[pdf_zh[tev][mass]]+[pdf_wh[tev][mass]]+[pdf_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ggH','lnN']+['-']*4+[qcd_gg[tev][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_qqH','lnN']+['-']*3+[qcd_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_VH','lnN']+['-']+[qcd_zh[tev][mass]]+[qcd_wh[tev][mass]]+['-']*3)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ttH','lnN']+[qcd_tth[tev][mass]]+['-']*5)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['lumi_'+TeV,'lnN']+[lumi[tev]]*5+['-'])))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_eff_'+lepton[0],'lnN']+[eff_l[tev][lepton]]*5+['-'])))
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_eff_trig_'+lepton[0],'lnN']+[eff_trig[tev][lepton]]*5+['-'])))
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_eff_PU_'+lepton[0],'lnN']+[eff_PU[tev][lepton]]*5+['-'])))
            totalLeptonEffSys = AddInQuad([eff_l[tev][lepton],eff_trig[tev][lepton],eff_PU[tev][lepton]])
            card.write('{0:<17} {1:<7} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15.5} {7:^15.5}\n'.format(*(['CMS_eff_'+lepton[0],'lnN']+[totalLeptonEffSys]*5+['-'])))

            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_eff_g_'+phoGeom,'lnN']+[eff_g[tev][phoGeom]]*5+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_scale_j','lnN']+['-']*3+[jes_vbf[cat]]+[jes_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_res_j','lnN']+['-']*3+[jer_vbf[cat]]+[jer_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_UEPS','lnN']+['-']*3+[ueps_vbf[cat]]+[ueps_gg[cat]]+['-'])))
            if cat in['1','2','6','7']:
              card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_hzg_eff_R9_'+TeV,'lnN']+[eff_R9[tev]]*5+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_hzg_err_BR','lnN']+[err_BR[mass]]*5+['-'])))
          else:
            card.write('{0:<25} {1:^15.5} {2:^15.5} {3:^15}\n'.format(*(['rate']+sigYields+[1])))
            card.write('-----------------------------------------------------------------------------------------------------------------------\n')
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['pdf_gg','lnN']+['-']+[pdf_gg[tev][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['pdf_qqbar','lnN']+[pdf_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['QCDscale_ggH','lnN']+['-']+[qcd_gg[tev][mass]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['QCDscale_qqH','lnN']+[qcd_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['lumi_'+TeV,'lnN']+[lumi[tev]]*2+['-'])))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_'+lepton[0],'lnN']+[eff_l[tev][lepton]]*2+['-'])))
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_trig_'+lepton[0],'lnN']+[eff_trig[tev][lepton]]*2+['-'])))
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_PU_'+lepton[0],'lnN']+[eff_PU[tev][lepton]]*2+['-'])))
            totalLeptonEffSys = AddInQuad([eff_l[tev][lepton],eff_trig[tev][lepton],eff_PU[tev][lepton]])
            card.write('{0:<17} {1:<7} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15.5} {7:^15.5}\n'.format(*(['CMS_eff_'+lepton[0]+'_'+TeV,'lnN']+[totalLeptonEffSys]*5+['-'])))

            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_g_'+phoGeom,'lnN']+[eff_g[tev][phoGeom]]*2+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_scale_j','lnN']+[jes_vbf[cat]]+[jes_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_res_j','lnN']+[jer_vbf[cat]]+[jer_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_UEPS','lnN']+[ueps_vbf[cat]]+[ueps_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_id_j','lnN']+jetId+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_acc_j','lnN']+jetAcc+['-'])))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_hzg_err_BR','lnN']+[err_BR[mass]]*2+['-'])))

          for sig in prefixSigList:
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_mShift_'+channel,'param', 1, 0.01))
            card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_sigmaShift_'+channel,'param', 1, 0.05))

          for param in bkgParams[:-1]:
            card.write('{0:<45} {1:<15}\n'.format('bkg_'+param+'_'+channel,'flatParam'))
          card.write('{0:<45} {1:<15}\n'.format('bkg_'+channel+'_'+bkgParams[-1],'flatParam'))


          card.close()
          print cardName, 'created'



def KapSwap(inputSyst = '1.0/2.0'):
  splitSyst = inputSyst.split('/')
  outputSyst = splitSyst[-1] + '/' + splitSyst[0]
  return outputSyst

def AddInQuad(inputList = ['1.1','1.2','1.3','1.4','1.5']):
  return str(1+math.sqrt(sum((1-float(i))**2 for i in inputList)))


if __name__=="__main__":
  makeCards()
  #print AddInQuad()


