#!/bin/sh
#SBATCH --job-name=priori_emotion_call
#SBATCH --mail-user=hnorthru@umich.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10000
#SBATCH --time=06:00:00
#SBATCH --array 1
#SBATCH --output=logs/%x-%j.log
#SBATCH --account=emilykmp1
#SBATCH --partition=standard
#SBATCH --export=NONE

module load python-anaconda3

python3 get_emotion_stats_new.py \
--level='day' \
--call_type='assessment' \
--output_dir='.' \
--emo_pred_file='/nfs/turbo/McInnisLab/priori_v1_data/collections/emotion_preds.csv' \
