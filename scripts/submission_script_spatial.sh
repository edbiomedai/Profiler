#!/bin/bash
#$ -N Spatial
#$ -cwd
#$ -l h_vmem=32G
#$ -l h_rt=24:00:00
#$ -o ../sumbmission_logs/
#$ -e ../sumbmission_logs/

. /etc/profile.d/modules.sh

module load anaconda/2024.02
source activate ../../../Profiler/env/

export folder=$(find . -mindepth 1 -maxdepth 1 -type d | sed -n ''$SGE_TASK_ID' p')

python -m profiler.spatial \
    --input-folder $folder
