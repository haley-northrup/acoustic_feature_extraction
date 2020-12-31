import sys, os 
import numpy as np
import pandas as pd 
import argparse 
import scipy.io.wavfile as wav
from mfb_util import new_get_mfbs

''' 
TODO: 
pass in file with paths to segments? 
make a parallel process?? 
multiprocess??
get chunks??  
''' 


def extract_mfb(f, input_dir, output_dir):
    audioPath = os.path.join(input_dir, f)
    featPath = os.path.join(output_dir, f.replace('.wav','.npy'))
    if not os.path.exists(featPath):
        spec, mean, std = new_get_mfbs(audioPath)
        np.save(featPath, spec) 

def _parse_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--job_num', type=int, default=1) 
    parser.add_argument('--segments_dir', type=str, help='Path to directory with segment wave files')
    parser.add_argument('--output_dir', type=str, help="Path to directory to output feature files to.")
    return parser.parse_args()

def main():
    args = _parse_args() 
    files = os.listdir(args.segments_dir)
    files = [f for f in files if f.endswith('.wav')]

    for f in files:
        extract_mfb(f, args.segments_dir, args.output_dir)
    
if __name__ == "__main__":
    main()
