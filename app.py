from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QTableWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSettings
import os
import sys
import librosa
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import numpy as np
from PIL import Image
# import imagehash
import pylab


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

        self.Browse_songs.triggered.connect(lambda: self.browse())

    def browse(self):
        """
        - Showing a dialog for choosing desired file
        - Convert the loaded file into array and insert it in the system
        - load only the first minute of any song
        """

        self.songName, notUSed = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")

        for index, name in enumerate(self.songName, start=1):
            # extract file name
            self.paths.append(os.path.basename(name))

        for i in range(2):
            self.songsLabel[i].setText(self.paths[i])

        # Converting mp3 to .wav formate

        for i in range(2):
            mp3_audio = AudioSegment.from_file(self.songName[i], format="mp3")[
                :60000]  # read mp3
            wname = mktemp('.wav')  # use temporary file
            mp3_audio.export(wname, format="wav")  # convert to wav
            self.wavesongs[i], self.samplingFrequencies[i] = librosa.load(
                wname)
        self.resultsTable.clearContents()

    def Mixer(self):
        mixingRatio = self.mixingSlider.value() / 100
        self.newSong = np.add(mixingRatio *
                              self.wavesongs[0], self.wavesongs[1] * (1-mixingRatio))
        self.spectrogram()

<<<<<<< HEAD
    # def spectrogram(self):
    #     D = librosa.amplitude_to_db(
    #         np.abs(librosa.stft(self.newSong)), ref=np.max)
    #     self.saveImage("mixingSpectrogram.png", D, "linear",
    #                    22050)  # 22050 is the default
    #     self.extractFeatures()

    # def saveImage(self, path, viewed, y, sampleRate):
    #     Spectro_Path = path
    #     pylab.axis('off')  # no axis
    #     pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[],
    #                yticks=[])  # Remove the white edge
    #     librosa.display.specshow(viewed, y_axis=y, sr=sampleRate)
    #     pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
    #     pylab.close()

    def extractFeatures(self):
        self.features.append(librosa.feature.spectral_centroid(
            y=self.newSong, sr=self.samplingFrequencies[0]))

        self.features.append(librosa.feature.spectral_rolloff(
            y=self.newSong, sr=self.samplingFrequencies[0]))

        for i in range(2):
            self.saveImage(self.featuresMethods[i]+'.png',
                           self.features[i].T, None, self.samplingFrequencies[0])
=======
    def Mixer(self):
        mixingRatio = self.mixingSlider.value() / 100
        self.newSong = mixingRatio * \
            self.wavsongs[0] + (1-mixingRatio) * self.wavesongs[1]
        self.spectrogram()

    def sepctrogram(self):
        spectro = librosa.amplitude_to_db(
            np.abs(librosa.stft(self.newSong)), ref=np.max)
        self.saveImage("mixingSpectrogram.png", spectro, "linear",
                       22050)  # 22050 is the default
        self.extractFeatures()
        
        
        
    def make_new_window(self):
        self.new_window = Shazam()
        self.new_window.show()
>>>>>>> 36ff0a494bcc52fda4b529054780c1e77cbb4645


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
