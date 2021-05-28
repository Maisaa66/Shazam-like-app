from pydub import AudioSegment
from tempfile import mktemp
import matplotlib.pyplot as plot
import librosa.display
import os
from PIL import Image
import imagehash
import xlwt
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("hashes")
n=0
m=0
l=1
v=0
paths=[]
songs_name=[]
feature=['Mfcc','Chroma']
directory=r'Songs'
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
         paths.append(filename)
         songs_name.append(os.path.splitext(filename)[0])
for t in feature:
    m+=1
    sheet.write(0,m,t)
for o in songs_name:
       v+=1
       sheet.write(v,0,o)
for i in paths:
    # plot.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
    fn_mp3 = os.path.join(directory +"/", i)
    mp3_audio = AudioSegment.from_file(fn_mp3, format="mp3")[:60000]
    sound = AudioSegment.from_mp3(f"{fn_mp3}")
    wname = mktemp('.wav')  # use temporary file
    sound.export(wname, format="wav")  # convert to wav
    wavsong, samplingFrequency = librosa.load(wname, duration=60)
    mfcc = librosa.feature.mfcc(wavsong, samplingFrequency) #Mel-Frequency Cepstral Coefficients(MFCCs)
    hash_mfcc=str((imagehash.phash(Image.fromarray(mfcc))))
    chroma_stft = librosa.feature.chroma_stft(wavsong, samplingFrequency) #Chroma feature
    hash_chroma_stft=str((imagehash.phash(Image.fromarray(chroma_stft))))
    hashes=[hash_mfcc,hash_chroma_stft]
    for k in hashes:
       n+=1
       sheet.write(l,n,k)
    n=0
    l+=1
    hashes.clear()
workbook.save("featuresHashes.xls")



