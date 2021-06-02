import numpy as np
import difflib
from pydub import AudioSegment
import os
import librosa
import librosa.display
import numpy as np
from tempfile import mktemp
import pylab
from PIL import Image
import imagehash
from scipy import spatial
from numpy import dot
from numpy.linalg import norm

# song1 = "Group17_Song1_Full.mp3"
# song2 = "Group17_Song2_Full.mp3"

# cutted_song1 = AudioSegment.from_file(song1, format="mp3")[:60000]
# cutted_song2 = AudioSegment.from_file(song2, format="mp3")[:60000]
{"ID": "171", "mel-spectrogram": {"Full": "a020cd8ebda50e2629b504e43df36dd314ce39666e670f3c295550f879a39bd3",
                                  "Music": "c080ac83fb652f3f48c867e619f07d5f23ce342e3ef506ba6f5443ee1b211834",
                                  "Vocals": "8906c735d0eecd38d3ed81add1d7d60cc4a2c110edaec638dbc9c0bacb2f9515"},
    "mfcc": {"Full": "c1e47bcdcd3eda4a059a82103ae7897f764370a78049cfbc302fdddea26540e6",
             "Music": "c1a0fee7edfcdacacfb6820032ffbff97b46a8e98200cdbf18584734200158a6",
             "Vocals": "8b6de4b3dc20e6b29d00bc79a0df709c809f728e27c29d09c2e7dd69825729af"}}

# waveName1 = mktemp('.wav')  # use temporary file
# waveName2 = mktemp('.wav')  # use temporary file
# cutted_song1.export(waveName1, format="wav")  # convert1 to wav
# cutted_song2.export(waveName2, format="wav")  # convert2 to wav


# wavSong1, freqSong1 = librosa.load(waveName1)
# wavSong2, freqSong2 = librosa.load(waveName2)

# mix = np.add(0.2 * wavSong1, 0.8 * wavSong2)


# chromaSong1 = librosa.feature.chroma_stft(y=wavSong1, sr=freqSong1)
# mfccSong1 = librosa.feature.mfcc(y=wavSong1, sr=freqSong1)

# chromaSong2 = librosa.feature.chroma_stft(y=wavSong2, sr=freqSong2)
# mfccSong2 = librosa.feature.mfcc(y=wavSong2, sr=freqSong2)

# mfccmix = librosa.feature.mfcc(y=mix, sr=freqSong2)

# song1FeaturesList = []
# song1FeaturesList.append(chromaSong1)
# song1FeaturesList.append(mfccSong1)

# song2FeaturesList = []
# song2FeaturesList.append(chromaSong2)
# song2FeaturesList.append(mfccSong2)


# result = 1 - spatial.distance.cosine(chromaSong1, chromaSong2)


# chroma_song1_music: a37e7ca3f85c8181  ##SAMPLE
# mfcc_song1_music: cbc99495959d1d4a    ##SAMPLE

# chroma_SONG1_FULL: a85f57a8f857a8a0
# mfcc_sog1_full: f4f0b4a6848de35c

def mapValue(inputValue: float, inputMin: float, inputMax: float, outputMin: float, outputMax: float):

    slope = (outputMax-outputMin) / (inputMax-inputMin)
    return outputMin + slope*(inputValue-inputMin)


# ==============================================================================================

    # ht7sb el difference between mel_song_hash w ben mel_allsongsinDB_hash
def hamming_distance(first_hash, second_hash):
    ''' calculates the hamming distance between two strings which represents the differences between them ''' 
    difference = imagehash.hex_to_hash(first_hash)-imagehash.hex_to_hash(second_hash)
    return difference

def normalization(n):
    return (n/256)


# # We double all numbers using map()
# numbers = [50, 0.4, -12, 130, -100, 256, -256, 0, -1]
# result = map(normalization, numbers)
# print(list(result))

x1 = hamming_distance("a37e7ca3f85c8181", "a85f57a8f857a8a0")
x2 = hamming_distance("cbc99495959d1d4a", "f4f0b4a6848de35c")
print("x1: ", x1)
print("x2: ", x2)
avg = (x1+x2)/2
mapped_avg = mapValue(avg, 0, 256, 0, 1)

similarityIndex = int((1-mapped_avg)*100)

print("similarityIndex: ", similarityIndex)
# hashes = ["c91ede01ad73c6b3997ec1e0b69d698f21dd48a9076a7e3125c8422660d9d5bd", "a826b0efcf16edfacd108200b2ffbee8324fd8c38248cfbcb8c16bbe304169a6"]

# result1 = imagehash.hex_to_hash(hashes[0])
# result2 = imagehash.hex_to_hash(hashes[1])
# diff = result2 - result1
# print("diff : ", diff)

# import xlrd
# book = xlrd.open_workbook("featuresHashes.xls")
# sheet = book.sheet_by_index(0)
# for i in range(sheet.nrows -1): #print all values in col (1)
#     x = sheet.cell_value(rowx=i+1, colx=1)
#     print(x)
