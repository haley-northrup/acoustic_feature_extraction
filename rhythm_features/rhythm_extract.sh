#!/bin/sh
#SBATCH --job-name=rhythm_extract
#SBATCH --mail-user=hnorthru@umich.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10000
#SBATCH --time=06:00:00
#SBATCH --array=1-100
#SBATCH --output=logs/%x-%j.log
#SBATCH --account=emilykmp1
#SBATCH --partition=standard
#SBATCH --export=NONE 

python3 rhythm_extract.py \
--segments_dir='/nfs/turbo/McInnisLab/hnorthru/code/acoustic_feature_extraction/rhythm_features/temp/wavs/' \
--output_dir='/nfs/turbo/McInnisLab/hnorthru/code/acoustic_feature_extraction/rhythm_features/temp/feats/' \