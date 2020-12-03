#!/bin/sh
####SBATCH --job-name=priori_day
####SBATCH --mail-user=hnorthru@umich.edu
####SBATCH --mail-type=FAIL
####SBATCH --nodes=1
####SBATCH --ntasks-per-node=1
####SBATCH --mem=10000
####SBATCH --time=06:00:00
####SBATCH --array 1-100
####SBATCH --output=logs/%x-%j.log
####SBATCH --account=emilykmp1
####SBATCH --partition=standard
####SBATCH --export=NONE

module load python-anaconda3

python3 get_opensmile_features.py \
--job_num=0  \
--level='day' \
--call_type='all' \
--segments_dir='/nfs/turbo/McInnisLab/priori_v1_data/segments_all/wav/' \
--output_dir='/scratch/emilykmp_root/emilykmp/hnorthru/gemaps_features/' \
--metadata_path='/nfs/turbo/McInnisLab/priori_v1_data/segments_all/data.csv' \
--config_path='/nfs/turbo/McInnisLab/Libraries/opensmile-2.3.0/config/gemaps/eGeMAPSv01a.conf' \

#wait 
#python3 aggregate_gemaps_features.py

#--job_num=$SLURM_ARRAY_TASK_ID#
 