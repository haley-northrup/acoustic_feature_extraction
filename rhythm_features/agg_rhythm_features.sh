#!/bin/sh
#SBATCH --job-name=agg_rhythm
#SBATCH --mail-user=hnorthru@umich.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10000
#SBATCH --time=2:00:00
#SBATCH --array=1
#SBATCH --output=logs/%x-%j.log
#SBATCH --account=emilykmp1
#SBATCH --partition=standard
#SBATCH --export=NONE 

source /nfs/turbo/McInnisLab/hnorthru/anaconda3/etc/profile.d/conda.sh 
conda activate gid_8_tn_20200220

python3 agg_rhythm_features.py \
--level='day' \
--call_type='personal' \
--input_dir='/scratch/emilykmp_root/emilykmp/hnorthru/priori_v1/microsoft_rhythm/day/personal/' \
--output_dir='.' \