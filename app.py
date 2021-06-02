from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QHeaderView
from PyQt5.QtCore import QSettings, endl
from autologging import logged, TRACE, traced
from SongModel import SongModel
import numpy as np
import os
import sys
import time
import logging
import xlrd
import imagehash

# Create and configure logger
LOG_FORMAT = "%(levelname)s:%(filename)s,%(lineno)d:%(name)s.%(funcName)s:%(message)s"
logging.basicConfig(filename="Shazam.log",
                    level=TRACE,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()


@ traced
@ logged
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

        self.mixing_slider.valueChanged.connect(lambda: self.mixer())
        self.New_window.triggered.connect(lambda: self.make_new_window())
        self.Browse_songs.triggered.connect(lambda: self.browse())
        self.searchButton.clicked.connect(lambda: self.search_button())

        self.mixing_slider.setEnabled(False)

        self.selected_songs, self.paths, self.loaded_song_hashes = [], [], []
        self.songsLabel = [self.song1, self.song2]
        self.ratio = 0.5  # initial value for slider = 50
        self.database_nrows = 0

    def browse(self):
        self.selected_songs = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")
        self.selected_songs = self.selected_songs[0]
        # Check conditions: number of selected songs,
        if len(self.selected_songs) > 2:
            # Showing warning msg and return to selection panel
            self.warning_msg_generator(
                "Error in selected Songs ", "You can't select more than two songs.")
            logger.info("The user selected more than 2 songs")
            return self.browse()
        else:
            if len(self.selected_songs) == 2:
                self.mixing_slider.setEnabled(True)
            self.song_model = SongModel(self.selected_songs, self.ratio)

            for i in range(len(self.selected_songs)):
                '''# Set lables with selected files'''
                self.paths.append(os.path.basename(self.selected_songs[i]))
                self.songsLabel[i].setText(self.paths[i])

            # you can extract and hash from database-related function not here
            # self.song_model.extract_features()
            # self.hashcode = self.song_model.hashing()
            logging.info(
                "Browsing done succussfelly, song_model created as well.")

    def mixer(self):
        self.ratio = (self.mixing_slider.value() / 100)
        self.song_model.update_mixer(self.ratio)
        return self.song_model

    def hamming_distance(self, first_hash, second_hash):
        # Calculate difference between selected-song-hash and another hash in db
        ''' calculates the hamming distance between two strings which represents the differences between them '''
        difference = imagehash.hex_to_hash(
            first_hash)-imagehash.hex_to_hash(second_hash)
        return difference

    def map_value(self, inputValue, inputMin, inputMax, outputMin, outputMax):
        """map_value maps a value from a certain range to another."""

        slope = (outputMax-outputMin) / (inputMax-inputMin)
        return outputMin + slope*(inputValue-inputMin)

    def search_button(self):

        self.loaded_song_hashes = self.song_model.hashing_script()

        chroma_hash_selected_song = str(self.loaded_song_hashes[0])

        mfcc_hash_selected_song = str(self.loaded_song_hashes[1])

        mel_hash_selected_song = str(self.loaded_song_hashes[2])

        database_file = xlrd.open_workbook("featuresHashes3.xls")
        database_sheet = database_file.sheet_by_index(0)
        self.database_nrows = database_sheet.nrows - 1

        # momkn a3ml nested for w a2ll el klam da, kol 7aga leha index ad5lha fe list
        results_list = []
        results_si, results_names = [], []

        for i in range(self.database_nrows):  # -1 to ignore rows of labels
            songname_db = str(database_sheet.cell_value(rowx=i+1, colx=0))
            chroma_hash_db = str(database_sheet.cell_value(rowx=i+1, colx=1))
            mfcc_hash_db = str(database_sheet.cell_value(rowx=i+1, colx=2))
            mel_hash_db = str(database_sheet.cell_value(rowx=i+1, colx=3))

            chroma_hamming_distance = self.song_model.hamming_distance(
                chroma_hash_selected_song, chroma_hash_db)

            mfcc_hamming_distance = self.song_model.hamming_distance(
                mfcc_hash_selected_song, mfcc_hash_db)

            mel_hamming_distance = self.song_model.hamming_distance(
                mel_hash_selected_song, mel_hash_db)

            avg_diff = (chroma_hamming_distance +
                        mfcc_hamming_distance+mel_hamming_distance) / 3
            mapped_avg_diff = self.map_value(avg_diff, 0, 256, 0, 1)

            similarity_idx = int((1-mapped_avg_diff)*100)
            results_names.append(songname_db)
            results_si.append(similarity_idx)

        results_list.append(results_names)

        results_list.append(results_si)
        self.showTable(results_list)
        # momkn yb2a dict gwah list
        # results = {'song_name': songname_db, 'SI': similarity_idx}
        # update table

    def showTable(self, results):
        self.resultsTable.clear()
        self.resultsTable.setRowCount(0)
        # set row and column count
        self.resultsTable.setRowCount(self.database_nrows)
        self.resultsTable.setColumnCount(2)
        # self.similarityResults.sort(key= lambda x: x[1], reverse=True)

        # displaying the data in the table
        for row in range(self.database_nrows):

            song_name = QTableWidgetItem(str(results[0][row]))
            similarity_idx = QTableWidgetItem(str((results[1][row])))
            self.resultsTable.setItem(row, 0, song_name)
            self.resultsTable.setItem(row, 1, similarity_idx)
            # self.resultsTable.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.Stretch)

        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        self.resultsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.resultsTable.setHorizontalHeaderLabels(
            ['Matching Songs', 'Similarity Index'])

        self.resultsTable.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.resultsTable.horizontalHeader().setStyleSheet("color: rgb(47, 47, 77)")
        self.resultsTable.verticalHeader().setStyleSheet("color: rgb(47, 47, 77)")
        self.resultsTable.sortItems(1, QtCore.Qt.AscendingOrder)
        self.resultsTable.show()

    def make_new_window(self):
        self.new_window = Shazam()
        self.new_window.show()

    def warning_msg_generator(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        return msg.exec_()


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
