import os
from pydub import AudioSegment
import librosa
from tempfile import mktemp
import matplotlib.pyplot as plot
import librosa.display
import numpy as np
import os
from PIL import Image
import imagehash
import pandas as pd
paths=[]
directory='E:/desktop/songs'
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
         paths.append(filename)
for i in paths:
    plot.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
    fn_mp3 = os.path.join(directory +"/", i)
    mp3_audio = AudioSegment.from_file(fn_mp3, format="mp3")[:60000]
    sound = AudioSegment.from_mp3(f"{fn_mp3}")
    wname = mktemp('.wav')  # use temporary file
    sound.export(wname, format="wav")  # convert to wav
    wavsong, samplingFrequency = librosa.load(wname, duration=60)
    spect = plot.specgram(wavsong, Fs=samplingFrequency)
    plot.savefig('spectro/' + os.path.basename(i)+'.png', bbox_inches=None, pad_inches=0)
    featured = librosa.feature.spectral_centroid(y=wavsong, sr=samplingFrequency)
    librosa.display.specshow(featured.T, sr=samplingFrequency)
    plot.savefig('centroid/' + os.path.basename(i) + '.png', bbox_inches=None, pad_inches=0)
    featured = librosa.feature.spectral_rolloff(y=wavsong, sr=samplingFrequency)
    librosa.display.specshow(featured.T, sr=samplingFrequency)
    plot.savefig('rolloff/' + os.path.basename(i) + '.png', bbox_inches=None, pad_inches=0)

df = pd.read_excel(r'Data.csv')








# for filename in os.listdir('spectro'):
#     if filename.endswith(".png"):
#         hash_code = imagehash.phash(Image.open('spectro'+'/'+filename))
#         f = open('phash/'+os.path.splitext(os.path.basename(filename))[0]+'.txt','w')
#         f.write(str(hash_code))
