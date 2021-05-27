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
        self.paths = []

        self.New_window.triggered.connect( self.make_new_window)
        self.Browse_songs.triggered.connect(lambda: self.browse())

    def browse(self):

        self.songName, self.select_song = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")
        #print(self.songName)

        for i, name in enumerate(self.songName, start=1):
            # extract file name
            self.paths.append(os.path.basename(name))
        #print(name)

        for i in range(2):
            self.songsLabel[i].setText(self.paths[i])

        for i in range(2):
            mp3_audio = AudioSegment.from_file(self.songName[i], format="mp3")[
                :60000]  # read mp3 & take only the first 60 seconds
            waveName = mktemp('.wav')  # use temporary file
            mp3_audio.export(waveName, format="wav")  # convert to wav
            self.wavesongs[i], self.samplingFrequencies[i] = librosa.load(
                waveName)


        
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
