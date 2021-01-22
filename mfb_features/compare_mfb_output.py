''' 
Compare MFB output 

normalized and un-normalized 

2021-01-05
mfb_util.get_mfbs - produces different output when applying normalization and not applying normalization 
** need to talk to Amrit about this... 

''' 

import os 
import numpy as np 
from IPython import embed 


#SET UP 
#************************

raw_path = './temp/raw/'
norm_path = './temp/norm/'

raw_files = os.listdir(raw_path) 
norm_files = os.listdir(norm_path) 

#compare files 
for f in raw_files:
    fn_raw = os.path.join(raw_path, f) 
    fn_norm = os.path.join(norm_path, f) 

    raw_data = np.load(fn_raw) 
    norm_data = np.load(fn_norm)

    print(f)
    print(np.sum(np.abs(norm_data - raw_data)))

