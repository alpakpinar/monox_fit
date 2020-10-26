import ROOT 
import os
import sys
from HiggsAnalysis.CombinedLimit.ModelTools import *

# ============================
# Helper script to create a workspace containing
# QCD histograms.
# ============================

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
pjoin = os.path.join

def create_workspace(fin, fout, category):
    foutdir = fout.mkdir("category_"+category)
    
    wsin_combine = ROOT.RooWorkspace("wspace_"+category,"wspace_"+category)
    wsin_combine._import = SafeWorkspaceImporter(wsin_combine)

    variable_name = 'mjj_{}'.format(category)
    varl = ROOT.RooRealVar(variable_name, variable_name, 0,100000)    

    # Helper function
    def write_obj(obj, name):
        '''Converts histogram to RooDataHist and writes to workspace + ROOT file'''
        print "Creating Data Hist for ", name
        dhist = ROOT.RooDataHist(
                            name,
                            "DataSet - %s, %s"%(category,name),
                            ROOT.RooArgList(varl),
                            obj
                            )
        wsin_combine._import(dhist)

        # Write the individual histograms
        # for easy transfer factor calculation
        # later on
        obj.SetDirectory(0)
        foutdir.cd()
        foutdir.WriteTObject(obj)

    # Get the input histogram
    obj = fin.Get('qcd_{}'.format(category) )
    name = obj.GetName()

    write_obj(obj,name)

    # Write the workspace
    foutdir.cd()
    foutdir.WriteTObject(wsin_combine)
    foutdir.Write()
    fout.Write()

    return wsin_combine

def main():
    # Path to root file containing the QCD histogram
    infile = sys.argv[1]

    fin = ROOT.TFile(infile, 'READ')
    dummy = []
    for category in ['vbf_2017', 'vbf_2018']:
        # Output root file containing the new workspace
        fout = ROOT.TFile('./bu_qcd_{}.root'.format(category), 'RECREATE')

        wsin_combine = create_workspace(fin, fout, category)
        dummy.append(wsin_combine)

    return dummy
if __name__ == '__main__':
    a = main()