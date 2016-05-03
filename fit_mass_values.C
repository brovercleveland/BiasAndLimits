//
// Perform an unbinned maximu likelihood to the HZG data.
//
// Michael Schmitt, Northwestern, March 2, 2016
//
#include <iomanip>
#include <math.h>
#include <fstream>
#include <iostream>
#include <algorithm>
#include "TH1D.h"
#include <TMath.h>

const Int_t nEMax = 5000;
Double_t xV[nEMax];
Int_t nE;
const Double_t xa =  150.;
const Double_t xb = 1410.;
const Double_t binwidth = 20.;
const Int_t nbins = Int_t((xb-xa)/binwidth+0.000001);

// mumugamma
/*
const Double_t kStart = 0.013;
const Double_t a1Start =  0.1;
const Double_t a2Start =  0.2;
const Double_t a3Start = -0.15;
const Double_t a4Start =  0.3;
const Double_t a5Start = -0.13;
*/
// eegamma
const Double_t kStart = 0.013;
const Double_t a1Start =  0.056;
const Double_t a2Start =  0.29;
const Double_t a3Start =  0.;
const Double_t a4Start =  0.;
const Double_t a5Start =  0.;

Double_t Laguerre0(Double_t x){return 1;}
Double_t Laguerre1(Double_t x){return (1.-x);}
Double_t Laguerre2(Double_t x){return (x*x-4.*x+2.)/2.;}
Double_t Laguerre3(Double_t x){return (-x*x*x+9.*x*x-18.*x+6.)/6.;}
Double_t Laguerre4(Double_t x){return (pow(x,4)-16.*pow(x,3)+72.*x*x-96.*x+24.)/24.;}
Double_t Laguerre5(Double_t x){return (-pow(x,5)+25.*pow(x,4)-200.*pow(x,3)+600.*x*x-600.*x+120.)/120.;}

Double_t func(Double_t x, Double_t k, Double_t a1, Double_t a2, Double_t a3, Double_t a4, Double_t a5) {
  Double_t u = k*(x-xa);
  Double_t f0 =    Laguerre0(u);
  Double_t f1 = a1*Laguerre1(u);
  Double_t f2 = a2*Laguerre2(u);
  Double_t f3 = a3*Laguerre3(u);
  Double_t f4 = a4*Laguerre4(u);
  Double_t f5 = a5*Laguerre5(u);
  Double_t f = (f0+f1+f2+f3+f4+f5)*k*exp(-u);
  /*
  cout << "func\t" << x << ", " << k << ", " << u << "    \ta1= " << a1
       << "\tL0= " << Laguerre0(u) 
       << "\tL1= " << Laguerre1(u) 
       << "\tf= " << f 
       << "  \t" << f0 << ", " << f1 << ", " << f2 << ", " << f3 << ", " << f4 << ", " << f5 
       << endl;
  */
  return f;
}

Double_t NLL(Double_t k, Double_t a1, Double_t a2, Double_t a3, Double_t a4, Double_t a5) {
  Double_t sum = 0.;
  for (Int_t i=0; i<nE; ++i) {
    Double_t fThis = func(xV[i],k,a1,a2,a3,a4,a5);
    if (fThis > 0) {
      sum -= log(fThis);
    } else {
      sum -= log(-fThis);
    }
  }
  return sum;
}

void fcn(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag){
  Double_t k     = par[0];
  Double_t a1    = par[1];
  Double_t a2    = par[2];
  Double_t a3    = par[3];
  Double_t a4    = par[4];
  Double_t a5    = par[5];
  Double_t sum = NLL(k,a1,a2,a3,a4,a5);
  f = sum;
}

