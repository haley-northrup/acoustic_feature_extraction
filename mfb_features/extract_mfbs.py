''' extract_mfbs 

Extract Mel-filterbanks (MFBs) 


'''


import numpy as np
import librosa
import os 
import pandas as pd
from scipy.io import wavfile

_SAMPLE_RATE = 16000
_N_FFT = 2048
_WIN_LENGTH = 200
_HOP_LENGTH = 80
_FMIN = 0
_FMAX = None
_N_MELS = 40


def extract_mfb(y, output_file):


        #y, sample_rate = librosa.load(input_wav, sr=_SAMPLE_RATE)
        y = librosa.effects.preemphasis(np.array(y))

        #print('preemph')

        spec = librosa.core.stft(y=y,
                                 n_fft=_N_FFT,
                                 hop_length=_HOP_LENGTH,
                                 win_length=_WIN_LENGTH,
                                 window='hann',
                                 center=True,
                                 pad_mode='reflect')
        spec = librosa.magphase(spec)[0]
        mel_spectrogram = librosa.feature.melspectrogram(S=spec,
                                                         sr=_SAMPLE_RATE,
                                                         n_mels=_N_MELS,
                                                         power=1.0,  # actually not used given "S=spec"
                                                         fmin=_FMIN,
                                                         fmax=_FMAX,
                                                         htk=False,
                                                         norm=1)
        log_mel_spectrogram = np.log(mel_spectrogram + 1e-6).astype(np.float32)
        

        #z-normalize utterance 
        stdVal = np.std(log_mel_spectrogram) 
        if stdVal == 0: 
            stdVal = 1 
        log_mel_spectrogram = (log_mel_spectrogram - np.mean(log_mel_spectrogram)) / stdVal 

        # clamp to 3 std
        clampVal = 3.0 
        log_mel_spectrogram[log_mel_spectrogram > clampVal] = clampVal 
        log_mel_spectrogram[log_mel_spectrogram < -clampVal] = -clampVal 

        #print('mfbs')
        np.save(output_file, arr=np.transpose(log_mel_spectrogram))

        #return True

    	#except Exception:
        #return False

if __name__ == '__main__': 
    
    # get timings of all vowels 
    phones_df = pd.read_csv('/data/aromana/TIMIT/Phone_timings.csv')
    vowels_df = pd.read_csv('/data/aromana/TIMIT/Vowels.csv')
    vowels_df = vowels_df.loc[vowels_df['vowel'] == 1] 
    phones_df = phones_df.loc[phones_df['phone'].isin(vowels_df['phone'].tolist())]

    audio_dir = '/data/aromana/TIMIT/Audio'
    output_dir = '/data/aromana/TIMIT/Vowel_MFBs'

    for idx, row in phones_df.iterrows(): 
        data, rate = librosa.core.load(os.path.join(audio_dir, row['audio_fname']), sr=_SAMPLE_RATE)
        output_file = os.path.join(output_dir, row['audio_fname'].strip('.WAV') + '_' + str(row['Unnamed: 0']) + '.npy')
        extract_mfb(data, output_file)
        print(row['audio_fname'])


