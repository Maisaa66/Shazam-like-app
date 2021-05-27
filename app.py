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
        self.songsLabel = [self.song1, self.song2]
        self.mixingSlider.valueChanged.connect(lambda: self.Mixer())
        self.paths = []
        self.featuresMethods = ['spectral_centroid', 'spectral_rolloff']
        self.features = []

        self.New_window.triggered.connect(self.make_new_window)
        self.Browse_songs.triggered.connect(lambda: self.browse())

    def browse(self):

        self.songName, self.select_song = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")
        # print(self.songName)

        for i, name in enumerate(self.songName, start=1):
            # extract file name
            self.paths.append(os.path.basename(name))
        # print(name)

        for i in range(2):
            self.songsLabel[i].setText(self.paths[i])

        for i in range(2):
            mp3_audio = AudioSegment.from_file(self.songName[i], format="mp3")[
                :60000]  # read mp3 & take only the first 60 seconds
            waveName = mktemp('.wav')  # use temporary file
            mp3_audio.export(waveName, format="wav")  # convert to wav
            self.wavesongs[i], self.samplingFrequencies[i] = librosa.load(
                waveName)

    def Mixer(self):
        mixingRatio = self.mixingSlider.value() / 100
        self.newSong = mixingRatio * \
            self.wavesongs[0] + (1-mixingRatio) * self.wavesongs[1]
        self.sepctrogram()

    def sepctrogram(self):
        spectro = librosa.amplitude_to_db(
            np.abs(librosa.stft(self.newSong)), ref=np.max)
        self.saveImage("mixingSpectrogram.png", spectro, "linear",
                       22050)  # 22050 is the default
        self.extractFeatures()

    def saveImage(self, path, viewed, y, sampleRate):
        Spectro_Path = path
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[],
                   yticks=[])  # Remove the white edge
        librosa.display.specshow(viewed, y_axis=y, sr=sampleRate)
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()

    def extractFeatures(self):
        self.features.append(librosa.feature.spectral_centroid(
            y=self.newSong, sr=self.samplingFrequencies[0]))

        self.features.append(librosa.feature.spectral_rolloff(
            y=self.newSong, sr=self.samplingFrequencies[0]))

        for i in range(2):
            self.saveImage(self.featuresMethods[i]+'.png',
                           self.features[i].T, None, self.samplingFrequencies[0])

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
