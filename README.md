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
    <td>biasStudy_toyMaker.py</td><td>signalCBFits.py</td><td>TBD</td>
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

Bias:
-----
Use `initialFitProducer.py` to generate all the initial inputs for bias study toy-making.

The `biasStudy_toyMaker.py` will then be used, usually in with a batch system, to generate a whole lotta fits.  Output is a simple TTree with branches corresponding to the generated toy data and the test functions.  A multitude of quality checks have been put in place to safegaurd against poor fits with non-physical results.

`plotPulls.py` must be updated to sync with the new naming scheme for the toy files.

`makeTables.py` generates LaTeX tables that highlight the best possible fitting function for a given channel.

Limits:
-------
The `initialFitProducer.py` creates all potential BG fit candidates, including the 'chosen' fits that are used in the analysis.  This macro also stores the unbinned signal distributions, weighted according to their associated scalefactors and scaled to the appropriate yield for their run year.  The outputs for this macro are then fed into the next steps.

`signalCBFits.py` and `bgCardPrep.py` can be run independently, and do not rely any inputs other than that produced in the `initialFitProducer.py` step.  `signalCBFits.py` takes all the unbinned signals and uses a Gaussian+Crystal Ball pdf to fit the distributions.  It also makes interpolations at 0.5 GeV steps, using the available signals (produced with 5 GeV steps).  **The signal fits are not yet tuned and may have converge poorly.**  The naming scheme of the saved fits follows the
necessary Higgs Combination syntax.  `bgCardPrep.py` takes the proper background fits and extends the pdf to produce a seperate normalization term.  The naming scheme is also altered to conform with Higgs Combination syntax.

`cardMaker.py` takes the signal and bg output from the previous step and creates datacards for use with the higgs combination tool.

`limitProducer.py` combines those datacards as specified by the user, and can run the 'combine' tool to produce asymptotic limits for all given mass points. It is recommended that you use `batchLimits.py` to run the calculation for each mass point.  In general, the cards take about 1-5 min to run if it is a single card, ~1 hour for the nominal (published) results, and 2-4 hours for the MVA categorization.

`limitPlotter.py` parses the outputs from the 'combine' tool, and makes nice pretty plots. *This code is not yet updated for new batchmode features, needs minor additions*

Fit Plots:
----------
The `initialFitProducer.py` is used like everything else on this page.  The fits are then fed into the prettyPlotter and something else happens.