//==================================================
//
// Main Program
//
//==================================================
void fit_mass_values() {
  cout << "\n--------------------------------\n"
       << "\tFit the mass values."
       << "\n--------------------------------\n";
  gROOT->SetStyle("Plain");
  cout << "nbins= " << nbins << endl;
  //

  //
  TH1::SetDefaultSumw2(1);
  TH1D *X_h = new TH1D("X","CMS data;M (GeV);entries per 20 GeV",nbins,xa,xb);
  //
  // Read in data values
  //
  cout << "Open and read data file with mass values.\n";
  //  ifstream DFile("m_mumugamma.csv");
  ifstream DFile("m_eegamma.csv");
  if (!DFile) {
    cout << "Error opening DFile!\n";
    return(1);
  }
  Double_t mass;
  nE = 0;
  while (DFile >> mass) {
    if (mass > xa) {
      X_h->Fill(mass);
      xV[nE] = mass;
      nE++;
      if (nE > nEMax) {
	cout << "nE is larger than array!\n";
	return(1);
      }
    }
  }
  cout << "nE = " << nE << endl;
  //
  // Set up unbinned likelihood fit
  //
  cout << "Set up Minuit.\n";
  const Int_t nP = 6;
  TMinuit *gMinuit = new TMinuit(nP);
  cout << "Set FCN.\n";
  gMinuit->SetFCN(fcn);
  Double_t arglist[10];
  Int_t ierflg = 0;
  arglist[0] = 1;
  cout << "Set ERR.\n";
  gMinuit->mnexcm("SET ERR", arglist ,1,ierflg);
  gMinuit->SetPrintLevel(1);
  //
  // Perform the fit
  //
  Double_t vstart[nP];
  Double_t step[nP];
  /*
  vstart[0] = kStart;
  vstart[1] = a1Start;
  vstart[2] = a2Start;
  vstart[3] = a3Start;
  vstart[4] = a4Start;
  vstart[5] = a5Start;
  step[0] = 0.1*fabs(kStart);
  step[1] = 0.02;
  step[2] = 0.02;
  step[3] = 0.02;
  step[4] = 0.02;
  step[5] = 0.02;
  gMinuit->mnparm(0, "k",     vstart[0], step[0], 0,0 ,ierflg);
  gMinuit->mnparm(1, "a1",    vstart[1], step[1], 0,0 ,ierflg);
  gMinuit->mnparm(2, "a2",    vstart[2], step[2], 0,0 ,ierflg);
  gMinuit->mnparm(3, "a3",    vstart[3], step[3], 0,0 ,ierflg);
  gMinuit->mnparm(4, "a4",    vstart[4], step[4], 0,0 ,ierflg);
  gMinuit->mnparm(5, "a5",    vstart[5], step[5], 0,0 ,ierflg);
  // Now ready for minimization step
  arglist[0] = 500;
  arglist[1] = 1.;
  gMinuit->FixParameter(1);
  gMinuit->FixParameter(2);
  gMinuit->FixParameter(3);
  gMinuit->FixParameter(4);
  gMinuit->FixParameter(5);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->Release(1);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->FixParameter(0);
  gMinuit->Release(2);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->Release(3);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->Release(4);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->Release(5);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  //
  gMinuit->Release(0);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;
  */

  cout << "\n\n\n***************************************************************\n\n"
       << "\t\tSuppress Laguerre 3,4,5\n"
       << "\n\n*****************************************************************\n\n";
  vstart[0] = 0.013;
  vstart[1] = 0.056;
  vstart[2] = 0.29;
  vstart[3] = 0;
  vstart[4] = 0;
  vstart[5] = 0;
  step[0] = 0.1*fabs(kStart);
  step[1] = 0.02;
  step[2] = 0.02;
  step[3] = 0.02;
  step[4] = 0.02;
  step[5] = 0.02;
  gMinuit->mnparm(0, "k",     vstart[0], step[0], 0,0 ,ierflg);
  gMinuit->mnparm(1, "a1",    vstart[1], step[1], 0,0 ,ierflg);
  gMinuit->mnparm(2, "a2",    vstart[2], step[2], 0,0 ,ierflg);
  gMinuit->mnparm(3, "a3",    vstart[3], step[3], 0,0 ,ierflg);
  gMinuit->mnparm(4, "a4",    vstart[4], step[4], 0,0 ,ierflg);
  gMinuit->mnparm(5, "a5",    vstart[5], step[5], 0,0 ,ierflg);
  // Now ready for minimization step
  arglist[0] = 500;
  arglist[1] = 1.;
  gMinuit->FixParameter(3);
  gMinuit->FixParameter(4);
  gMinuit->FixParameter(5);
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);
  cout << "ierflg = " << ierflg << endl;

  //
  // get parameters
  //
  Double_t vpar[nP];
  Double_t vunc[nP];
  for (Int_t i=0; i < nP; i++) {
    gMinuit->GetParameter(i,vpar[i],vunc[i]);
    cout << "\tParameter " << i << ":\t" << vpar[i] << "\t" << vunc[i] << endl;
  }
  //
  Double_t k  = vpar[0];
  Double_t a1 = vpar[1];
  Double_t a2 = vpar[2];
  Double_t a3 = vpar[3];
  Double_t a4 = vpar[4];
  Double_t a5 = vpar[5];
  //
  // Map the function
  //
  TPolyLine *PL;
  Double_t xt = xa;
  const Int_t nPLMax = 500;
  Double_t xPL[nPLMax];
  Double_t yPL[nPLMax];
  Double_t e0PL[nPLMax];
  Double_t e1PL[nPLMax];
  Double_t e2PL[nPLMax];
  Int_t nPL = 0;
  while (xt <= xb) {
    Double_t ft = func(xt,k,a1,a2,a3,a4,a5);
    Double_t yt = ft*Double_t(nE)*binwidth;
    xPL[nPL] = xt;
    yPL[nPL] = yt;
    Double_t u = k*(xt-xa);
    Double_t ef = k*exp(-u);
    yt = Laguerre0(u)*ef*Double_t(nE)*binwidth;
    e0PL[nPL] = yt;
    yt = a1*Laguerre1(u)*ef*Double_t(nE)*binwidth;
    e1PL[nPL] = yt;
    yt = a2*Laguerre2(u)*ef*Double_t(nE)*binwidth;
    e2PL[nPL] = yt;
    /*
    cout << xt << "\t" << yPL[nPL]
	 << "\t" << e0PL[nPL]
	 << "\t" << e1PL[nPL]
	 << "\t" << e2PL[nPL]
	 <<endl;
    */
    nPL++;
    xt += 10.;
  }
  PL = new TPolyLine(nPL,xPL,yPL,"");
  EPL0 = new TPolyLine(nPL,xPL,e0PL,"");
  EPL1 = new TPolyLine(nPL,xPL,e1PL,"");
  EPL2 = new TPolyLine(nPL,xPL,e2PL,"");
  //
  //
  gStyle->SetOptStat(10);
  TCanvas *HX = new TCanvas("HX","X",100,10,1700,1000);
  HX->SetGridx(1);
  HX->SetGridy(1);
  HX->SetLogy(1);
  X_h->SetMinimum(0.008);
  //  X_h->SetMinimum(-40);
  //  X_h->SetMaximum(740);
  X_h->SetMarkerStyle(20);
  X_h->Draw("e");
  PL->Draw("same");
  EPL0->SetLineStyle(2);
  EPL1->SetLineStyle(2);
  EPL2->SetLineStyle(2);
  EPL1->SetLineColor(2);
  EPL2->SetLineColor(4);
  /*
  EPL0->Draw("same");
  EPL1->Draw("same");
  EPL2->Draw("same");
  */
  HX->Print("HX_data.pdf");

  //
  // tail yields
  //
  cout << "\n\n ====================== \n"
       << "    Tail Yields   \n"
       << " ====================== \n\n";

  Double_t sum = 0.;
  xt = 500;
  Double_t dx = 1.;
  while (xt <= xb) {
    Double_t ft = func(xt,k,a1,a2,a3,a4,a5);
    Double_t yt = ft*Double_t(nE);
    sum += yt*dx;
    xt += dx;
  }
  Double_t count = 0;
  for (Int_t i=0; i<nE; ++i) {
    if (xV[i] > 500.) count++;
  }
  cout << "\nThreshold = 500:\tIntegral= " << sum << "\tcount= " << count << endl;

  sum = 0.;
  xt = 600;
  while (xt <= xb) {
    Double_t ft = func(xt,k,a1,a2,a3,a4,a5);
    Double_t yt = ft*Double_t(nE);
    sum += yt*dx;
    xt += dx;
  }
  count = 0;
  for (Int_t i=0; i<nE; ++i) {
    if (xV[i] > 600.) count++;
  }
  cout << "\nThreshold = 600:\tIntegral= " << sum << "\tcount= " << count << endl;


}
