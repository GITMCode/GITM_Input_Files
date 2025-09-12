#!/bin/sh

# set the dates with a restart in the middle:
START=20110803
RESTART=20110805.1800
END=20110808

PID=s2516
SUBDIR=vMSIS_60

# where to find gitm:
GITM=~/Software/GITM

# set number of lat and lon blocks:
LATS=20
LONS=10
CPUS=$((${LATS}*${LONS}))

# time in hours for wall time:
WALLTIME=48

# This is for the post processor on pleiades:
echo "ridley\nmia\n/nobackup/Gitm/Runs/${START}.Storm/${SUBDIR}" > remote

# Make two UAM.in files (start and restart):
${GITM}/srcPython/gitm_makerun.py -gitm=${GITM} -output=UAM.in -imf=find -sme=find -fism -dynamo -fang -fta -nlats=${LATS} -nlons=${LONS} -3dall=300 -2danc=300 -restart -cputimemax=${WALLTIME} -restarttime=${RESTART} ${START} ${END}

# Make another UAM.in file for running with Newell:
#${GITM}/srcPython/gitm_makerun.py -gitm=${GITM} -output=UAM.in.newell -imf=imf${START}.dat -sme=ae${START}.dat -fism -dynamo -fang -newell -nlats=${LATS} -nlons=${LONS} -3dall=300 -2danc=300 -restart -cputimemax=${WALLTIME} ${START} ${END}

# make two job files (start and restart):
# rule of thumb would be 2 days of sim / 24 hours
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job -name=g${START} -wall=${WALLTIME} -gid=${PID} -cpus=${CPUS}
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job.r -name=g${START}r -wall=${WALLTIME} -gid=${PID} -cpus=${CPUS} -restart

