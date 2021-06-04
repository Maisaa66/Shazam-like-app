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
        self.New_window.triggered.connect(lambda: self.new_window())
        self.Browse_songs.triggered.connect(lambda: self.browse())
        self.searchButton.clicked.connect(lambda: self.search())

        
        self.mixing_slider.setEnabled(False)
        
        self.selected_songs, self.paths, self.song_hashes = [], [], []
        self.songsLabel = [self.song1, self.song2]
        self.db_nrows,  self.ratio = 0, 0.5  # initial value for slider = 50

    def browse(self):

        self.selected_songs = QFileDialog.getOpenFileNames(
            self, 'Choose the Songs', os.getenv('HOME'), "mp3(*.mp3)")
        self.selected_songs = self.selected_songs[0]

        if len(self.selected_songs) > 2:
            self.warning_msg_generator(
                "Error in selected Songs ", "You can't select more than two songs.")
            logger.info("The user selected more than 2 songs")
            return self.browse()
        else:
            self.song_model = SongModel(self.selected_songs, self.ratio)

            if len(self.selected_songs) == 2:
                self.mixing_slider.setEnabled(True)  # Enable slider
                if self.song_model.check():
                    # Check sampling freq of the two selected songs.
                    self.warning_msg_generator(
                        "Error in selected Songs ", "User selected 2 songs with different sampling freq.")
                    # clear selection of old songs.
                    self.selected_songs.clear()
                    return self.browse()

            for i in range(len(self.selected_songs)):
                '''# Set lables with selected files'''
                self.paths.append(os.path.basename(self.selected_songs[i]))
                self.songsLabel[i].setText(self.paths[i])

            logging.info(
                "Browsing done succussfelly.")

    def mixer(self):
        self.ratio = (self.mixing_slider.value() / 100)
        self.song_model.mix_songs(self.ratio)
        return self.song_model

    # def map_value(self, inputValue, inputMin, inputMax, outputMin, outputMax):
    #     """map_value maps a value from a certain range to another."""

    #     slope = (outputMax-outputMin) / (inputMax-inputMin)
    #     return outputMin + slope*(inputValue-inputMin)

    def search(self):

        # [0]: mfcc hash ,, [1]: chroma hass ,, [2]: mel hash
        self.song_hashes = self.song_model.hashing_script()

        database_file = xlrd.open_workbook("featuresHashes.xls")
        database_sheet = database_file.sheet_by_index(0)
        self.db_nrows = database_sheet.nrows - 1

        # momkn a3ml nested for w a2ll el klam da, kol 7aga leha index ad5lha fe list
        results = [[], []]  # [0]: names ,, [1]: SI
        db_fetcher = []  # [1]: mfcc hash ,, [2]: chroma hass ,, [3]: mel hash ,, [0]: song name
        hamming_d_list = []  # [0]: mfcc ,, [1]: chroma ,, [2]: mel

        for i in range(self.db_nrows):  # -1 to ignore rows of labels
            for j in range(4):
                db_fetcher[j] = str(
                    database_sheet.cell_value(rowx=i+1, colx=j))
            for k in range(3):
                hamming_d_list[k] = self.song_model.hamming_distance(
                    db_fetcher[k+1], self.song_hashes[k])

            mapped_avg_diff = (sum(hamming_d_list) / len(hamming_d_list)) / 256
            similarity_idx = int((1-mapped_avg_diff)*100)
            results[0].append(db_fetcher[0])
            results[1].append(similarity_idx)

        self.showTable(results)

    def showTable(self, results):
        #start with clearing all results to update them after changing slider value.
        self.resultsTable.clear()
        self.resultsTable.setRowCount(0)
            
        # set row count same as database n.rows
        self.resultsTable.setRowCount(self.db_nrows)
        self.resultsTable.setColumnCount(2)
        
        ''' self.similarityResults.sort(key= lambda x: x[1], reverse=True) '''

        # displaying results
        for row in range(self.db_nrows):

            song_name = QTableWidgetItem(str(results[0][row]))
            similarity_idx = QTableWidgetItem(str((results[1][row])))
            self.resultsTable.setItem(row, 0, song_name)
            self.resultsTable.setItem(row, 1, similarity_idx)

        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        self.resultsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.resultsTable.setHorizontalHeaderLabels(['Matching Songs', 'Similarity Index'])

        self.resultsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.resultsTable.horizontalHeader().setStyleSheet("color: rgb(47, 47, 77)")
        self.resultsTable.verticalHeader().setStyleSheet("color: rgb(47, 47, 77)")
        self.resultsTable.sortItems(1, QtCore.Qt.DescendingOrder)
        self.resultsTable.show()


    def new_window(self):
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

''' 
QUESTIONS:
for Dr.Tamer:
    1- function for maping or not
    2- extract lists in many variables or just iterate on it
    3- naming variables, long or short
    4- how to name classes? for example: songModel
for Maisaa:
    1-why do we create temp file for converting from mp3 to wav

for Essam:
    1- mapping?
    2-
''' 