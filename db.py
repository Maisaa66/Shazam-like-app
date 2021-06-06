from pydub import AudioSegment
from tempfile import mktemp
import matplotlib.pyplot as plot
import librosa.display
import os
from PIL import Image
import imagehash
import xlwt


class Database(object):
    def __init__(self, *args):
        super(Database, self).__init__(*args)

        self.column_hash = 0
        self.column_counter = 0
        self.row_hash = 1
        self.row_counter = 0
        self.paths = []
        self.songs_name = []
        self.features = ['Chroma', 'Mfcc', 'Mel']
        self.directory = r'Songs'
        self.sheet_name = ""
# Mel-Frequency Cepstral Coefficients(MFCCs)

    def create_xls_file(self):
        ''' Here we create xls sheet of database (songs) and its features hashing values'''
        print("Please make sure your songs are stored in a directory named (Songs) ")
        self.workbook = xlwt.Workbook()
        self.sheet_name = input('sheet name: ')
        self.output = input('output file name: ')
        self.sheet = self.workbook.add_sheet(self.sheet_name)

    def fetch_songs(self):
        for subdir, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".mp3"):
                    self.paths.append(filepath)
                    self.songs_name.append(os.path.splitext(
                        os.path.basename(filepath))[0])

    def update_xls(self):
        for feature in self.features:
            self.column_counter += 1
            self.sheet.write(0, self.column_counter, feature)

        for name in self.songs_name:
            self.row_counter += 1
            self.sheet.write(self.row_counter, 0, name)

    def hashing(self):
        for i in self.paths:
            print("file.mp3: ", i)
            mp3_audio = AudioSegment.from_file(i, format="mp3")[:60000]
            wname = mktemp('.wav')  # use temporary file
            mp3_audio.export(wname, format="wav")  # convert to wav
            wavsong, samplingFrequency = librosa.load(wname, duration=60)

            mfcc = librosa.feature.mfcc(wavsong, samplingFrequency)
            chroma_stft = librosa.feature.chroma_stft(
                wavsong, samplingFrequency)  # Chroma feature
            mel = librosa.feature.melspectrogram(
                wavsong, samplingFrequency)  # mel feature

            features_list, array, hash_list = [], [], []
            features_list.append(chroma_stft)
            features_list.append(mfcc)
            features_list.append(mel)

            for i in range(3):
                array = Image.fromarray(features_list[i], mode='RGB')
                hash_code = imagehash.phash(array, hash_size=16).__str__()
                hash_list.append(hash_code)

            for hash in hash_list:
                self.column_hash += 1
                self.sheet.write(self.row_hash, self.column_hash, hash)
            self.column_hash = 0
            self.row_hash += 1
            hash_list.clear()

    def script(self):
        self.create_xls_file()
        self.fetch_songs()
        self.update_xls()
        self.hashing()
        self.workbook.save(self.output + ".xls")


### RUN ###
file = Database()
file.script()
