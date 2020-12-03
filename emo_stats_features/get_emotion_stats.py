""" get_emotion_stats

Get emotion statistics from MADDoG emotion predictions 
Aggregate statistics over the segments in each call or day (specified by user) 

"""

import sys
import os
import math
import numpy as np 
import pandas as pd 
import argparse
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from IPython import embed


def get_emo_stats(args): 
    """
    Compute statistics over emotion predictions by segment based on data level (i.e. call, day) 
    save to csv file (full - all 27 statistics, abv - abreviated set 'min', 'max', 'range', 'mean', 'std' )

    :param args: input arguments from argparse  
    :return: none
    """

    #set up
    level = args.level 
    cols = ['activation_low', 'activation_mid', 'activation_high', 
                'valence_low', 'valence_mid', 'valence_high']

    # final df that will be appended to as we loop over all the calls    
    features_df = pd.DataFrame()

    #get segment-level emotion predictions 
    segment_df = pd.read_csv(args.emo_pred_file)
    segment_df['call_datetime'] = pd.to_datetime(segment_df['call_datetime'])
    segment_df['call_date'] = segment_df['call_datetime'].dt.date
    segment_df['day_id'] = segment_df['subject_id'].apply(str) + '_' + segment_df['call_date'].apply(str)   

    #filter call type (personal, assessment, both) 
    if args.call_type == 'personal':
        segment_df = segment_df.loc[segment_df['is_assessment'] == 'f', :]
    elif args.call_type == 'assessment':
        segment_df = segment_df.loc[segment_df['is_assessment'] == 't', :]
    elif args.call_type != 'all':
        print('Invalid call_type: ' + str(args.call_type))
        return 

    #aggregation level 
    if level == 'call': 
        idx_vals = segment_df['call_id'].sort_values().unique().tolist()
        idx_col = 'call_id'
    elif level == 'day': 
        idx_vals = segment_df['day_id'].drop_duplicates().values.tolist() 
        idx_col = 'day_id' 

    #Generate statistics dataframe 
    #*****************************
    for idx in idx_vals[0:5]: #iterate over calls or days         
        temp_df = segment_df.loc[segment_df[idx_col] == idx]
        
        func_dict = compute_statistics(temp_df, cols)
        # append to the entire dataframe where the index is the call_id or day_id depending on level  
        features_idx = pd.Series(func_dict).rename(idx)
        features_df = features_df.append(features_idx) 
            
    #Add metadata based on level 
    if level == 'day': 
        features_df['day_id'] = features_df.index 
        sub_ids = features_df['day_id'].apply(lambda x: x.split('_')[0]).values 
        dates = features_df['day_id'].apply(lambda x: x.split('_')[1]).values
        features_df.insert(loc=0, column='subject_id', value=sub_ids)
        features_df.insert(loc=1, column='date', value=dates) 
        features_df = features_df.drop(['day_id'], axis=1) 
        meta_cols = ['subject_id', 'date']
    elif level == 'call':
        features_df.insert(loc=0, column='call_id', value=features_df.index.values) 
        meta_cols = ['call_id']
 
    #Save Results
    #****************************
    #"full": full statistics set (27) 
    output_name = level + '_' + args.call_type + '_emotion'
    features_df.to_csv(os.path.join(args.output_dir, output_name + '_full.csv'), index=False)
    
    # "abv": abbreviated version of the dataframe (5) 
    ft_cols = [c for c in features_df.columns if c != 'subject_id' and c!= 'date' and c != 'call_id']
    cols_abv = [c for c in ft_cols if c.split('_')[2] in ['min', 'max', 'range', 'mean', 'std']]
    features_df_abv = features_df[meta_cols + cols_abv]
    features_df_abv.to_csv(os.path.join(args.output_dir, output_name + '_abv.csv'), index=False)


def compute_statistics(df, cols):
    """
    Compute statistics over columns of dataframe 
    all 27 statistics
    # these 27 functionals are from John Gideon's When to Intervene paper 
    # he mentions 31, but only these 27 are specifically listed in the paper
    
    :param args: input arguments from argparse  
    :return: none
    """

    func_dict = {}       
    for col in cols:
        # basic stats
        func_dict[col + '_mean'] = df[col].mean() 
        func_dict[col + '_std'] = df[col].std() 
        func_dict[col + '_skew'] = df[col].skew() 
        func_dict[col + '_kurt'] = df[col].kurt() 
        func_dict[col + '_min'] = df[col].min() 
        func_dict[col + '_max'] = df[col].max() 
        func_dict[col + '_range'] = func_dict[col + '_max'] - func_dict[col + '_min']
    
        # percentiles 
        func_dict[col + '_p01'] = df[col].quantile(0.01) 
        func_dict[col + '_p10'] = df[col].quantile(0.10) 
        func_dict[col + '_p25'] = df[col].quantile(0.25) 
        func_dict[col + '_p50'] = df[col].quantile(0.50) 
        func_dict[col + '_p75'] = df[col].quantile(0.75)
        func_dict[col + '_p90'] = df[col].quantile(0.90)
        func_dict[col + '_p99'] = df[col].quantile(0.99) 
            
        # differences between percentiles
        func_dict[col + '_pdiff_50_25'] = func_dict[col + '_p50'] - func_dict[col + '_p25']
        func_dict[col + '_pdiff_75_50'] = func_dict[col + '_p75'] - func_dict[col + '_p50'] 
        func_dict[col + '_pdiff_75_25'] = func_dict[col + '_p75'] - func_dict[col + '_p25'] 
        func_dict[col + '_pdiff_90_10'] = func_dict[col + '_p90'] - func_dict[col + '_p10']
        func_dict[col + '_pdiff_99_01'] = func_dict[col + '_p99'] - func_dict[col + '_p99']

        # percentages above different thresholds which are all percentages of the range
        func_dict[col + '_pabove_10'] = sum(df[col] > (0.10*func_dict[col + '_range'])) / len(df[col])
        func_dict[col + '_pabove_25'] = sum(df[col] > (0.25*func_dict[col + '_range'])) / len(df[col])
        func_dict[col + '_pabove_50'] = sum(df[col] > (0.50*func_dict[col + '_range'])) / len(df[col])
        func_dict[col + '_pabove_75'] = sum(df[col] > (0.75*func_dict[col + '_range'])) / len(df[col])
        func_dict[col + '_pabove_90'] = sum(df[col] > (0.90*func_dict[col + '_range'])) / len(df[col])

        # goodness of fit info 
        y_true = np.array(df[col]).reshape(-1,1)
        x = np.array(range(len(y_true))).reshape(-1,1)
        reg = LinearRegression().fit(x, y_true)
        y_preds = reg.predict(y_true)
        func_dict[col + '_r2'] = r2_score(y_true, y_preds)
        func_dict[col + '_mae'] = mean_absolute_error(y_true, y_preds) 
        func_dict[col + '_mse'] = mean_squared_error(y_true, y_preds)
    return func_dict 


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=str, default='call')
    parser.add_argument('--call_type', type=str, default='specifies type of call (assessment, personal, or all)')
    parser.add_argument('--emo_pred_file', type=str,
                        help="Path to csv file containing emotion predictions for each segment and segment metadata (call_id, datetime)")
    parser.add_argument('--output_dir', type=str, help="Path to directory to output feature files to.")
    return parser.parse_args()


def main():
    args = _parse_args()    
    get_emo_stats(args)

if __name__== "__main__":
    main() 
        

