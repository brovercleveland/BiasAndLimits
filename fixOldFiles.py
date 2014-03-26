#!/usr/bin/env python
import sys,os
#sys.argv.append('-b')
from ROOT import *
import numpy as np


gROOT.SetBatch()

leptonList = ['mu','el']
yearList = ['2011','2012']
catList = ['0','1','2','3','4','5']
massList = ['120','125','130','135','140','145','150','155','160']
sigNameListInput = ['gg','vbf','tth','wh','zh']

def doData():
  for lep in leptonList:
    for year in yearList:
      infileData = TFile('inputFiles/poterFiles/data_'+lep.capitalize()+year+'.root','READ')
      #infileSignal = TFile('inputFiles/poterFiles/signal_'+lep.capitalize()+year+'.root','READ')
      if lep == 'el': outfile = TFile('inputFiles/m_llgFile_'+lep[0].capitalize()*2+year+'ABCD_Proper.root','RECREATE')
      else: outfile = TFile('inputFiles/m_llgFile_'+lep.capitalize()*2+year+'ABCD_Proper.root','RECREATE')

      # data part
      dataTreeIn = infileData.Get('m_llg_DATA')
      outfile.cd()
      dataTreeOut = TTree('m_llg_DATA','m_llg_DATA')

      n0 = np.zeros(1, dtype='d')
      n1 = np.zeros(1, dtype='d')
      n2 = np.zeros(1, dtype='d')
      n3 = np.zeros(1, dtype='d')
      n4 = np.zeros(1, dtype='d')
      n5 = np.zeros(1, dtype='d')
      dataTreeOut.Branch('m_llg_DATA',n0,'m_llg_DATA/D')
      dataTreeOut.Branch('m_llgCAT1_DATA',n1,'m_llgCAT1_DATA/D')
      dataTreeOut.Branch('m_llgCAT2_DATA',n2,'m_llgCAT2_DATA/D')
      dataTreeOut.Branch('m_llgCAT3_DATA',n3,'m_llgCAT3_DATA/D')
      dataTreeOut.Branch('m_llgCAT4_DATA',n4,'m_llgCAT4_DATA/D')
      if year == '2012': dataTreeOut.Branch('m_llgCAT5_DATA',n5,'m_llgCAT5_DATA/D')

      for event in dataTreeIn:
        n0[0] = event.m_llg_DATA
        n1[0] = event.m_llgCAT1_DATA
        n2[0] = event.m_llgCAT4_DATA
        n3[0] = event.m_llgCAT2_DATA
        n4[0] = event.m_llgCAT3_DATA
        if year == '2012': n5[0] = event.m_llgCAT5_DATA

        dataTreeOut.Fill()

      infileData.Close()
      outfile.Write()
      outfile.Close()

      if year == '2011' and lep == 'el':
        infileData = TFile('inputFiles/poterFiles/data_All2011.root')
        #infileSignal = TFile('inputFiles/poterFiles/signal_All2011.root')
        outfile = TFile('inputFiles/m_llgFile_All'+year+'ABCD_Proper.root','RECREATE')

        dataTreeIn = infileData.Get('m_llg_DATA')
        outfile.cd()
        dataTreeOut = TTree('m_llg_DATA','m_llg_DATA')
        dataTreeOut.Branch('m_llgCAT5_DATA',n5,'m_llgCAT5_DATA/D')

        for event in dataTreeIn:
          n5[0] = event.m_llgCAT5_DATA

          dataTreeOut.Fill()

        infileData.Close()
        #infileSignal.Close()
        outfile.Write()
        outfile.Close()

