# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1010, 778)
        mainWindow.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(47, 47, 77);")
        self.Browse_songs = QAction(mainWindow)
        self.Browse_songs.setObjectName(u"Browse_songs")
        self.actionClear = QAction(mainWindow)
        self.actionClear.setObjectName(u"actionClear")
        self.actionNew_tab = QAction(mainWindow)
        self.actionNew_tab.setObjectName(u"actionNew_tab")
        self.New_window = QAction(mainWindow)
        self.New_window.setObjectName(u"New_window")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 2, 3, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.searchButton = QPushButton(self.centralwidget)
        self.searchButton.setObjectName(u"searchButton")

        self.gridLayout_2.addWidget(self.searchButton, 0, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.resultsTable = QTableWidget(self.centralwidget)
        self.resultsTable.setObjectName(u"resultsTable")
        self.resultsTable.setEnabled(True)
        self.resultsTable.setStyleSheet(u"")
        self.resultsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.resultsTable.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.resultsTable.setAlternatingRowColors(False)

        self.gridLayout_2.addWidget(self.resultsTable, 1, 0, 1, 3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 75 11pt \"MS Shell Dlg 2\";")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 3, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line, 3, 0, 1, 4)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 2, 3, 1, 1)

        self.mixing_slider = QSlider(self.centralwidget)
        self.mixing_slider.setObjectName(u"mixing_slider")
        self.mixing_slider.setMaximum(100)
        self.mixing_slider.setSingleStep(10)
        self.mixing_slider.setPageStep(10)
        self.mixing_slider.setValue(50)
        self.mixing_slider.setOrientation(Qt.Horizontal)
        self.mixing_slider.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_3.addWidget(self.mixing_slider, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 0, 1, 4)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 9pt \"MS Shell Dlg 2\";")
        self.label_4.setMidLineWidth(2)

        self.gridLayout_3.addWidget(self.label_4, 2, 1, 1, 1, Qt.AlignHCenter)

        self.song1 = QLabel(self.centralwidget)
        self.song1.setObjectName(u"song1")
        self.song1.setStyleSheet(u"background-color: rgb(74, 74, 110);\n"
"color: rgb(255, 255, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";")

        self.gridLayout_3.addWidget(self.song1, 1, 0, 1, 1)

        self.song2 = QLabel(self.centralwidget)
        self.song2.setObjectName(u"song2")
        self.song2.setStyleSheet(u"background-color: rgb(74, 74, 110);\n"
"color: rgb(255, 255, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";")

        self.gridLayout_3.addWidget(self.song2, 1, 2, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 0, 1, 1, 1)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1010, 22))
        self.menufile = QMenu(self.menubar)
        self.menufile.setObjectName(u"menufile")
        self.menufile.setStyleSheet(u"selection-background-color: rgb(35, 35, 50);\n"
"gridline-color: rgb(255, 255, 255);")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menufile.menuAction())
        self.menufile.addAction(self.New_window)
        self.menufile.addAction(self.Browse_songs)
        self.menufile.addAction(self.actionClear)

        self.retranslateUi(mainWindow)
        self.mixing_slider.valueChanged.connect(self.label_4.setNum)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Music Discovery", None))
        self.Browse_songs.setText(QCoreApplication.translate("mainWindow", u"Browse songs", None))
#if QT_CONFIG(shortcut)
        self.Browse_songs.setShortcut(QCoreApplication.translate("mainWindow", u"Ctrl+B", None))
#endif // QT_CONFIG(shortcut)
        self.actionClear.setText(QCoreApplication.translate("mainWindow", u"Clear", None))
#if QT_CONFIG(shortcut)
        self.actionClear.setShortcut(QCoreApplication.translate("mainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionNew_tab.setText(QCoreApplication.translate("mainWindow", u"New tab", None))
        self.New_window.setText(QCoreApplication.translate("mainWindow", u"New window", None))
#if QT_CONFIG(shortcut)
        self.New_window.setShortcut(QCoreApplication.translate("mainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.searchButton.setText(QCoreApplication.translate("mainWindow", u"Search", None))
        self.label_3.setText(QCoreApplication.translate("mainWindow", u" Similar songs", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\"><br/></span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.label_4.setWhatsThis(QCoreApplication.translate("mainWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_4.setText(QCoreApplication.translate("mainWindow", u"50", None))
        self.song1.setText(QCoreApplication.translate("mainWindow", u" Song 1", None))
        self.song2.setText(QCoreApplication.translate("mainWindow", u" Song 2", None))
        self.menufile.setTitle(QCoreApplication.translate("mainWindow", u"File", None))
    # retranslateUi

