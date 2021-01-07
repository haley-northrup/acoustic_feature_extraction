#!/bin/sh
#SBATCH --job-name=rhythm_feats 
#SBATCH --mail-user=hnorthru@umich.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10000
#SBATCH --time=12:00:00
#SBATCH --array=1-100
#SBATCH --output=logs/%x-%j.log
#SBATCH --account=emilykmp1
#SBATCH --partition=standard
#SBATCH --export=NONE 

source /nfs/turbo/McInnisLab/hnorthru/anaconda3/etc/profile.d/conda.sh 
conda activate gid_8_tn_20200220

python3 get_rhythm_features.py \
--job_num=$SLURM_ARRAY_TASK_ID   \
--level='day' \
--call_type='personal' \
--segments_dir='/nfs/turbo/McInnisLab/PRIORI_v1_Microsoft_Azure/PRIORI-v1-Microsoft-segments/wav/' \
--output_dir='/scratch/emilykmp_root/emilykmp/hnorthru/priori_v1/microsoft_rhythm/' \
--metadata_path='/nfs/turbo/McInnisLab/PRIORI_v1_Microsoft_Azure/PRIORI-v1-Microsoft-segments/priori_v1_ma_segments.csv' \
