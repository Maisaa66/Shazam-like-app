from typing import final
from pydub import AudioSegment
from tempfile import mktemp
import librosa
import librosa.display
import time
import imagehash
from PIL import Image
import pylab
import numpy as np
from scipy.fftpack.pseudo_diffs import diff


class SongModel(object):
    def __init__(self, song_paths, ratio):
        self.song_paths = song_paths  # list of selected songs
        self.ratio = ratio  # slider ratio, default = 0.5
        self.wavsong, self.wavsongs_list, self.features_list, self.hashes_list = [], [], [], []
        self.features_methods = ['spectral_centroid', 'spectral_rolloff']
        self.samplingfreq = 0
        self.hashcode = ""
        self.avg_all_features = 0
        self.convert_to_wav()

    def update_mixer(self, ratio):

        self.ratio = ratio
        self.wavsong = np.add(
            self.ratio * self.wavsongs_list[1], self.wavsongs_list[0] * (1-self.ratio))
        return self.wavsong

    def convert_to_wav(self):
        if len(self.song_paths) == 2:
            for i in range(2):
                cutted_mp3 = AudioSegment.from_file(
                    self.song_paths[i], format="mp3")[:60000]
                tmp_wav_file = mktemp('.wav')  # use temporary file
                # convert mp3 to wav
                cutted_mp3.export(tmp_wav_file, format="wav")
                # load wav-file into array using librosa
                temp_wav_array, self.samplingfreq = librosa.load(tmp_wav_file)
                # store wav array of both songs
                self.wavsongs_list.append(temp_wav_array)
            self.wavsong = np.add(
                self.ratio * self.wavsongs_list[0], self.wavsongs_list[1] * (1-self.ratio))

            return self.wavsong
        else:
            cutted_mp3 = AudioSegment.from_file(
                self.song_paths[0], format="mp3")[:60000]
            tmp_wav_file = mktemp('.wav')  # use temporary file
            cutted_mp3.export(tmp_wav_file, format="wav")  # convert mp3 to wav
            self.wavsong, self.samplingfreq = librosa.load(tmp_wav_file)
            return self.wavsong

    def extract_features(self):
        self.features_list.clear()

        self.features_list.append(librosa.feature.chroma_stft(
            y=self.wavsong, sr=self.samplingfreq))
        self.features_list.append(librosa.feature.mfcc(
            y=self.wavsong, sr=self.samplingfreq))
        self.features_list.append(librosa.feature.melspectrogram(
            y=self.wavsong, sr=self.samplingfreq))

        return self.features_list

    def hashing(self):
        self.hashes_list.clear()
        # We will use Perceptual hashing
        for i in range(len(self.features_list)):
            # convert the array of the feature to a PIL image
            newhash = Image.fromarray(self.features_list[i], mode='RGB')
            finalhash = imagehash.phash(newhash, hash_size=16).__str__()
            print("hashcode: ", finalhash)
            # hashcode = imagehash.phash(Image.fromarray(self.features_list[i]))
            self.hashes_list.append(finalhash)

    def hashing_script(self):
        self.extract_features()
        self.hashing()
        return self.hashes_list

        # song_hashes = {}
        # song_hashes['chroma_stft'] = str(self.hashes_list[0])
        # song_hashes['mfcc'] = str(self.hashes_list[1])

    # ht7sb el difference between mel_song_hash w ben mel_allsongsinDB_hash

    def hamming_distance(self, first_hash, second_hash):
        # Calculate difference between selected-song-hash and another hash in db
        ''' calculates the hamming distance between two strings which represents the differences between them '''
        difference = imagehash.hex_to_hash(
            first_hash)-imagehash.hex_to_hash(second_hash)
        return difference

    def saveImage(self, path, y):
        # start_savingImg = time.time()
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[],
                   yticks=[])  # Remove the white edge
        librosa.display.specshow(
            self.spectrogram_data, y_axis=y, sr=self.samplingfreq)
        pylab.savefig(path, bbox_inches=None, pad_inches=0)
        pylab.close()
