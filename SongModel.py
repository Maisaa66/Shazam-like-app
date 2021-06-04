from pydub import AudioSegment
from tempfile import mktemp
import librosa
import librosa.display
import imagehash
from PIL import Image
import pylab
import numpy as np


class SongModel:
    def __init__(self, song_paths, ratio):
        self.song_paths = song_paths  # list of selected songs
        self.ratio = ratio  # slider ratio, default = 0.5
        self.wavsong, self.wavsongs_list, self.features_list, self.all_hashes, self.samp_rates = [], [], [], [], []
        self.features_methods = ['spectral_centroid',
                                 'spectral_rolloff']  # for saving img
        self.convert_to_wav()
        if len(self.wavsongs_list) == 1:
            self.wavsong = self.wavsongs_list[0]
        else:
            self.mix_songs(self.ratio)  # mix 2 converted songs.

    def convert_to_wav(self):
        for path in self.song_paths:
            cutted_mp3 = AudioSegment.from_file(path, format="mp3")[:60000]
            tmp_wav_file = mktemp('.wav')  # use temporary file
            # convert mp3 to wav
            cutted_mp3.export(tmp_wav_file, format="wav")
            # load wav-file into array using librosa
            temp_wav_array, _ = librosa.load(tmp_wav_file)
            # store wav array of both songs
            self.wavsongs_list.append(temp_wav_array)

    def mix_songs(self, ratio):
        self.ratio = ratio
        self.wavsong = np.add(
            self.ratio * self.wavsongs_list[1], self.wavsongs_list[0] * (1-self.ratio))
        return self.wavsong

    def extract_features(self):
        self.features_list.clear()
        # Sampling rate = 22050, default value
        self.features_list.append(librosa.feature.chroma_stft(self.wavsong))
        self.features_list.append(librosa.feature.mfcc(self.wavsong))
        self.features_list.append(librosa.feature.melspectrogram(self.wavsong))
        return self.features_list

    def generate_hash(self):
        self.all_hashes.clear()
        # We will use Perceptual hashing
        for i in range(len(self.features_list)):
            # convert the array of the feature to a PIL image
            array = Image.fromarray(self.features_list[i], mode='RGB')
            hash = imagehash.phash(array, hash_size=16).__str__()
            self.all_hashes.append(hash)

    def hashing_script(self):
        self.extract_features()
        self.generate_hash()
        return self.all_hashes

    def hamming_distance(self, first_hash, second_hash):
        # Calculate difference between selected-song-hash and another hash in db
        ''' calculates the hamming distance between two strings which represents the differences between them '''
        difference = imagehash.hex_to_hash(
            first_hash)-imagehash.hex_to_hash(second_hash)
        return difference

    # def saveImage(self, path, y):
    #     pylab.axis('off')  # no axis
    #     pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[],
    #                yticks=[])  # Remove the white edge
    #     librosa.display.specshow(
    #         self.spectrogram_data, y_axis=y, sr=self.samplingfreq)
    #     pylab.savefig(path, bbox_inches=None, pad_inches=0)
    #     pylab.close()
