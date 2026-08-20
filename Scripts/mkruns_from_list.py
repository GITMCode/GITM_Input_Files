#!/usr/bin/env python3

import os
import argparse
import re

# ----------------------------------------------------------------------
# Function to parse input arguments
# ----------------------------------------------------------------------

def parse_args():

    parser = argparse.ArgumentParser(description = \
                                     'Runs gitm_makerun for a list of times')

    home = '/home/ridley/Software'
    
    parser.add_argument('-list', \
                        help = 'file that contains list of dates', \
                        default = 'run_list.txt')

    parser.add_argument('-gitm', \
                        help = 'path to gitm code', \
                        default = home + '/GITM')

    parser.add_argument('-outpath', \
                        help = 'output path (/YYYY/MM/YYYYMMDD.Type added)', \
                        default = home + '/GITM/GITM_Input_Files')

    parser.add_argument('-pid', \
                        help = 'PID for Athena / Pleiades', \
                        default = 's3140')

    parser.add_argument('-name', \
                        help = 'name for sequence of runs', \
                        default = 'vBaseline')

    # Grid stuff
    parser.add_argument('-nlats', type = int, \
                        help = 'set number of latitude blocks',
                        default = 16)
    parser.add_argument('-nlons', type = int, \
                        help = 'set number of longitude blocks',
                        default = 16)

    parser.add_argument('-walltime', type = int, \
                        help = 'set walltime for simulation',
                        default = -1)

    parser.add_argument('-dtplot', type = int, \
                        help = 'Set dt for outputting plots during storm',
                        default = -1)

    # These are for the remote file for the post_processor
    parser.add_argument('-remoteuser', \
                        help = 'userID for remote file', \
                        default = 'none')
    parser.add_argument('-remotehost', \
                        help = 'hostname for remote file', \
                        default = 'none')
    parser.add_argument('-remotedir', \
                        help = 'base directory for remote file', \
                        default = 'none')

    parser.add_argument('-jobfile', \
                        help = 'baseline job file', \
                        default = '../Pleiades/job_athena')

    parser.add_argument('-v', \
                        help='turn on verbose', \
                        action="store_true")
    
    args = parser.parse_args()
    
    return args

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def write_remote_file(outfile, user, host, dir):

    if (user != 'none'):
        fp = open(outfile, 'w')
        fp.write(user + "\n")
        fp.write(host + "\n")
        fp.write(dir + "\n")
        fp.close()
        didWrite = True
    else:
        didWrite = False

    return didWrite

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def read_list_file(file):

    fp = open(file, 'r')
    allLines = fp.readlines()
    fp.close()
    
    runList = []
    
    iLine = 0
    nLines = len(allLines)
    while iLine < nLines:
        line = allLines[iLine].strip()
        m = re.match(r'(.*):', line)
        if m:
            indicator = m.group(1)
        m = re.match(r'.*(\d\d\d\d).(\d\d).(\d\d)....(\d\d\d\d).(\d\d).(\d\d)', line)
        if m:
            start = m.group(1) + m.group(2) + m.group(3)
            end = m.group(4) + m.group(5) + m.group(6)
            yyyy = m.group(1)
            mm = m.group(2)
            dd = m.group(3)
            doRestart = False
            restart = ''
            dirDate = start
            m2 = re.match(r'.*restart (\d\d\d\d)-(\d\d)-(\d\d).(\d\d)', line)
            if m2:
                restart = \
                    m2.group(1) + m2.group(2) + m2.group(3) + '.' + m2.group(4) 
                doRestart = True
                dirDate = m2.group(1) + m2.group(2) + m2.group(3)
                mm = m2.group(2)
                dd = m2.group(3)
            else:
                m3 = re.match(r'.*restart (\d\d\d\d)-(\d\d)-(\d\d)', line)
                if m3:
                    restart = \
                        m3.group(1) + m3.group(2) + m3.group(3) + '.00' 
                    doRestart = True
                    dirDate = m2.group(1) + m2.group(2) + m2.group(3)
                    mm = m3.group(2)
                    dd = m3.group(3)
            run = {'indicator': indicator,
                   'start': start,
                   'end': end,
                   'year': yyyy,
                   'month': mm,
                   'day': dd,
                   'doRestart': doRestart,
                   'restart': restart,
                   'dirDate': dirDate}
            runList.append(run)
        iLine = iLine + 1
    
    return runList

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def run_command(command, verbose = False):
    if (verbose):
        print("   -> Running Command : ")
        print("      ", command)
    os.system(command)
    return True

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

args = parse_args()

listFile = args.list
isVerbose = args.v

outPathSave = args.outpath
if (not os.path.exists(outPathSave)):
    print('Output path does not exist : ', outPathSave)
    print(' -> Need a -outpath=loc for the output')
    exit()

