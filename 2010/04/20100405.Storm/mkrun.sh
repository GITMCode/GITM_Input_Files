#!/bin/sh

# set the dates with a restart in the middle:
START=20100404
RESTART=20100405.0600
END=20100408

# ------------------------------------------------------------------

# where to find gitm:
GITM=~/Software/GITM

# set number of lat and lon blocks:
LATS=20
LONS=10
CPUS=$((${LATS}*${LONS}))

# time in hours for wall time:
WALLTIME=24

# This is for the post processor on pleiades:
echo "ridley\nmia\n/nobackup/Gitm/Runs/${START}.Storm/vMSIS_60" > remote

# Make two UAM.in files (start and restart):
${GITM}/srcPython/gitm_makerun.py -gitm=${GITM} -output=UAM.in -imf=find -sme=find -fism -dynamo -nlats=${LATS} -nlons=${LONS} -3dall=300 -2danc=300 -restart -cputimemax=${WALLTIME} -restarttime=${RESTART} ${START} ${END}

# make two job files (start and restart):
# rule of thumb would be 2 days of sim / 24 hours
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job -name=g${START} -wall=${WALLTIME} -gid=s2516 -cpus=${CPUS}
${GITM}/srcPython/gitm_makejob.py -gitm=${GITM} -output=job.r -name=g${START}r -wall=${WALLTIME} -gid=s2516 -cpus=${CPUS} -restart
