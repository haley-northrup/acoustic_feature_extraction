#!/bin/sh
#SBATCH --job-name=priori_os_agg_segs 
#SBATCH --mail-user=hnorthru@umich.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10000
#SBATCH --time=10:00:00
#SBATCH --array 1
#SBATCH --output=logs/%x-%j.log
#SBATCH --account=emilykmp1
#SBATCH --partition=standard
#SBATCH --export=NONE

python3 combine_opensmile_seg_feats.py \
--level='segment' \
--call_type='all' \
--input_dir='/scratch/emilykmp_root/emilykmp/aromana/gemaps_features/segments/' \
--output_dir='.' \
