from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QHeaderView
from PyQt5.QtCore import QSettings
from autologging import logged, TRACE, traced
from songmodel import SongModel
import os
import sys
import logging
import xlrd

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
        self.ui = uic.loadUi('Shazam.ui', self)
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

    def search(self):
        # calculating all hashes for selected song
        self.song_hashes = self.song_model.hashing_script()

        database_file = xlrd.open_workbook("Database.xls")
        database_sheet = database_file.sheet_by_index(0)
        self.db_nrows = database_sheet.nrows - 1  # ignoring 1st row of labels.

        results = [[], []]

        '''
        GUIDE:     
        # self.song_hashes[0]: mfcc hash, [1]: chroma hash, [2]: mel hash
        # results[0]: songs names, [1]: similarity percentages
        # tmp_fetcher[0][0]: db_song_name, [0][1]: mfcc hash, [0][2]: chroma hash, [0][3]: mel hash
        # tmp_fetcher[1][0]:  = 0 always. Added to avoid creating two nested loops, won't affect any result., [1][1,2,3]: hamming results
        '''

        for i in range(self.db_nrows):
            # reset values by clearing the temporary list.
            tmp_fetcher = [[0]*4, [0]*4]
            tmp_fetcher[0][0] = str(
                database_sheet.cell_value(rowx=i+1, colx=0))  # fetch song name.

            for j in range(1, 4):
                tmp_fetcher[0][j] = str(database_sheet.cell_value(
                    rowx=i+1, colx=j))  # fetch three hashes
                tmp_fetcher[1][j] = self.song_model.hamming_distance(
                    tmp_fetcher[0][j], self.song_hashes[j-1])  # compare hashes

            # calculate the avg difference and map it (0,1)
            mapped_avg_diff = (sum(tmp_fetcher[1]) / 3) / 256
            # SI = 1 - avg difference
            similarity_idx = int((1-mapped_avg_diff)*100)
            results[0].append(tmp_fetcher[0][0])  # store the name of that song
            results[1].append(similarity_idx)  # store SI of that song

        self.table(results)

    def table(self, results):
        # start with clearing all results to update them after changing slider value.
        self.resultsTable.clear()
        self.resultsTable.setRowCount(0)

        # set row count same as database n.rows
        self.resultsTable.setRowCount(self.db_nrows)
        self.resultsTable.setColumnCount(2)

        # displaying results
        for row in range(self.db_nrows):

            song_name = QTableWidgetItem(str(results[0][row]))
            similarity_idx = QTableWidgetItem(str((results[1][row])))
            self.resultsTable.setItem(row, 0, song_name)
            self.resultsTable.setItem(row, 1, similarity_idx)

        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        self.resultsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.resultsTable.setHorizontalHeaderLabels(
            ['Matching Songs', 'Similarity Index'])
        self.resultsTable.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
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
