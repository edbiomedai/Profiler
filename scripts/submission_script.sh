#!/bin/bash
#$ -N ExtractMorphology
#$ -pe sharedmem 8
#$ -cwd
#$ -l h_vmem=16G
#$ -l h_rt=24:00:00
#$ -o ./sumbmission_logs/
#$ -e ./sumbmission_logs/

. /etc/profile.d/modules.sh

module load anaconda/2024.02
source activate ../../Profiler/env/

export file=$(find . -maxdepth 1 -type f | sed -n ''$SGE_TASK_ID' p')

python -m profiler \
    --image $file