#!/bin/sh

# where to find gitm:
GITM=/Users/ridley/Software/GITM

# set the dates with a restart in the middle:
START=20110803
RESTART=20110805.1800
END=20110808

# set number of lat and lon blocks:
LATS=40
LONS=20
let CPUS=${LATS}*${LONS}

# time in hours for wall time:
WALLTIME=72

# This is for the post processor on pleiades:
echo "ridley\nmia\n/nobackup/Gitm/Runs/${START}.Storm/v1" > remote

# Make two UAM.in files (start and restart):
${GITM}/srcPython/gitm_makerun.py -gitm=${GITM} -output=UAM.in -imf=find -sme=find -fism -dynamo -fang -fta -nlats=${LATS} -nlons=${LONS} -3dall=300 -2danc=300 -restart -cputimemax=${WALLTIME} -restarttime=${RESTART} ${START} ${END}

# Make another UAM.in file for running with Newell:
${GITM}/srcPython/gitm_makerun.py -gitm=${GITM} -output=UAM.in.newell -imf=imf${START}.dat -sme=ae${START}.dat -fism -dynamo -fang -newell -nlats=${LATS} -nlons=${LONS} -3dall=300 -2danc=300 -restart -cputimemax=${WALLTIME} ${START} ${END}

# make two job files (start and restart):
# rule of thumb would be 2 days of sim / 24 hours
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job -name=g${START} -wall=${WALLTIME} -gid=s2516 -cpus=${CPUS}
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job.r -name=g${START}r -wall=${WALLTIME} -gid=s2516 -cpus=${CPUS} -restart

