from pydub import AudioSegment
from tempfile import mktemp
import matplotlib.pyplot as plot
import librosa.display
import os
from PIL import Image
import imagehash
import xlwt

# Here we create xls sheet of database (songs) and its features hashing values
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("hashes")
row = 0
column = 0
hashRow = 1
hashColumn = 0
paths = []
songs_name = []
features = ['Chroma', 'Mfcc']
# read the file that containes the songs and if its ending with mp3 get its name so we can use it in the xls sheet
directory = r'Songs'
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        paths.append(filename)
        songs_name.append(os.path.splitext(filename)[0])

# writing features name in rows of xls
for feature in features:
    row += 1
    sheet.write(0, row, feature)

# writing songs name in columns of xls
for song in songs_name:
    column += 1
    sheet.write(column, 0, song)

for i in paths:
    # getting the path of each song in the file and convert it into wave
    fn_mp3 = os.path.join(directory + "/", i)
    mp3_audio = AudioSegment.from_file(fn_mp3, format="mp3")[:60000]
    sound = AudioSegment.from_mp3(f"{fn_mp3}")
    wname = mktemp('.wav')  # use temporary file
    sound.export(wname, format="wav")  # convert to wav
    wavsong, samplingFrequency = librosa.load(wname, duration=60)
    # getting the features (chroma, mfcc) of each song in the file
    # Mel-Frequency Cepstral Coefficients(MFCCs)
    mfcc = librosa.feature.mfcc(wavsong, samplingFrequency)
    hash_mfcc = str((imagehash.phash(Image.fromarray(mfcc))))
    chroma_stft = librosa.feature.chroma_stft(
        wavsong, samplingFrequency)  # Chroma feature
    hash_chroma_stft = str((imagehash.phash(Image.fromarray(chroma_stft))))
    hashes = [hash_chroma_stft, hash_mfcc]
    # Write each hashing value in the xls sheet to its crossponding feature and song name and save file
    for Hash in hashes:
        hashColumn += 1
        sheet.write(hashRow, hashColumn, Hash)
    hashColumn = 0
    hashRow += 1
    hashes.clear()
workbook.save("featuresHashes.xls")
