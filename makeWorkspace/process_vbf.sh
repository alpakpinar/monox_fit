#!/bin/bash
set -e
TAG='default'
INDIR=../input/vbf/merged_2020-11-06_vbfhinv_03Sep20v7_jetid_on_endcap
INDIR="$(readlink -e $INDIR)"

OUTDIR="../vbf/$(basename $INDIR)/${TAG}/root"
mkdir -p ${OUTDIR}
OUTDIR="$(readlink -e ${OUTDIR})"

# Save some information so we can trace inputs
INFOFILE=${OUTDIR}/INFO.txt
echo "Input directory: ${INDIR}" > ${INFOFILE}
echo "--- INPUT ---" > ${INFOFILE}

INFILE=${INDIR}/legacy_limit_vbf.root   
WSFILE=${OUTDIR}/ws_vbf.root

# Save the check sum for the input
md5sum ${INFILE} >> ${INFOFILE}

./make_ws.py ${INFILE} --out ${WSFILE} --categories vbf_2017,vbf_2018
./runModel.py ${WSFILE} --categories vbf_2017,vbf_2018 --out ${OUTDIR}/combined_model_vbf.root

# Split for IC
./runModel.py ${WSFILE} --categories vbf_2017 --out ${OUTDIR}/combined_model_vbf_forIC_2017.root --rename "mjj_MTR_2017"
./runModel.py ${WSFILE} --categories vbf_2018 --out ${OUTDIR}/combined_model_vbf_forIC_2018.root --rename "mjj_MTR_2018"

cp sys/vbf_qcd_nckw_ws_201*.root ${OUTDIR}

# Save the check sums for the output
echo "--- OUTPUT ---" >> ${INFOFILE}
md5sum ${OUTDIR}/*root >> ${INFOFILE}

ln -fs $(readlink -e ../vbf/templates/Makefile) ${OUTDIR}/../Makefile

pushd ${OUTDIR}/..
make cards
popd

echo $(readlink -e ${OUTDIR}/..)
