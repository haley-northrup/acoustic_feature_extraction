""" get_opensmile_features

Get OpenSmile features for segments, statistics (mean, std) over segments for day or call level 

"""

import os 
import sys
import argparse
import pandas as pd 
from IPython import embed
from get_chunks import chunks 

#TODO (2020-12-02) new version of OpenSmile with a python API 


opensmile_path = '/nfs/turbo/McInnisLab/Libraries/opensmile-2.3.0/bin/linux_x64_standalone_static/SMILExtract'

def extract_open_smile_features(args):
    """
    Extract OpenSmile features for segments and statistics over segments in (day or call) 

    :param args: input arguments from argparse 
    :return: none
    """

    #set up 
    level = args.level  
    temp_dir = os.path.join(args.output_dir, 'segments')
    output_dir = os.path.join(args.output_dir, level+'s', args.call_type)   
 
    #get segment metadata 
    metadata_df = pd.read_csv(args.metadata_path)
    metadata_df['datetime'] = pd.to_datetime(metadata_df['datetime'])
    metadata_df['date'] = metadata_df['datetime'].dt.date
    metadata_df['day_id'] = metadata_df['subject_id'].apply(str) + '_' + metadata_df['date'].apply(str)   

    #filter call type (personal, assessment, all) 
    if args.call_type == 'personal':
        metadata_df = metadata_df.loc[metadata_df['is_assessment'] == 'f', :]
    elif args.call_type == 'assessment':
        metadata_df = metadata_df.loc[metadata_df['is_assessment'] == 't', :]
    elif args.call_type != 'all':
        print('Invalid call_type: ' + str(args.call_type))
        return 

    #get call_ids in chunk
    chunk = int(args.job_num)
    call_ids = sorted(metadata_df['call_id'].unique()) 
    call_ids = list(chunks(call_ids,100))[chunk-1]  

    #aggregation level 
    if level == 'call': 
        idx_vals = metadata_df['call_id'].sort_values().unique().tolist()
        idx_col = 'call_id'
    elif level == 'day': 
        idx_vals = metadata_df['day_id'].drop_duplicates().values.tolist() 
        idx_col = 'day_id' 
    idx_vals = list(chunks(idx_vals,100))[chunk-1] 

    #make output directories 
    if not os.path.exists(temp_dir): 
        os.makedirs(temp_dir) 
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir) 

    #COMPUTE OPENSMILE FEATURES 
    #***********************************************************
    #***********************************************************
    for idx in idx_vals[0:5]: #iterate over calls or days
        seg_ids = metadata_df.loc[metadata_df[idx_col] == idx, 'segment_id'].unique()  

        #Compute features for all segment in idx 
        feats_df = pd.DataFrame() 
        for seg_id in seg_ids: #iterate over segments
            seg_input_path = os.path.join(args.segments_dir, str(seg_id) + '.wav')
            seg_output_path = os.path.join(temp_dir, str(seg_id) + '.csv')
            
            #compute OpenSmile features for segment 
            if not os.path.exists(seg_output_path): 
                # if we use the option -D instead of -csvoutput 
                # we can get frame-level outputs
                runprocess = opensmile_path + ' -C ' + args.config_path + ' -I ' + seg_input_path + ' -csvoutput ' + seg_output_path 
                os.system(runprocess) 

            #add segment features to feature dataframe 
            seg_feats_df = pd.read_csv(seg_output_path, sep=';') 
            seg_feats_df['segment_id'] = seg_id 
            feats_df = feats_df.append(seg_feats_df) 
        
        #compute mean and std over segment OpenSmile features 
        s = pd.Series()
        for col in feats_df.columns: 
            if col in ['name', 'frameTime', 'segment_id']:
                continue   
            s[col+'_mean'] = feats_df[col].mean() 
            s[col+'_std'] = feats_df[col].std() 
        
        #save feature stats for index to file 
        output_path = os.path.join(output_dir, str(idx) + '.csv')
        s.to_csv(output_path) 


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=str, default='call')
    parser.add_argument('--job_num', type=int, default=1) 
    parser.add_argument('--call_type', type=str, default='all', help='specifies type of call (assessment, personal, or all)')
    parser.add_argument('--segments_dir', type=str, help='Path to directory with segment wave files')
    parser.add_argument('--output_dir', type=str, help="Path to directory to output feature files to.")
    parser.add_argument('--metadata_path', type=str, help="Path to segment metadata file (subject, call, etc.).")
    parser.add_argument('--config_path', type=str, help="Path to OpenSmile config file") 
    return parser.parse_args()
    
def main():
    args = _parse_args() 
    extract_open_smile_features(args) 


if __name__ == '__main__': 
    main() 

