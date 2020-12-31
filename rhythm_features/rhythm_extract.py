'''
Required Library: 
https://pypi.org/project/EMD-signal/

Amrit Updated John's Original Code (2020-12-05) 
Step D: Empirical Mode Decomposition 
eemd vs. emd 
eemd - ensemble empirical mode decomposition (John's version)
emd - empirical mode decomposition (Updated version - matches John's paper description) 


'''

import sys, os 
import numpy as np
import pandas as pd 
import scipy.io.wavfile as wav
from scipy import signal
from PyEMD import EMD 

from multiprocessing import Pool
import argparse

NUM_PROCESSES = 1

def discreteIntegral(y, Fs, fLower, fUpper, weighted):
    f = (Fs/2)*np.linspace(0.0,1.0,len(y))
    w = f[1]
    total = 0.0
    for i in range(len(y)):
        fL = max(fLower, f[i]-(w/2.0))
        fU = min(fUpper, f[i]+(w/2.0))
        totF = fU - fL
        if totF <= 0:
            continue
        if weighted:
            total += (totF/w)*y[i]*(fL+(w/2.0))
        else:
            total += (totF/w)*y[i]
    return total

def smooth(a,WSZ):
    # https://stackoverflow.com/questions/40443020/matlabs-smooth-implementation-n-point-moving-average-in-numpy-python
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ    
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((start , out0, stop))

def extractRhythmFeatures(audio, Fs, windowSize, stepSize):
    Fn = Fs / 2
    srcRate = 48000.0
    ds = int(np.floor(100*(float(Fs)/srcRate)))
    if ds == 16:
        allDs = [4, 4]
    else:
        allDs = [ds,]
    dsLen = int(np.floor(windowSize/ds))

    # Calculate number of frames needed
    nli=len(audio)-windowSize+stepSize
    nf = max(nli/stepSize,0)   # number of full frames

    # Extend end of array
    if nf == 0:
        audio = np.append(audio, np.full((windowSize-len(audio),1), audio[-1], audio.dtype))    
        nf = 1
    else:
        na=nli-stepSize*nf # number of samples left over
        if na > 0:
            audio = np.append(audio, np.full((stepSize-int(na),1), audio[-1], audio.dtype))    
            nf += 1

    # Create the filters and windows
    z,p,k = signal.butter(2, [400.0/Fn, 3999.0/Fn], 'bandpass', output='zpk')
    BP = signal.zpk2sos(z, p, k)
    z,p,k = signal.butter(4, [10.0/Fn,], 'lowpass', output='zpk')
    LP = signal.zpk2sos(z, p, k)
    tWin = signal.tukey(dsLen, 0.2)

    # Loop through segments
    feats = np.empty((int(nf), 7))
    feats[:] = np.nan
    frameStart = 0
    for fOn in range(int(nf)):
        # Step A - Get the frame and advance the counter
        segment = audio[frameStart:frameStart+windowSize]
        frameStart = frameStart + stepSize  

        # Step B - Extract the envelope      
        segment = signal.sosfilt(BP,segment)
        segment = signal.sosfilt(LP,np.abs(segment))
        segment = segment - np.mean(segment)
        segment = segment/np.max(np.abs(segment))

        # Skip if NaNs        
        if np.any(np.isnan(segment)):
            continue

        # Downsample
        for dsOn in allDs:
            segment = signal.decimate(segment, dsOn, zero_phase=True)
        fss = Fs/ds
        windowedSegment = segment * tWin

        # Step C - Spectral analysis
        NFFT = len(windowedSegment)
        spectrum = np.square(np.abs(np.fft.fft(windowedSegment,NFFT)))
        spectrum = (spectrum*2)/NFFT;
        spectrum = spectrum[:int(np.floor(NFFT/2))]
        SPBr3_5 = discreteIntegral(spectrum, fss, 1.0, 3.5, False) / discreteIntegral(spectrum, fss, 3.5, 10.0, False)
        CNTR1_10 = discreteIntegral(spectrum, fss, 1.0, 10.0, True) / discreteIntegral(spectrum, fss, 1.0, 10.0, False)
        feats[fOn,:2] = [SPBr3_5, CNTR1_10]

        # Step D - Empirical mode decomposition
        #imfs = eemd(segment, num_imfs=2)
        emd = EMD() 
        imfs = emd(segment)[:2,:]
        IMF12 = np.sum(np.square(imfs[1])) / np.sum(np.square(imfs[0]))

        # Step E - Get instantaneous frequencies
        rem = int(np.ceil(fss/10));
        phase = signal.hilbert(imfs, axis=1)
        phase = np.angle(phase)
        phase = np.unwrap(phase) 
        for i in range(2):
            phase[i] = smooth(phase[i],5)
        phase = np.diff(phase, axis=1)
        phase = phase[:,rem:-rem]
        Fi = []
        for i in range(2):
            filter = np.abs(phase[i]-np.mean(phase[i])) < (3.0*np.std(phase[i]))
            Fi.append(phase[i][filter])
        IMF1_M = np.mean(Fi[0])
        IMF1_S = np.std(Fi[0])
        IMF2_M = np.mean(Fi[1])
        IMF2_S = np.std(Fi[1])                
        feats[fOn,2:] = [IMF12, IMF1_M, IMF1_S, IMF2_M, IMF2_S] 
    feat_names = ['SPBr3_5', 'CNTR1_10', 'IMF12', 'IMF1_M', 'IMF1_S', 'IMF2_M', 'IMF2_S']      

    return feats, feat_names 

def extractRhythmMap(f, input_dir, output_dir):
    audioPath = os.path.join(input_dir, f)
    #featPath = os.path.join(output_dir, f.replace('.wav','.npy'))
    featPath = os.path.join(output_dir, f.replace('.wav','.csv'))
    if not os.path.exists(featPath):
        (Fs, x) = wav.read(audioPath)
        x = x.astype(np.float) / 32768.0
        #feats = extractRhythmFeatures(x, Fs, 2*Fs, Fs)
        #np.save(featPath, feats) 
        feats, feat_names = extractRhythmFeatures(x, Fs, 2*Fs, Fs)
        df = pd.DataFrame(feats, columns = feat_names) 
        df.to_csv(featPath, index=False) 

def _parse_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--level', type=str, default='call')
    #parser.add_argument('--job_num', type=int, default=1) 
    #parser.add_argument('--call_type', type=str, default='all', help='specifies type of call (assessment, personal, or all)')
    parser.add_argument('--segments_dir', type=str, help='Path to directory with segment wave files')
    parser.add_argument('--output_dir', type=str, help="Path to directory to output feature files to.")
    #parser.add_argument('--metadata_path', type=str, help="Path to segment metadata file (subject, call, etc.).")
    return parser.parse_args()

def main():
    args = _parse_args() 
    files = os.listdir(args.segments_dir)
    files = [f for f in files if f.endswith('.wav')]

    if NUM_PROCESSES==1:
        for f in files:
            extractRhythmMap(f, args.segments_dir, args.output_dir)
    else:
        pool = Pool(processes=NUM_PROCESSES)
        pool.map(extractRhythmMap, files)
    
if __name__ == "__main__":
    main()
