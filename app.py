from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QTableWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSettings
import os
import sys
import librosa
from pydub import AudioSegment
import librosa.display
import numpy as np
from tempfile import mktemp
import pylab
from PIL import Image
import imagehash


class Shazam(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UI.ui', self)
        self.settings = QSettings("Voice Recognizer", 'App')
        try:
            # Saving the last position and size of the application window
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

        self.wavesongs = [0, 0]
        self.samplingFrequencies = [0, 0]
        self.newSong = []
        self.songsLabel = [self.song1, self.song2]
        self.mixingSlider.valueChanged.connect(lambda: self.Mixer())
        self.paths = []
        self.featuresMethods = ['spectral_centroid', 'spectral_rolloff']
        self.features = []

        self.New_window.triggered.connect(self.make_new_window)
        self.Browse_songs.triggered.connect(lambda: self.browse())

    def browse(self):

        self.songName, _ = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")
        # print(self.songName)

        for i, name in enumerate(self.songName, start=1):
            # extract file name
            self.paths.append(os.path.basename(name))
        # print(name)

        for i in range(len(self.songName)):
            # add the song name in UI_label
            self.songsLabel[i].setText(self.paths[i])
        self.converting(self.songName)
        print(len(self.songName))

        # for i in range(len(self.songName)):
        #     mp3_audio = AudioSegment.from_file(self.songName[i], format="mp3")[
        #         :60000]  # read mp3 & take only the first 60 seconds
        #     waveName = mktemp('.wav')  # use temporary file
        #     mp3_audio.export(waveName, format="wav")  # convert to wav
        #     self.wavesongs[i], self.samplingFrequencies[i] = librosa.load(
        #         waveName)

    def converting(self, path):

        for i in range(len(path)):
            mp3_audio = AudioSegment.from_file(path[i], format="mp3")[
                :60000]  # read mp3 & take only the first 60 seconds
            wname = mktemp('.wav')  # use temporary file
            mp3_audio.export(wname, format="wav")  # convert to wav
            self.wavesongs[i], self.samplingFrequencies[i] = librosa.load(
                wname)

        self.spectrogram(self.wavesongs)
        self.extractFeatures(self.wavesongs)

    def Mixer(self):
        mixingRatio = self.mixingSlider.value() / 100
        self.newSong.append(
            np.add(mixingRatio * self.wavesongs[0], self.wavesongs[1] * (1-mixingRatio)))
        self.spectrogram(self.newSong)
        self.extractFeatures(self.newSong)

    def spectrogram(self, song):
        for i in range(len(self.paths)):
            spectroPath = "mixingSpectrogram"+str(i)+".png"
            D = librosa.amplitude_to_db(
                np.abs(librosa.stft(song[i])), ref=np.max)
            self.saveImage(spectroPath, D, "linear",
                           22050)  # 22050 is the default

    def saveImage(self, path, viewed, y, sampleRate):
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[],
                   yticks=[])  # Remove the white edge
        librosa.display.specshow(viewed, y_axis=y, sr=sampleRate)
        pylab.savefig(path, bbox_inches=None, pad_inches=0)
        pylab.close()

    def extractFeatures(self, song):
        for i in range(len(self.paths)):
            self.features.append(librosa.feature.chroma_stft(
                y=song[i], sr=self.samplingFrequencies[0]))

            self.features.append(librosa.feature.mfcc(
                y=song[i], sr=self.samplingFrequencies[0]))

        for i in range(2):
            self.saveImage(self.featuresMethods[i]+'.png',
                           self.features[i].T, None, self.samplingFrequencies[0])

        self.hashingData(self.features)

    def hashingData(self, features):
        for i in range(len(features)):
            # We will use Perceptual hashing
            hashcode = imagehash.phash(Image.fromarray(features[i]))
            print(str(hashcode))

    def showTable(self, matchingSongs, similarityIndex):
        # set row and column count
        self.resultsTable.setRowCount(len(matchingSongs))
        self.resultsTable.setColumnCount(2)
        
        #displaying the data in the table
        for row in range(len(matchingSongs)):

            song_name = QTableWidgetItem(str(matchingSongs[row]))
            SI = QTableWidgetItem(str(similarityIndex[row]))
            self.resultsTable.setItem(row, 0, song_name)
            self.resultsTable.setItem(row, 1, SI)
            self.resultsTable.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.Stretch)

        self.resultsTable.setHorizontalHeaderLabels(['Matching Songs', 'Similarity Index'])
        self.resultsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.resultsTable.horizontalHeader().setStyleSheet("color: rgb(47, 47, 77)")
        self.resultsTable.verticalHeader().setStyleSheet("color: rgb(47, 47, 77)")
            
        self.resultsTable.show()

    def make_new_window(self):
        self.new_window = Shazam()
        self.new_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("CUFE")
    app.setOrganizationDomain("CUFEDomain")
    app.setApplicationName("Voice Recognizer")
    application = Shazam()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
