#!/bin/sh
#SBATCH --job-name=gemap_day
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

module load python-anaconda3

python3 get_opensmile_features.py \
--level='day' \
--job_num=$SLURM_ARRAY_TASK_ID  \
--call_type='personal' \
--segments_dir='/nfs/turbo/McInnisLab/PRIORI_v1_Microsoft_Azure/PRIORI-v1-Microsoft-segments/wav/' \
--output_dir='/scratch/emilykmp_root/emilykmp/hnorthru/priori_v1/microsoft_gemaps/' \
--metadata_path='/nfs/turbo/McInnisLab/PRIORI_v1_Microsoft_Azure/PRIORI-v1-Microsoft-segments/priori_v1_ma_segments.csv' \
--config_path='/nfs/turbo/McInnisLab/Libraries/opensmile-2.3.0/config/gemaps/eGeMAPSv01a.conf' \

wait 

python3 agg_opensmile_features.py \
--level='day' \
--call_type='personal' \
--input_dir='/scratch/emilykmp_root/emilykmp/hnorthru/priori_v1/microsoft_gemaps/day/personal/' \
--output_dir='.' \
--tag='gemaps' \