runList = read_list_file(listFile)

nRuns = len(runList)
print('Found %d runs...' % nRuns)

if (not os.path.isfile('UAM.in')):
    print('  --> Found old UAM.in file, saving')
    command = 'mv UAM.in UAM.in.Save'
    run_command(command, verbose = isVerbose)

for run in runList:

    print('Processing Time : ', run['start'])

    # -----------------------------------------------------------
    print('  --> Removing any files that may get in the way')

    command = 'rm -f UAM.in UAM.in.Start UAM.in.Restart'
    run_command(command, verbose = isVerbose)
    
    command = 'rm -f ae*dat imf*dat'
    run_command(command, verbose = isVerbose)
    
    command = 'rm -f remote'
    run_command(command, verbose = isVerbose)
    
    # -----------------------------------------------------------
    print('  --> Checking for output directory')
    dir = run['dirDate'] + '.' + run['indicator'] + '/' + args.name
    outPath = outPathSave + '/' + run['year']
    if (not os.path.exists(outPath)):
        print('  -> need to make directory : ', outPath)
        command = 'mkdir ' + outPath
        run_command(command, verbose = isVerbose)
    outPath = outPath + '/' + run['month']
    if (not os.path.exists(outPath)):
        print('  -> need to make directory : ', outPath)
        command = 'mkdir ' + outPath
        run_command(command, verbose = isVerbose)
    outPath = outPath + '/' + \
        run['year'] + run['month'] + run['day'] + '.' + run['indicator']
    if (not os.path.exists(outPath)):
        print('  -> need to make directory : ', outPath)
        command = 'mkdir ' + outPath
        run_command(command, verbose = isVerbose)
    else:
        print('  -> directory exists: ', outPath)
        
    # -----------------------------------------------------------
    print('  --> Making remote file, if asked for')
    remoteFile = 'remote'
    remoteDir = args.remotedir + '/' + dir
    didWriteRemote = write_remote_file(remoteFile, \
                                       args.remoteuser, \
                                       args.remotehost, \
                                       remoteDir)

    # -----------------------------------------------------------
    print('  --> Building gitm_makerun command')
    makerun = args.gitm + '/srcPython/gitm_makerun.py -gitm=' + args.gitm + ' '
    makerun = makerun + '-output=UAM.in '
    makerun = makerun + '-imf=find '
    makerun = makerun + '-sme=find '
    makerun = makerun + '-fism -dynamo '
    makerun = makerun + '-nlons=%d ' % args.nlons
    makerun = makerun + '-nlats=%d ' % args.nlats
    dtplot = args.dtplot
    if (dtplot <= 0):
        dtplot = 900
    makerun = makerun + '-3dall=%d ' % dtplot
    makerun = makerun + '-2danc=%d ' % dtplot
    if (args.walltime > 0):
        makerun = makerun + '-cputimemax=%d ' % args.walltime
    if (run['doRestart']):
        makerun = makerun + '-restart -restarttime=' + run['restart'] + ' '
    makerun = makerun + run['start'] + ' '
    makerun = makerun + run['end'] + ' '
    run_command(makerun, verbose = isVerbose)
    
    # -----------------------------------------------------------
    print('  --> Building gitm_makejob command')

    makejob = args.gitm + '/srcPython/gitm_makejob.py -gitm=' + args.gitm + ' '
    if (args.walltime > 0):
        makejob = makejob + '-wall=%d ' % args.walltime
    nCpus = args.nlons * args.nlats
    makejob = makejob + '-cpus=%d ' % nCpus
    makejob = makejob + '-gid=' + args.pid + ' '
    makejob = makejob + '-input=' + args.jobfile + ' '
    makejobBase = makejob

    makejob = makejobBase + '-output=job -name=g' + run['start']
    run_command(makejob, verbose = isVerbose)
    if (run['doRestart']):
        makejob = makejobBase + '-output=job.r -name=g' + run['start'] + 'r '
        makejob = makejob + '-restart'
        run_command(makejob, verbose = isVerbose)

    # -----------------------------------------------------------
    print('  --> Moving files into output directory')
    if (run['doRestart']):
        command = 'mv UAM.in.Start UAM.in.Restart'
    else:
        command = 'mv UAM.in.Start'
    command = command + ' ' + outPath
    run_command(command, verbose = isVerbose)

    command = 'mv ae*.dat imf*.dat '
    command = command + outPath
    run_command(command, verbose = isVerbose)
 
    if (didWriteRemote):
        command = 'mv remote '
        command = command + outPath
        run_command(command, verbose = isVerbose)
 
    command = 'mv job* '
    command = command + outPath
    run_command(command, verbose = isVerbose)

