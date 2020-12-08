import os 
import pandas as pd 
import argparse

from IPython import embed 

''' Combine OpenSmile segment-level features into single csv file ''' 



#Parse Arguments 
#**********************
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, help="Path to directory with individual output files")
parser.add_argument('--output_dir', type=str, help="Path to directory to output feature files to.")
parser.add_argument('--level', type=str, default='call')
parser.add_argument('--call_type', type=str, default='all')
args = parser.parse_args()

#Aggregate individual files in input_dir 
#***********************************
files = os.listdir(args.input_dir) 

feats_df = pd.DataFrame() 
for f in files: #iterate over segments
    seg_id = f.strip('.csv')
    seg_path = os.path.join(args.input_dir, f)
    #add segment features to feature dataframe 
    seg_feats_df = pd.read_csv(seg_path, sep=';') 
    seg_feats_df['segment_id'] = seg_id
    seg_feats_df['name'] = seg_id  
    feats_df = feats_df.append(seg_feats_df) 

cols = list(feats_df.columns.values) 
cols.pop(cols.index('segment_id'))
feats_df = feats_df[['segment_id'] + cols]
feats_df = feats_df.drop(['name'], axis=1) 

#Save aggregate segments file 
feats_df.to_csv(os.path.join(args.output_dir, args.level + '_' + args.call_type + '_gemaps.csv'), index=False) 
