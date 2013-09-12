#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *

def makeToyStucts():
  gROOT.ProcessLine('''
  struct TOYDATA{
    Int_t totalData;
    Int_t sigWindowData;
  };
  ''')

  gROOT.ProcessLine('''
  struct GAUSSBERN3{
    Double_t yieldBkg;
    Double_t yieldBkgErr;
    Double_t yieldSig;
    Double_t yieldSigErr;
    Double_t paramSigma;
    Double_t paramSigmaErr;
    Double_t paramStep;
    Double_t paramStepErr;
    Double_t paramP1;
    Double_t paramP1Err;
    Double_t paramP2;
    Double_t paramP2Err;
    Double_t paramP3;
    Double_t paramP3Err;

    Int_t statusAll;
    Int_t statusMIGRAD;
    Int_t statusHESSE;
    Int_t covQual;
    Int_t numInvalidNLL;
    Double_t edm;
    Double_t minNll;
  };
  ''')

  gROOT.ProcessLine('''
  struct GAUSSBERN4{
    Double_t yieldBkg;
    Double_t yieldBkgErr;
    Double_t yieldSig;
    Double_t yieldSigErr;
    Double_t paramSigma;
    Double_t paramSigmaErr;
    Double_t paramStep;
    Double_t paramStepErr;
    Double_t paramP1;
    Double_t paramP1Err;
    Double_t paramP2;
    Double_t paramP2Err;
    Double_t paramP3;
    Double_t paramP3Err;
    Double_t paramP4;
    Double_t paramP4Err;

    Int_t statusAll;
    Int_t statusMIGRAD;
    Int_t statusHESSE;
    Int_t covQual;
    Int_t numInvalidNLL;
    Double_t edm;
    Double_t minNll;
  };
  ''')

  gROOT.ProcessLine('''
  struct GAUSSBERN5{
    Double_t yieldBkg;
    Double_t yieldBkgErr;
    Double_t yieldSig;
    Double_t yieldSigErr;
    Double_t paramSigma;
    Double_t paramSigmaErr;
    Double_t paramStep;
    Double_t paramStepErr;
    Double_t paramP1;
    Double_t paramP1Err;
    Double_t paramP2;
    Double_t paramP2Err;
    Double_t paramP3;
    Double_t paramP3Err;
    Double_t paramP4;
    Double_t paramP4Err;
    Double_t paramP5;
    Double_t paramP5Err;

    Int_t statusAll;
    Int_t statusMIGRAD;
    Int_t statusHESSE;
    Int_t covQual;
    Int_t numInvalidNLL;
    Double_t edm;
    Double_t minNll;
  };
  ''')
