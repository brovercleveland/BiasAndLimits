#!/usr/bin/env python
import sys
from ROOT import *

def makeToyStucts():
  print 'making TOYDATA..'
  gROOT.ProcessLine(
  'struct TOYDATA{\
    Int_t totalData;\
    Int_t sigWindowData;\
  };')

  print 'making GAUSSBERN3...'
  gROOT.ProcessLine(
  'struct GAUSSBERN3{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramSigma;\
    Double_t paramSigmaErr;\
    Double_t paramStep;\
    Double_t paramStepErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making GAUSSBERN4...'
  gROOT.ProcessLine(
  'struct GAUSSBERN4{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramSigma;\
    Double_t paramSigmaErr;\
    Double_t paramStep;\
    Double_t paramStepErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t paramP4;\
    Double_t paramP4Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making GAUSSBERN5...'
  gROOT.ProcessLine(
  'struct GAUSSBERN5{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramSigma;\
    Double_t paramSigmaErr;\
    Double_t paramStep;\
    Double_t paramStepErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t paramP4;\
    Double_t paramP4Err;\
    Double_t paramP5;\
    Double_t paramP5Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making POW...'
  gROOT.ProcessLine(
  'struct POW{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramAlpha;\
    Double_t paramAlphaErr;\
    Double_t paramBeta;\
    Double_t paramBetaErr;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making EXP2...'
  gROOT.ProcessLine(
  'struct EXP2{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making POWDECAY...'
  gROOT.ProcessLine(
  'struct POWDECAY{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making POWDECAYEXP...'
  gROOT.ProcessLine(
  'struct POWDECAYEXP{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making POWLOG...'
  gROOT.ProcessLine(
  'struct POWLOG{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making LAURENT...'
  gROOT.ProcessLine(
  'struct LAURENT{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making EXPSUM...'
  gROOT.ProcessLine(
  'struct EXPSUM{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making POWEXPSUM...'
  gROOT.ProcessLine(
  'struct POWEXPSUM{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making TRIPEXPSUM...'
  gROOT.ProcessLine(
  'struct TRIPEXPSUM{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t paramP1;\
    Double_t paramP1Err;\
    Double_t paramP2;\
    Double_t paramP2Err;\
    Double_t paramP3;\
    Double_t paramP3Err;\
    Double_t paramP4;\
    Double_t paramP4Err;\
    Double_t paramP5;\
    Double_t paramP5Err;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

  print 'making GEN...'
  gROOT.ProcessLine(
  'struct GEN{\
    Double_t yieldBkg;\
    Double_t yieldBkgErr;\
    Double_t yieldSig;\
    Double_t yieldSigErr;\
    Double_t edm;\
    Double_t minNll;\
    Int_t statusAll;\
    Int_t statusMIGRAD;\
    Int_t statusHESSE;\
    Int_t covQual;\
    Int_t numInvalidNLL;\
  };')

