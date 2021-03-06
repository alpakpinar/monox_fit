#!/bin/env python
import os
import sys
sys.path.append(os.path.abspath("../../../plotter"))
from plot_PreFitPostFit import plotPreFitPostFit
from plot_datavalidation import dataValidation
from plot_ratio import plot_ratio
from plot_diffnuis import plot_nuis
lumi ={
    2017 : 41.5,
    2018: 59.7
}
regions = ['singlemuon','dimuon','gjets','singleelectron','dielectron']
procs = ['zmm','zee','w_weights','photon','wen','wmn']

### Years fit separately
ws_file="root/ws_monov_nominal_tight.root"
model_file = "root/combined_model_monov_nominal_tight.root"
for year in [2017,2018]:
    category='monovtight_' + str(year)
    filler = {
        "year" : year,
        "category" : category
    }
    fitdiag_file = 'diagnostics/fitDiagnostics_nominal_{category}.root'.format(**filler)
    diffnuis_file = 'diagnostics/diffnuisances_nominal_{category}.root'.format(**filler)

    outdir = './plots/{year}/'.format(**filler)
    for region in regions:
        plotPreFitPostFit(region,     category,ws_file, fitdiag_file, outdir, lumi[year], year)
    for proc in procs:
        plot_ratio(proc, category, model_file, outdir, lumi[year], year)

    # Flavor integrated
    dataValidation("combined",  "gjets",    category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("combinedW", "gjets",    category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("combined",  "combinedW",category, ws_file, fitdiag_file, outdir,lumi[year],year)
    # Split by flavor
    dataValidation("dimuon",        "singlemuon",    category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("dielectron",    "singleelectron",category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("singleelectron","gjets",         category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("singlemuon",    "gjets",         category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("dielectron",    "gjets",         category, ws_file, fitdiag_file, outdir,lumi[year],year)
    dataValidation("dimuon",        "gjets",         category, ws_file, fitdiag_file, outdir,lumi[year],year)
    plot_nuis(diffnuis_file, outdir)


### Years fit together
filler = {
    "category" : "monovtight"
}
ws_file="root/ws_monov_nominal_tight.root".format(**filler)
fitdiag_file = 'diagnostics/fitDiagnostics_nominal_{category}_combined.root'.format(**filler)
diffnuis_file = 'diagnostics/diffnuisances_nominal_{category}_combined.root'.format(**filler)
model_file = "root/combined_model_monov_nominal_tight.root".format(**filler)

for year in [2017,2018]:
    outdir = './plots/combined_{YEAR}/'.format(YEAR=year)
    category = 'monovtight_{YEAR}'.format(YEAR=year)
    for region in regions:
        plotPreFitPostFit(region,     category,ws_file, fitdiag_file, outdir, lumi[year], year)
    for proc in procs:
        plot_ratio(proc, category, model_file, outdir, lumi[year], year)

outdir = './plots/combined/'
plot_nuis(diffnuis_file, outdir)

