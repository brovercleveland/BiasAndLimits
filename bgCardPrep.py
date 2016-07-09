#!/usr/bin/env python
import sys
sys.argv.append('-b')
import ROOT
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import configLimits as cfl
import CMS_lumi

#gROOT.ProcessLine('.L ./CMSStyle.C')
#CMSStyle()

doMVA = cfl.doMVA
doExt = cfl.doExt
suffixCard = cfl.suffixPostFix

leptonList = cfl.leptonList
tevList = cfl.tevList
catListSmall = cfl.catListSmall
catListBig = cfl.catListBig

YR = cfl.YR
sigFit = cfl.sigFit
highMass = cfl.highMass
blind = cfl.blind
doFancy = cfl.doFancy
logy=True


#rooWsFile = TFile('testRooFitOut_Poter.root')
rooWsFile = TFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffixCard+'.root')
myWs = rooWsFile.Get('ws')
card_ws = RooWorkspace('ws_card')
#card_ws.autoImportClassCode(True)
outfile = TFile('fit_plots.root',"recreate")

#c = TCanvas("c","c",0,0,550,400)
#c.cd()


mzg = myWs.var('CMS_hzg_mass')
mzg.setRange('signal',120,130)

########################################
# prep the background and data card        #
# we're going to the extend the bg pdf #
# and rename the parameters to work        #
# with the higgs combination tool            #
########################################


