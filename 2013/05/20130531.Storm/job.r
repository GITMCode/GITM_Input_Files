#!/bin/csh
#PBS -S /bin/csh
#PBS -N g20130529r
#PBS -lselect=40:ncpus=20:model=ivy
#PBS -l walltime=72:00:00

# the group list is the GID of the project:
#PBS -W group_list=s2516
#PBS -j oe

# Send e-mail when job ends and begins:
#PBS -m eb

cd $PBS_O_WORKDIR

# load the right module files.  These should match the
# modules files in your cshrc or bashrc file:
module load comp-intel/2016.2.181 mpi-hpe/mpt

# choose the right UAM.in file:
#rm -f UAM.in ; ln -s UAM.in.Start UAM.in
rm -f UAM.in ; ln -s UAM.in.Restart UAM.in

# run the code with the right number of processors
mpiexec -np 800 GITM.exe > log.txt

