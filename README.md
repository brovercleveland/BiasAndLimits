Updating all roofit-related nonsense for the HZG analysis.  Bias stuides, limit production, plot making (for PAS and papers) will be included here

Flow goes like this:
--------------------
 * Output 3-body mass distributions, unbinned, via the analyzer
 * Run initialFitProducer.py, this will do all BG fits and store the signal distributions

<table>
  <tr>
    <th>Bias</th><th>Limits</th><th>Fit Plots</th>
  </tr>
  <tr>
    <td>biasStudy_toyMaker.py</td><td>signalFits.py</td><td>TBD</td>
  </tr>
  <tr>
    <td>plotPulls.py</td><td>bgCardPrep.py</td><td>TBD</td>
  </tr>
  <tr>
    <td>makeTables.py</td><td>cardMaker.py</td><td>TBD</td>
  </tr>
  <tr>
    <td>TBD</td><td>limitProducer.py</td><td>TBD</td>
  </tr>
  <tr>
    <td>TBD</td><td>limitPlotter.py</td><td>TBD</td>
  </tr>
</table>

Parameters for all scripts are set in `configLimits.py`

Bias:
-----

Use `initialFitProducer.py` to generate all the initial inputs for bias study toy-making.

The `biasStudy_toyMaker.py` will then be used, usually in with a batch system, to generate a whole lotta fits.  Output is a simple TTree with branches corresponding to the generated toy data and the test functions.  A multitude of quality checks have been put in place to safegaurd against poor fits with non-physical results. `batchBias.py` and `biasCombine.py` used for producing and finishing bias study outputs.

`plotPulls.py` produces most relevant metrics for use in bias studies.  The Type-A metric is used for final determination of bias (n(sig)/err(bg))

`makeTables.py` generates LaTeX tables that highlight the best possible fitting function for a given channel.

Limits:
-------
The `initialFitProducer.py` creates all potential BG fit candidates, including the 'chosen' fits that are used in the analysis.  This macro also stores the unbinned signal distributions, weighted according to their associated scalefactors and scaled to the appropriate yield for their run year.  The outputs for this macro are then fed into the next steps. The fit building and management is handled by the class located in `rooFitBuilder.py`.

`signalFits.py` and `bgCardPrep.py` can be run independently, and do not rely any inputs other than that produced in the `initialFitProducer.py` step.  `signalFits.py` takes all the unbinned signals and uses a Gaussian+Crystal Ball (or triple gaussian) pdf to fit the distributions.  It also makes interpolations at 0.5 (or 0.1 near M125) GeV steps, using the available signals (produced with 5 GeV steps).  The naming scheme of the saved fits follows the
necessary Higgs Combination syntax.  `bgCardPrep.py` takes the proper background fits and extends the pdf to produce a seperate normalization term.  Fit functions and renaming schemes are located in `rooFitBuilder.py`.
The naming scheme is also altered to conform with Higgs Combination syntax. `batchSignals.py` handles large-scale signal fitting operations.

`cardMaker.py` takes the signal and bg output from the previous step and creates datacards for use with the higgs combination tool.

`limitProducer.py` combines those datacards as specified by the user, and can run the 'combine' tool to produce asymptotic limits for all given mass points. It is recommended that you use `batchLimits.py` to run the calculation for each mass point.  In general, the cards take about 1-5 min to run if it is a single card, ~1 hour for the nominal (published) results, and 2-4 hours for the MVA categorization. The time increases greatly with the number of channels for a given mass point.

`limitPlotter.py` parses the outputs from the 'combine' tool, and makes nice pretty plots.

Fit Plots:
----------
The `initialFitProducer.py` is used like everything else on this page.  The fits are then fed into the prettyPlotter, not yet updated.