def doSignal():
  for lep in leptonList:
    for year in yearList:
      infileSignal = TFile('inputFiles/poterFiles/signal_'+lep.capitalize()+year+'.root','READ')
      if lep == 'el': outfile = TFile('inputFiles/m_llgFile_'+lep[0].capitalize()*2+year+'ABCD_Proper.root','UPDATE')
      else: outfile = TFile('inputFiles/m_llgFile_'+lep.capitalize()*2+year+'ABCD_Proper.root','UPDATE')

      for sig in sigNameListInput:
        for mass in massList:
          sigTreeIn = infileSignal.Get('m_llg_Signal'+year+sig+'M'+mass)
          outfile.cd()
          sigTreeOut = TTree('m_llg_Signal'+year+sig+'M'+mass,'m_llg_Signal'+year+sig+'M'+mass)

          n0 = np.zeros(1, dtype='d')
          n1 = np.zeros(1, dtype='d')
          n2 = np.zeros(1, dtype='d')
          n3 = np.zeros(1, dtype='d')
          n4 = np.zeros(1, dtype='d')
          n5 = np.zeros(1, dtype='d')
          nw = np.zeros(1, dtype='d')
          sigTreeOut.Branch('m_llg_Signal'+year+sig+'M'+mass,n0,'m_llg_Signal'+year+sig+'M'+mass+'/D')
          sigTreeOut.Branch('m_llgCAT1_Signal'+year+sig+'M'+mass,n1,'m_llgCAT1_Signal'+year+sig+'M'+mass+'/D')
          sigTreeOut.Branch('m_llgCAT2_Signal'+year+sig+'M'+mass,n2,'m_llgCAT2_Signal'+year+sig+'M'+mass+'/D')
          sigTreeOut.Branch('m_llgCAT3_Signal'+year+sig+'M'+mass,n3,'m_llgCAT3_Signal'+year+sig+'M'+mass+'/D')
          sigTreeOut.Branch('m_llgCAT4_Signal'+year+sig+'M'+mass,n4,'m_llgCAT4_Signal'+year+sig+'M'+mass+'/D')
          if year == '2012': sigTreeOut.Branch('m_llgCAT5_Signal'+year+sig+'M'+mass,n5,'m_llgCAT5_Signal'+year+sig+'M'+mass+'/D')
          sigTreeOut.Branch('unBinnedWeight_Signal'+year+sig+'M'+mass,nw,'unBinnedWeight_Signal'+year+sig+'M'+mass+'/D')

          print lep, year, sig, mass
          totalEvents = 0
          for i,event in enumerate(sigTreeIn):
            n0[0] = getattr(event, 'm_llg_Signal'+year+sig+'M'+mass)
            n1[0] = getattr(event, 'm_llgCAT1_Signal'+year+sig+'M'+mass)
            n2[0] = getattr(event, 'm_llgCAT4_Signal'+year+sig+'M'+mass)
            n3[0] = getattr(event, 'm_llgCAT2_Signal'+year+sig+'M'+mass)
            n4[0] = getattr(event, 'm_llgCAT3_Signal'+year+sig+'M'+mass)
            if year == '2012': n5[0] = getattr(event, 'm_llgCAT5_Signal'+year+sig+'M'+mass)
            nw[0] = getattr(event, 'unBinnedWeight_Signal'+year+sig+'M'+mass)
            if i ==0:
              totalEvents = getattr(event, 'unBinnedLumiXS_Signal'+year+sig+'M'+mass)

            sigTreeOut.Fill()

          unskimmedEvents = TH1F('unskimmedEventsTotal_Signal'+year+sig+'M'+mass,'unskimmedEventsTotal_Signal'+year+sig+'M'+mass,1,0,1)
          unskimmedEvents.SetBinContent(1,totalEvents)

          outfile.Write()

      infileSignal.Close()
      outfile.Close()

      if year == '2011' and lep == 'el':
        infileSignal = TFile('inputFiles/poterFiles/signal_All2011.root')
        outfile = TFile('inputFiles/m_llgFile_All'+year+'ABCD_Proper.root','UPDATE')
        for sig in sigNameListInput:
          for mass in massList:

            sigTreeIn = infileSignal.Get('m_llg_Signal'+year+sig+'M'+mass)
            outfile.cd()
            sigTreeOut = TTree('m_llg_Signal'+year+sig+'M'+mass,'m_llg_Signal'+year+sig+'M'+mass)
            n5 = np.zeros(1, dtype='d')
            nw = np.zeros(1, dtype='d')
            sigTreeOut.Branch('m_llgCAT5_Signal'+year+sig+'M'+mass,n5,'m_llgCAT5_Signal'+year+sig+'M'+mass+'/D')
            sigTreeOut.Branch('unBinnedWeight_Signal'+year+sig+'M'+mass,nw,'unBinnedWeight_Signal'+year+sig+'M'+mass+'/D')

            print 'all', year, sig, mass
            totalEvents = 0
            for i,event in enumerate(sigTreeIn):
              n5[0] = getattr(event, 'm_llgCAT5_Signal'+year+sig+'M'+mass)
              nw[0] = getattr(event, 'unBinnedWeight_Signal'+year+sig+'M'+mass)
              if i ==0:
                totalEvents = getattr(event, 'unBinnedLumiXS_Signal'+year+sig+'M'+mass)

              sigTreeOut.Fill()

            unskimmedEvents = TH1F('unskimmedEventsTotal_Signal'+year+sig+'M'+mass,'unskimmedEventsTotal_Signal'+year+sig+'M'+mass,1,0,1)
            unskimmedEvents.SetBinContent(1,totalEvents)

            outfile.Write()

        infileSignal.Close()
        outfile.Close()

if __name__=='__main__':
  doData()
  doSignal()

