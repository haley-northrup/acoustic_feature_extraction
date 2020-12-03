import os 
import pandas as pd 

#TODO add metadata columns (call_id, subject_id, date) 

input_dir = '/scratch/emilykmp_root/emilykmp/aromana/gemaps_features/days'
output_dir = '/nfs/turbo/chai-health/aromana/gemaps_features/'
files = os.listdir(input_dir) 
df_full = pd.DataFrame()
for f in files: 
    df = pd.read_csv(os.path.join(input_dir, f), index_col=0, header=0, names=[f.strip('.csv')])
    df_full = df_full.append(df.T) 
df_full.to_csv(os.path.join(output_dir, 'day_gemaps.csv')) 


