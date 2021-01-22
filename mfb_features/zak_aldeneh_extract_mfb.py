import librosa
import numpy as np
import soundfile as sf
import scipy.io.wavfile as wav
from python_speech_features import logfbank


wav_file = 'some_file.wav'
sampling_rate = 16000
n_fft = 2048
win_length = n_fft
hop_length = n_fft // 4
n_mels = 40
fmin = 0
fmax = None


def main_librosa():

    # read source wav
    y, sr = librosa.load(wav_file, sr=sampling_rate)

    # extract spectrogram and Mel spectrogram
    spec = librosa.core.stft(y=y,
                             n_fft=n_fft,
                             hop_length=hop_length,
                             win_length=win_length,
                             window='hann',
                             center=True,
                             pad_mode='reflect')
    spec = librosa.magphase(spec)[0]
    mel_spec = librosa.feature.melspectrogram(S=spec,
                                              sr=sr,
                                              n_mels=n_mels,
                                              power=1.0,  # actually not used given "S=spec"
                                              fmin=fmin,
                                              fmax=fmax,
                                              htk=False,
                                              norm=1)

    return np.log(mel_spec)


def main_speech_features():

    rate, sig = wav.read("file.wav")

    # read source wav
    y, sr = librosa.load(wav_file, sr=sampling_rate)

    feats = logfbank(y, samplerate=sr, winlen=0.025, winstep=0.01,
                     nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97,
                     winfunc=lambda x: np.ones((x,)))
    return feats


if __name__ == '__main__':

    # extract using librosa
    main_librosa()

    # extract using python_speech_features
    main_speech_features()