for tev in tevList:
    for lepton in leptonList:
        if tev == '8TeV' and doMVA: catList = catListBig
        else: catList = catListSmall
        for cat in catList:
            if cat is '5' and tev is '7TeV' and lepton is 'mu': continue
            elif cat is '5' and tev is '7TeV' and lepton is 'el': lepton = 'all'

            canv = ROOT.TCanvas('c','c',550,600)
            if logy:
                    legend = ROOT.TLegend(0.65,0.55,0.9,0.9)
                    #legend = ROOT.TLegend(0.17,0.11,0.5,0.5)
            else:
                    legend = ROOT.TLegend(0.4,0.5,0.9,0.9)
                    ## legend = ROOT.TLegend(0.4,0.35,0.9,0.9)

            canv.Divide(1,2)

            canv.cd(1)
            ROOT.gPad.SetPad(0.,0.38,1.,0.95)
            ROOT.gPad.SetLeftMargin(0.12),ROOT.gPad.SetRightMargin(0.05),ROOT.gPad.SetTopMargin(0.0015),ROOT.gPad.SetBottomMargin(0.02)
            ROOT.gPad.SetLogy(logy)
            ROOT.gPad.SetFillStyle(0)
            ROOT.gPad.SetTickx()

            canv.cd(2)
            ROOT.gPad.SetPad(0.,0.,1.,0.38)
            ROOT.gPad.SetFillStyle(0)
            ROOT.gPad.SetLeftMargin(0.12),ROOT.gPad.SetRightMargin(0.05),ROOT.gPad.SetTopMargin(0.0015),ROOT.gPad.SetBottomMargin(0.32)
            ROOT.gPad.SetFillStyle(0)
            ROOT.gPad.SetTickx()

            canv.cd(1)

            dataName = '_'.join(['data',lepton,tev,'cat'+cat])
            suffix = '_'.join([tev,lepton,'cat'+cat])

            fitNameHeader = cfl.bgLimitDict[highMass][tev][lepton][cat]
            #fitNameHeader = 'ExpSum'
            fitName = fitNameHeader+'_'+suffix
            normName = 'norm'+fitName

            data = myWs.data(dataName)
            data.Print()
            print fitName
            fit = myWs.pdf(fitName)
            #p1 = myWs.var('p1TripExpSumv2_8TeV_'+lepton+'_cat0')
            #p2 = myWs.var('p2TripExpSumv2_8TeV_'+lepton+'_cat0')
            #p3 = myWs.var('p3TripExpSumv2_8TeV_'+lepton+'_cat0')
            #p4 = myWs.var('p4TripExpSumv2_8TeV_'+lepton+'_cat0')
            #p5 = myWs.var('p5TripExpSumv2_8TeV_'+lepton+'_cat0')
            #p6 = myWs.var('p6TripExpSumv2_8TeV_'+lepton+'_cat0')
            fit.Print()
            #p6.Print()
            #p1.setConstant(True)
            #p2.setConstant(True)
            #p3.setConstant(False)
            #p4.setConstant(True)
            #p5.setConstant(True)
            #p6.setConstant(False)
            #raw_input()

            ###### Extend the fit (give it a normalization parameter)
            print dataName
            sumEntries = data.sumEntries()
            sumEntriesS = data.sumEntries('1','signal')
            print sumEntries, sumEntriesS
            #raw_input()
            dataYieldName = '_'.join(['data','yield',lepton,tev,'cat'+cat])
            dataYield = RooRealVar(dataYieldName,dataYieldName,sumEntries)
            if doExt:
                norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.1,sumEntries*2)
                print 'start', norm.getVal()
                fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
                fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)
                #fit_ext = fit

                fit_ext.fitTo(data,RooFit.Range('fullRegion'))

                testFrame = mzg.frame()
                data.plotOn(testFrame)
                fit_ext.plotOn(testFrame)
                testFrame.Draw('e0')
                canv.Print('debugPlots/'+'_'.join(['test','data','fit',lepton,tev,'cat'+cat])+'.pdf')
                print 'end', norm.getVal()
            else:
                norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.9,sumEntries*1.1)
                #norm = RooRealVar(normName,normName,sumEntries,sumEntries*0.8,sumEntries*1.2)


            ###### Import the fit and data, and rename them to the card convention

            dataNameNew = '_'.join(['data','obs',lepton,tev,'cat'+cat])
            dataYieldNameNew = '_'.join(['data','yield',lepton,tev,'cat'+cat])
            dataYield.SetName(dataYieldNameNew)

            getattr(card_ws,'import')(data,RooFit.Rename(dataNameNew))
            if doExt:
                getattr(card_ws,'import')(fit_ext)
            else:
                getattr(card_ws,'import')(fit)
                normNameFixed    = '_'.join(['bkg',lepton,tev,'cat'+cat,'norm'])
                norm.SetName(normNameFixed)
                getattr(card_ws,'import')(norm)
            getattr(card_ws,'import')(dataYield)
            card_ws.commitTransaction()
            #fit_ext.Print()
            fitBuilder = FitBuilder(mzg,tev,lepton,cat)
            fitBuilder.BackgroundNameFixer(card_ws,fitNameHeader,doExt)

            if doFancy:
                #canv.SetTopMargin(0.075);
                ######################
                # making fancy plots #
                ######################

                fitExtName = '_'.join(['bkgTmp',lepton,tev,'cat'+cat])
                fit_ext = RooExtendPdf(fitExtName,fitExtName, fit,norm)
                #fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minos(RooArgSet(norm)), RooFit.Minimizer("Minuit2"))
                #fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minos(RooArgSet(norm)), RooFit.Minimizer("Minuit"))
                fit_res = None
                if lepton == 'mu':
                    #fit_res = fit_ext.fitTo(data,RooFit.Range('reduced'), RooFit.Save(), RooFit.Strategy(0), RooFit.Extended(), RooFit.InitialHesse(True), RooFit.Minos(True), RooFit.Minimizer("Minuit"))

                    fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(0), RooFit.Minos(False), RooFit.Extended())
                else:
                    #fit_res = fit_ext.fitTo(data,RooFit.Range('reduced'), RooFit.Save(), RooFit.Strategy(0), RooFit.Extended(), RooFit.InitialHesse(True), RooFit.Minos(True), RooFit.Minimizer("Minuit"))

                    fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(0), RooFit.Minos(False), RooFit.Extended())
                    #fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(1), RooFit.InitialHesse(True), RooFit.Extended())
                    #fit_res = fit_ext.fitTo(data,RooFit.Range('full'), RooFit.Save(), RooFit.Strategy(2), RooFit.Extended(), RooFit.Minimizer("Minuit"))
                    #fit_res = fit_ext.fitTo(data,RooFit.Range('reduced'), RooFit.Save(), RooFit.Strategy(0), RooFit.Extended(), RooFit.InitialHesse(True), RooFit.Minos(True), RooFit.Minimizer("Minuit"))

                testFrame = mzg.frame(RooFit.Range('reduced'))
                residFrame = mzg.frame(RooFit.Range('reduced'))
                binning = (cfl.bgRange[1]-cfl.bgRange[0])/20

                if blind:
                    data.plotOn(testFrame,RooFit.Binning(3,cfl.bgRange[0],cfl.blindRange[1]),RooFit.Name('data'),RooFit.MarkerSize(0.5))
                    data.plotOn(testFrame,RooFit.Binning(5,cfl.blindRange[1],cfl.bgRange[1]),RooFit.Name('data'), RooFit.MarkerSize(0.5))
                    data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.Invisible())
                else:
                    data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Range('reduced'),RooFit.Name('data'),RooFit.MarkerSize(1.1),RooFit.XErrorSize(0),RooFit.DataError(RooAbsData.Poisson),RooFit.Invisible())

                linearInterp = True
                #fit_ext.plotOn(testFrame, RooFit.Name(fitExtName+"2sigma"),
                #                     RooFit.VisualizeError(fit_res,2, linearInterp), RooFit.FillColor(kYellow),RooFit.LineColor(kBlack))
                #                     #RooFit.VisualizeError(fit_res,RooArgSet(p1,p4),2,False), RooFit.FillColor(kYellow),RooFit.LineColor(kBlack))

                fit_ext.plotOn(testFrame,RooFit.Name(fitExtName+"1sigma"),
                                     RooFit.VisualizeError(fit_res,1, linearInterp), RooFit.FillColor(17), RooFit.LineColor(17))
                                     #RooFit.VisualizeError(fit_res,RooArgSet(p1,p4),1,False), RooFit.FillColor(kGreen),RooFit.LineColor(kBlack))
                fit_ext.plotOn(testFrame,RooFit.Name(fitExtName), RooFit.LineColor(46), RooFit.LineWidth(2))

                if blind:
                    data.plotOn(testFrame,RooFit.Binning(3,cfl.bgRange[0],cfl.blindRange[1]),RooFit.Name('data'),RooFit.MarkerSize(0.5))
                    data.plotOn(testFrame,RooFit.Binning(5,cfl.blindRange[1],cfl.bgRange[1]),RooFit.Name('data'), RooFit.MarkerSize(0.5))
                    data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'),RooFit.Invisible())
                else:
                    data.plotOn(testFrame,RooFit.Binning(binning),RooFit.Range('full'),RooFit.Name('data'),RooFit.MarkerSize(1.1),RooFit.XErrorSize(0),RooFit.DataError(RooAbsData.Poisson))

                central = testFrame.findObject(fitExtName)
                onesigma = testFrame.findObject(fitExtName+"1sigma")
                #onesigma.Dump()
                hist = testFrame.findObject('data')
                ronesigma = TGraphAsymmErrors(hist.GetN())

                ifit = 0
                for idata in range(hist.GetN()):

                    hx = hist.GetX()[idata]
                    hy = hist.GetY()[idata]
                    while(abs(central.GetX()[ifit]-hx)>0.2): ifit+=1
                    px = central.GetX()[ifit]
                    py = central.GetY()[ifit]
                    ronesigma.SetPoint(idata,hx,0.)
                    #raw_input()



                    oerrp, oerrm = onesigma.GetY()[onesigma.GetN()-1-ifit]-py, py-onesigma.GetY()[ifit]
                    herrp, herrm = hist.GetErrorYhigh(idata), hist.GetErrorYlow(idata)
                    #oerrp = oerrm = onesigma.GetY()[onesigma.GetN()-1-ifit]-py
                    #herrp = herrm = hist.GetErrorYhigh(idata)
                    print 'idata', idata, 'ifit', ifit
                    print 'datax', hx, 'fitx', px
                    print 'datay', hy, 'fity', py
                    print 'dataEH', herrp, 'fitEH',oerrp
                    print 'dataEL', herrm, 'fitEL',oerrm
                    #raw_input()

                    #print oerrp, oerrm, herrp, herrm
                    #raw_input()
                    ## print oerrp, oerrm, herrp, herrm
                    #if py > hy:
                    #    if herrm == 0.: continue
                    #    oerrp /= herrm
                    #    oerrm /= herrm
                    #else:
                    #    if herrp == 0.: continue
                    #    oerrp /= herrp
                    #    oerrm /= herrp

                    if py > hy:
                        if herrm != 0.:
                            oerrp /= herrm
                            oerrm /= herrm
                    else:
                        if herrp != 0.:
                            oerrp /= herrp
                            oerrm /= herrp
                    ## print oerrp, oerrm, herrp, herrm
                    #print ip,oerrp,oerrm
                    print px, oerrp,oerrm
                    #raw_input()
                    if idata==0:
                        exl=0
                    else:
                        exl = (hx - hist.GetX()[idata-1])/2.0
                    if idata == hist.GetN()-1:
                        exh = 0
                    else:
                        exh = (hist.GetX()[idata+1]-hx)/2.0
                    if exl==0: exl = exh
                    if exh==0: exh = exl
                    ronesigma.SetPointEYhigh(idata,max(oerrp,oerrm)),ronesigma.SetPointEYlow(idata,max(oerrm,oerrp))
                    #ronesigma.SetPointEYhigh(idata,oerrp),ronesigma.SetPointEYlow(idata,oerrm)
                    ronesigma.SetPointEXhigh(idata,exh),ronesigma.SetPointEXlow(idata,exl)
                    #ronesigma.SetPointEYhigh(idata,1),ronesigma.SetPointEYlow(idata,1)

                residHist = testFrame.residHist('data',fitExtName,True)
                for ip in range(hist.GetN()):
                    # set 0 bins to 0 error bars, why i have to fucking do this by hand is beyond me
                    hy = hist.GetY()[ip]
                    if hy ==0:
                        hist.SetPointEYhigh(ip,0)
                        hist.SetPointEYlow(ip,0)


                testFrame.GetXaxis().SetLabelFont(42)
                testFrame.GetXaxis().SetTitleFont(42)
                testFrame.GetXaxis().SetLabelSize( 1.5*testFrame.GetXaxis().GetLabelSize() )
                testFrame.GetXaxis().SetTitleSize( 1.2*testFrame.GetXaxis().GetTitleSize() )
                testFrame.GetXaxis().SetTitleOffset(0.8)

                testFrame.GetYaxis().SetLabelFont(42)
                testFrame.GetYaxis().SetTitleFont(42)
                testFrame.GetYaxis().SetLabelSize( testFrame.GetXaxis().GetLabelSize() * canv.GetWh() / ROOT.gPad.GetWh() * 1.3 )
                testFrame.GetYaxis().SetTitleSize( testFrame.GetXaxis().GetTitleSize() * canv.GetWh() / ROOT.gPad.GetWh() * 1.8 )
                testFrame.GetYaxis().SetTitleOffset(0.75)
                testFrame.GetXaxis().SetNdivisions(1005, False)
                testFrame.SetMinimum(0.02)
                testFrame.SetMaximum(1500)
                testFrame.GetXaxis().SetTitle("")
                testFrame.Draw()
                #hist.Draw('sameep')
                legend.AddEntry(testFrame.findObject('data'),"Data","pe")
                legend.AddEntry(testFrame.findObject(fitExtName),"Fit","l")
                legend.AddEntry(testFrame.findObject(fitExtName+'1sigma'),"Uncertainty","f")
                legend.SetFillColor(ROOT.kWhite)
                legend.SetFillStyle(0)
                legend.SetTextSize(0.07)
                legend.SetTextFont(42)
                legend.SetShadowColor(ROOT.kWhite)
                legend.SetBorderSize(0)

                legend.Draw("same")

                #testFrame.GetXaxis().SetTitleFont(42)
                #testFrame.GetYaxis().SetTitleFont(42)
                #testFrame.GetXaxis().SetLabelFont(42)
                #testFrame.GetYaxis().SetLabelFont(42)

                if lepton=='mu':
                    testFrame.SetTitle(";m_{#mu#mu#gamma} (GeV);Events / ( "+str(20)+" GeV )")
                elif lepton=='el':
                    testFrame.SetTitle(";m_{ee#gamma} (GeV);Events / ( "+str(20)+" GeV )")
                #testFrame.GetYaxis().CenterTitle()

                ronesigma.SetMarkerStyle(21)
                ronesigma.SetMarkerColor(4)
                ronesigma.SetFillColor(17)
                ronesigma.SetFillStyle(1001)
                #ronesigma.SetDrawOption("2")
                residFrame.addObject(ronesigma,"2")
                one = ROOT.TLine(150,0,1400,0)
                one.SetLineColor(46)
                one.SetLineWidth(2)
                residFrame.addObject(one)
                residFrame.addPlotable(residHist,"PE")
                canv.cd(2)
                ROOT.gPad.SetGridy()
                #ROOT.gPad.SetLogx(logx)
                ROOT.gPad.RedrawAxis()

                residFrame.SetTitle('')
                residFrame.GetXaxis().SetLabelFont(42)
                residFrame.GetXaxis().SetTitleFont(42)
                residFrame.GetXaxis().SetMoreLogLabels()
                residFrame.GetXaxis().SetNoExponent()
                #residFrame.GetXaxis().SetNdivisions(515)
                residFrame.GetXaxis().SetNdivisions(1005, False)
                residFrame.GetYaxis().SetNdivisions(505)
                residFrame.GetYaxis().CenterTitle()
                residFrame.GetYaxis().SetTitleSize    ( testFrame.GetYaxis().GetTitleSize() * 1.5 )
                residFrame.GetYaxis().SetTitleOffset( testFrame.GetYaxis().GetTitleOffset() * 0.5    ) # not clear why the ratio should be upside down, but it does
                residFrame.GetYaxis().SetLabelFont(42)
                residFrame.GetYaxis().SetTitleFont(42)
                residFrame.GetYaxis().SetLabelSize( testFrame.GetYaxis().GetLabelSize() * 1.3 )
                residFrame.GetXaxis().SetTitleSize( testFrame.GetXaxis().GetTitleSize() * 3. )
                residFrame.GetXaxis().SetTitleOffset( testFrame.GetXaxis().GetTitleOffset()*1.2 )
                residFrame.GetXaxis().SetLabelSize( testFrame.GetXaxis().GetLabelSize() * 6.5/3.5 )
                if lepton=="el": residFrame.SetXTitle("M(e^{+}e^{-}#gamma) [GeV]")
                if lepton=="mu": residFrame.SetXTitle("M(#mu^{+}#mu^{-}#gamma) [GeV]")
                ## residFrame.GetYaxis().SetTitle("(data - model) / #sigma_{data}")
                ## residFrame.GetYaxis().SetTitle("(data-fit)/#sigma_{data}")
                residFrame.GetYaxis().SetTitle("(data-fit)/#sigma_{stat}")
                residFrame.GetYaxis().SetRangeUser( -2.5, 2.5 )
                residFrame.Draw()
                testFrame.GetXaxis().SetLabelSize(0.)
                #ronesigma.Draw('4')

                #leg    = TLegend(0.2,0.2,0.6,0.45)
                #leg    = TLegend(0.3,0.7,0.5,0.9)
                #leg.SetFillColor(0)
                #leg.SetFillStyle(0)
                #leg.SetBorderSize(0)
                #leg.SetTextFont(42)
                #if lepton=='el':
                #    leg.SetHeader('pp#rightarrow ee#gamma')
                #else:
                #    leg.SetHeader('pp#rightarrow #mu#mu#gamma')
                #leg.AddEntry(testFrame.findObject(fitExtName),"Background Model",'l')
                #leg.AddEntry(testFrame.findObject(fitExtName+'1sigma'),"#pm 1 #sigma",'f')
                #leg.AddEntry(testFrame.findObject(fitExtName+'2sigma'),"#pm 2 #sigma",'f')
                #leg.SetTextSize(0.042)
                #leg.Draw()
                canv.cd()
                ## legend.AddEntry(None,"%s category" % label.split("_")[-1],"")
                #legend.AddEntry(hist,"MC","pe")

                label_lumi = ROOT.TPaveText(0.4,0.953,0.975,0.975, "brNDC")
                label_lumi.SetBorderSize(0)
                label_lumi.SetFillColor(ROOT.kWhite)
                label_lumi.SetTextSize(0.038)
                label_lumi.SetTextAlign(31)
                label_lumi.SetTextFont(42)
                label_lumi.AddText( "19.7 fb^{-1} (8 TeV)")
                label_lumi.Draw("same")

                label_cms = ROOT.TPaveText(0.12,0.96,0.27,0.965, "brNDC")
                label_cms.SetBorderSize(0)
                label_cms.SetFillColor(ROOT.kWhite)
                label_cms.SetTextSize(0.042)
                label_cms.SetTextAlign(11)
                label_cms.SetTextFont(42)
                #label_cms.SetTextFont(61)
                #label_cms.AddText( "CMS" )
                label_cms.AddText( "CMS" )
                label_cms.Draw("same")

                #lat1 = TLatex()
                #lat1.SetNDC()
                #lat1.SetTextSize(0.040)
                #if lepton=='el':
                #    lat1.DrawLatex(0.18,0.95, 'A #rightarrowZ#gamma#rightarrow ee#gamma')
                #else:
                #    lat1.DrawLatex(0.18,0.95, 'A #rightarrowZ#gamma#rightarrow#mu#mu#gamma')

                #lat2 = TLatex()
                #lat2.SetNDC()
                #lat2.SetTextSize(0.040)
                #lat2.DrawLatex(0.40,0.95, 'CMS Preliminary')

                #CMS_lumi.relPosX = 0.08
                #CMS_lumi.CMS_lumi(c,2,33)

                gPad.RedrawAxis()
                outfile.cd()
                canv.SetName(lepton)
                canv.Write()
                if blind:
                    canv.Print('debugPlots/fancyPlots/'+'_'.join(['PAS','fit','blind',suffixCard,tev,lepton,'cat'+cat])+'.pdf')
                else:
                    #c.Print('debugPlots/fancyPlots/'+'_'.join(['PAS','fit','partial3',suffixCard,tev,lepton,'cat'+cat])+'.pdf')
                    #canv.Print('debugPlots/fancyPlots/'+'_'.join(['PASCombo','fit',suffixCard,tev,lepton,'cat'+cat])+'.pdf')
                    canv.Print('debugPlots/paperPlots/'+'_'.join(['PaperCombo','fit',lepton])+'.pdf')
                    #canv.Print('debugPlots/paperPlots/'+'_'.join(['PASCombo','fit',lepton])+'.pdf')

card_ws.writeToFile('outputDir/'+suffixCard+'_'+YR+'_'+sigFit+'/CardBackground_'+suffixCard+'.root')
outfile.Close()






