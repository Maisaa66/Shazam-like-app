import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
        # self.sorted_table()
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def sorted_table(self):
        mywidget = QTableWidget()
        mywidget.insertColumn(0)
        mywidget.insertColumn(1)
        list1 = [25,1,7]
        list2 = [3,15,1]
        for num in range(len(list1)):
            mywidget.insertRow(num)
            item = QTableWidgetItem()
            item.setData(QtCore.Qt.EditRole, list1[num])
            mywidget.setItem(num, 0, item)
            mywidget.setItem(num, 1, QTableWidgetItem(str(list2[num])))
        mywidget.sortItems(0, QtCore.Qt.AscendingOrder)
        mywidget.show()
    def createTable(self):
       # Create table
       
        self.tableWidget = QTableWidget()
        self.tableWidget.insertColumn(0)
        self.tableWidget.insertColumn(1)
        list1 = [25,1,7]
        list2 = [3,15,1]
        for num in range(len(list1)):
            self.tableWidget.insertRow(num)
            item = QTableWidgetItem()
            item.setData(QtCore.Qt.EditRole, list1[num])
            self.tableWidget.setItem(num, 0, item)
            self.tableWidget.setItem(num, 1, QTableWidgetItem(str(list2[num])))
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()
        
        # self.tableWidget = QTableWidget()
        # self.tableWidget.setRowCount(4)
        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        # self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        # self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        # self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        # self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        # self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        # self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(),
                  currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
