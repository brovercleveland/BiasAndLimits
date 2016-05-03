#!/usr/bin/env python
import sys
import os
import math
from ROOT import *
from systematics import *
import numpy as np
#import pdb
from rooFitBuilder import *
from collections import defaultdict
from configLimits import AutoVivification
import configLimits as cfl
import pickle
gROOT.SetBatch()

f = open('XSBR.p')
xsDict = pickle.load(f)
xsScaleErrDict = pickle.load(f)
xsPDFErrDict = pickle.load(f)
brDict = pickle.load(f)
brErrDict = pickle.load(f)
f.close()

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

prodToPick = {'ggH':'ggF','qqH':'VBF','WH':'WH','ZH':'ZH','ttH':'ttH'}


#################################################
# We're finally ready to make the datacards     #
# Pull the info out, make the cards, write them #
# Run with: combine -M Asymptotic datacard.txt  #
#################################################

def makeCards(MVATest = cfl.doMVA):
  suffix = cfl.suffixPostFix

  leptonList = cfl.leptonList
  tevList = cfl.tevList
  catListSmall = cfl.catListSmall
  catListBig = cfl.catListBig
  massList = cfl.massListBig

  YR = cfl.YR
  sigFit = cfl.sigFit
  scale13TeV = cfl.scale13TeV

  bgFile = TFile('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/CardBackground_'+suffix+'.root')
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
        #if cat == '0': continue
        sigNameList = cfl.sigNameList
        if len(sigNameList)==5:
          sigNameList = ['ggH','qqH','WH','ZH','ttH']
        if tev is '7TeV' and cat is '5' and lepton is 'mu': continue
        elif tev is '7TeV' and cat is '5' and lepton is 'el': lepton='all'


        if cat in ['1','2','3','6','7','8']: phoGeom = 'EB'
        else: phoGeom = 'EE'
        channel = '_'.join([lepton,tev,'cat'+cat])
        if cfl.highMass:
          #bkgParams = ['p1','p2','p3','p4','p5','norm']
          #bkgParams = ['p1','p2','p3','p4','p5','p6','norm']
          #bkgParams = ['p1','p2','p3','p4','k','norm']
          #bkgParams = ['p1','p2','p3','k','norm']
          bkgParams = ['p1','p2','norm']
        elif cat is '5':
          bkgParams = ['p1','p2','p3','norm']
          sigNameList = filter(lambda i: i in ['ggH', 'qqH'],sigNameList)
        elif cat is '1' and (lepton is 'el' or (lepton is 'mu' and tev is '7TeV')):
          bkgParams = ['p1','p2','p3','p4','sigma','step','norm']
        else:
          bkgParams = ['p1','p2','p3','p4','p5','sigma','step','norm']

        for mass in massList:
          YR = cfl.YR
          sigFileName = '_'.join(['SignalOutput',lepton,tev,'cat'+cat,mass])+'.root'
          #sigFileName = 'SignalOutput_All_'+suffix+'_'+mass+'.root'
          sigFile = TFile('outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'+sigFileName)
          sigWs = sigFile.Get('ws_card')
          prefixSigList = [sig+'_hzg' for sig in sigNameList]

          #card = open('testCards/'+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass])+'.txt','w')
          cardName = 'outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'+'_'.join(['hzg',lepton,tev,'cat'+cat,'M'+mass,suffix])+'.txt'

          if type(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]) == AutoVivification:
            if YR == 'YR3': YR = 'YR2'
            elif YR == 'YR2': YR = 'YR3'

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

          #card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['bin']+[channel]*6)))
          card.write('{0:<25} '.format('bin'))
          for sig in prefixSigList[::-1]:
            card.write('{0:^15} '.format(channel))
          card.write('{0:^15}\n'.format(channel))

          #card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process']+prefixSigList[::-1]+['bkg'])))
          card.write('{0:<25} '.format('process'))
          for sig in prefixSigList[::-1]:
            card.write('{0:^15} '.format(sig))
          card.write('{0:^15}\n'.format('bkg'))

          #card.write('{0:<25} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15}\n'.format(*(['process',-4,-3,-2,-1,0,1])))
          card.write('{0:<25} '.format('process'))
          for i,sig in enumerate(prefixSigList[::-1]):
            card.write('{0:^15} '.format(i+1-len(prefixSigList)))
          card.write('{0:^15}\n'.format('1'))

          card.write('-----------------------------------------------------------------------------------------------------------------------\n')
          sigYields = []
          for sig in prefixSigList[::-1]:
            sigYields.append(sigWs.var('_'.join([sig,'yield',lepton,tev,'cat'+cat])).getVal())
          #if cat is not '5':
          #card.write('{0:<25} {1:^15.5} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15}\n'.format(*(['rate']+sigYields+[1])))
          card.write('{0:<25} '.format('rate'))
          zBR = 1
          if cfl.highMass: zBR = 0.10098
          else: zBR = 1
          for sig in prefixSigList[::-1]:
            if scale13TeV:
              card.write('{0:^15.5} '.format(sigWs.var('_'.join([sig,'yield',lepton,tev,'cat'+cat])).getVal()*5.0/zBR))
            else:
              #card.write('{0:^15.5} '.format(sigWs.var('_'.join([sig,'yield',lepton,tev,'cat'+cat])).getVal()/zBR))
              card.write('{0:^15.5} '.format(sigWs.var('_'.join([sig,'yield',lepton,tev,'cat'+cat])).getVal()))
          if scale13TeV:
            card.write('{0:^15}\n'.format(10))
          else:
            card.write('{0:^15}\n'.format(1))

          card.write('-----------------------------------------------------------------------------------------------------------------------\n')

          #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_gg','lnN']+[KapSwap(pdf_tth[tev][mass])]+['-']*3+[pdf_gg[tev][mass]]+['-'])))

          if not cfl.modelIndependent and not cfl.highMass:
            card.write('{0:<17} {1:<7} '.format('pdf_gg','lnN'))
            for sig in prefixSigList[::-1]:
              #if 'ggH' in sig: card.write('{0:^15} '.format(pdf_gg[tev][mass]))
              #elif 'ttH' in sig: card.write('{0:^15} '.format(KapSwap(pdf_tth[tev][mass])))
              if 'ggH' in sig: card.write('{0:^15} '.format(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              elif 'ttH' in sig: card.write('{0:^15} '.format(KapSwap(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass])))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['pdf_qqbar','lnN']+['-']+[pdf_zh[tev][mass]]+[pdf_wh[tev][mass]]+[pdf_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} '.format('pdf_qqbar','lnN'))
            for sig in prefixSigList[::-1]:
              #if 'ZH' in sig: card.write('{0:^15} '.format(pdf_zh[tev][mass]))
              #elif 'WH' in sig: card.write('{0:^15} '.format(pdf_wh[tev][mass]))
              #elif 'qqH' in sig: card.write('{0:^15} '.format(pdf_vbf[tev][mass]))
              if 'ZH' in sig: card.write('{0:^15} '.format(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              elif 'WH' in sig: card.write('{0:^15} '.format(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              elif 'qqH' in sig: card.write('{0:^15} '.format(xsPDFErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ggH','lnN']+['-']*4+[qcd_gg[tev][mass]]+['-'])))
            card.write('{0:<17} {1:<7} '.format('QCDscale_ggH','lnN'))
            for sig in prefixSigList[::-1]:
              #if 'ggH' in sig: card.write('{0:^15} '.format(qcd_gg[tev][mass]))
              if 'ggH' in sig: card.write('{0:^15} '.format(xsScaleErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_qqH','lnN']+['-']*3+[qcd_vbf[tev][mass]]+['-']*2)))
            card.write('{0:<17} {1:<7} '.format('QCDscale_qqH','lnN'))
            for sig in prefixSigList[::-1]:
              #if 'qqH' in sig: card.write('{0:^15} '.format(qcd_vbf[tev][mass]))
              if 'qqH' in sig: card.write('{0:^15} '.format(xsScaleErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            if cat != '5':
              #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_VH','lnN']+['-']+[qcd_zh[tev][mass]]+[qcd_wh[tev][mass]]+['-']*3)))
              card.write('{0:<17} {1:<7} '.format('QCDscale_VH','lnN'))
              for sig in prefixSigList[::-1]:
                #if 'ZH' in sig: card.write('{0:^15} '.format(qcd_zh[tev][mass]))
                #elif 'WH' in sig: card.write('{0:^15} '.format(qcd_wh[tev][mass]))
                if 'ZH' in sig: card.write('{0:^15} '.format(xsScaleErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
                elif 'WH' in sig: card.write('{0:^15} '.format(xsScaleErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
                else: card.write('{0:^15} '.format('-'))
              card.write('{0:^15}\n'.format('-'))

              #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['QCDscale_ttH','lnN']+[qcd_tth[tev][mass]]+['-']*5)))
              card.write('{0:<17} {1:<7} '.format('QCDscale_ttH','lnN'))
              for sig in prefixSigList[::-1]:
                #if 'ttH' in sig: card.write('{0:^15} '.format(qcd_tth[tev][mass]))
                if 'ttH' in sig: card.write('{0:^15} '.format(xsScaleErrDict[YR][tev][prodToPick[sig.rstrip('_hzg')]][mass]))
                else: card.write('{0:^15} '.format('-'))
              card.write('{0:^15}\n'.format('-'))

          #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['lumi_'+TeV,'lnN']+[lumi[tev]]*5+['-'])))
          card.write('{0:<17} {1:<7} '.format('lumi_'+TeV,'lnN'))
          for sig in prefixSigList[::-1]:
            card.write('{0:^15} '.format(lumi[tev]))
          card.write('{0:^15}\n'.format('-'))

          totalLeptonEffSys = AddInQuad([eff_l[tev][lepton],eff_trig[tev][lepton],eff_PU[tev][lepton]])
          #card.write('{0:<17} {1:<7} {2:^15.5} {3:^15.5} {4:^15.5} {5:^15.5} {6:^15.5} {7:^15.5}\n'.format(*(['CMS_eff_'+lepton[0],'lnN']+[totalLeptonEffSys]*5+['-'])))
          card.write('{0:<17} {1:<7} '.format('CMS_eff_'+lepton[0],'lnN'))
          for sig in prefixSigList[::-1]:
            card.write('{0:^15.5} '.format(totalLeptonEffSys))
          card.write('{0:^15}\n'.format('-'))

          #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_eff_g','lnN']+[eff_g[tev][phoGeom]]*5+['-'])))
          card.write('{0:<17} {1:<7} '.format('CMS_eff_g','lnN'))
          for sig in prefixSigList[::-1]:
            card.write('{0:^15} '.format(eff_g[tev][phoGeom]))
          card.write('{0:^15}\n'.format('-'))

          #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_scale_j','lnN']+['-']*3+[jes_vbf[cat]]+[jes_gg[cat]]+['-'])))
          if cat != '0':
            card.write('{0:<17} {1:<7} '.format('CMS_scale_j','lnN'))
            for sig in prefixSigList[::-1]:
              if 'ggH' in sig: card.write('{0:^15} '.format(jes_gg[cat]))
              elif 'qqH' in sig: card.write('{0:^15} '.format(jes_vbf[cat]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_res_j','lnN']+['-']*3+[jer_vbf[cat]]+[jer_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_res_j','lnN'))
            for sig in prefixSigList[::-1]:
              if 'ggH' in sig: card.write('{0:^15} '.format(jer_gg[cat]))
              elif 'qqH' in sig: card.write('{0:^15} '.format(jer_vbf[cat]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_UEPS','lnN']+['-']*3+[ueps_vbf[cat]]+[ueps_gg[cat]]+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_UEPS','lnN'))
            for sig in prefixSigList[::-1]:
              if 'ggH' in sig: card.write('{0:^15} '.format(ueps_gg[cat]))
              elif 'qqH' in sig: card.write('{0:^15} '.format(ueps_vbf[cat]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

          if cat == '5':
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_id_j','lnN']+jetId+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_eff_id_j','lnN'))
            for sig in prefixSigList[::-1]:
              if 'qqH' in sig: card.write('{0:^15} '.format(jetId[0]))
              elif 'ggH' in sig: card.write('{0:^15} '.format(jetId[1]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15}\n'.format(*(['CMS_eff_acc_j','lnN']+jetAcc+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_eff_acc_j','lnN'))
            for sig in prefixSigList[::-1]:
              if 'qqH' in sig: card.write('{0:^15} '.format(jetAcc[0]))
              elif 'ggH' in sig: card.write('{0:^15} '.format(jetAcc[1]))
              else: card.write('{0:^15} '.format('-'))
            card.write('{0:^15}\n'.format('-'))

          if cat in['1','2','6','7']:
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_hzg_eff_R9_'+TeV,'lnN']+[eff_R9[tev]]*5+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_hzg_eff_R9_'+TeV,'lnN'))
            for sig in prefixSigList[::-1]:
              card.write('{0:^15} '.format(eff_R9[tev]))
            card.write('{0:^15}\n'.format('-'))

          if not cfl.modelIndependent and not cfl.highMass:
            #card.write('{0:<17} {1:<7} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}\n'.format(*(['CMS_hzg_err_BR','lnN']+[err_BR[mass]]*5+['-'])))
            card.write('{0:<17} {1:<7} '.format('CMS_hzg_err_BR','lnN'))
            for sig in prefixSigList[::-1]:
              #card.write('{0:^15} '.format(err_BR[mass]))
              card.write('{0:^15} '.format(brErrDict[YR]['Zgamma'][mass]))
            card.write('{0:^15}\n'.format('-'))


          if cfl.highMass:
            card.write('{0:<17} {1:<7} {2:^15} {3:^15}\n'.format('CMS_hzgHigh_acc','lnN',pdfSys,'-'))
            card.write('{0:<17} {1:<7} {2:^15} {3:^15}\n'.format('CMS_hzgHigh_pu','lnN',puSys,'-'))

          if cfl.highMass:
            for sig in prefixSigList:
              card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_mShift_'+channel,'param', 1, 0.01))
              card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_sigmaShift_'+channel,'param', 1, 0.1))
          else:
            for sig in prefixSigList:
              card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_mShift_'+channel,'param', 1, 0.01))
              card.write('{0:<40} {1:<10} {2:^10} {3:^10}\n'.format(sig+'_sigmaShift_'+channel,'param', 1, 0.05))

          for param in bkgParams[:-1]:
            card.write('{0:<45} {1:<15}\n'.format('bkg_'+param+'_'+channel,'flatParam'))
          card.write('{0:<45} {1:<15}\n'.format('bkg_'+channel+'_'+bkgParams[-1],'flatParam'))


          card.close()
  print 'cards created'



def KapSwap(inputSyst = '1.0/2.0'):
  splitSyst = inputSyst.split('/')
  outputSyst = splitSyst[-1] + '/' + splitSyst[0]
  return outputSyst

def AddInQuad(inputList = ['1.1','1.2','1.3','1.4','1.5']):
  return str(1+math.sqrt(sum((1-float(i))**2 for i in inputList)))


if __name__=="__main__":
  makeCards()
  #print AddInQuad()


