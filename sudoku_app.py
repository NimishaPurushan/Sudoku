from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Sudoku:
    def __init__(self, matrix, table_widget):
        self.matrix = matrix
        self.table_widget = table_widget
        self.solve()

    @staticmethod
    def check(num_row, num_column, num, matrix):
        for row in range(len(matrix)):
            if num == matrix[row][num_column] and row != num_row:
                return False
        for column in range(len(matrix)):
            if num == matrix[num_row][column] and column != num_column:
                return False
        row_block = num_row//3
        column_block = num_column//3
        for column in range(column_block*3, column_block*3 + 3):
            for row in range(row_block * 3, row_block * 3 + 3):
                if num == matrix[row][column] and num_row != row:
                    return False
        return True

    def solve(self):
        try:
            elements = self.find_empty()
            if not elements:
                return True
            else:
                for num in range(1, 10):
                    if self.check(elements[0], elements[1], num, self.matrix):
                        self.matrix[elements[0]][elements[1]] = num
                        if self.solve():
                            return True
                        self.matrix[elements[0]][elements[1]] = ""
            return False
        except Exception as err:
            print(err)

    def find_empty(self):
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                if not self.matrix[row][column]:
                    return row, column
        return None


class WindowWidget(QWidget):

    board = [
        [7, 8, "", 4, "", "", 1, 2, ""],
        [6, "", "", "", 7, 5, "", "", 9],
        ["", "", "", 6, "", 1, "", 7, 8],
        ["", "", 7, "", 4, "", 2, 6, ""],
        ["", "", 1, "", 5, "", 9, 3, ""],
        [9, "", 4, "", 6, "", "", "", 5],
        ["", 7, "", 3, "", "", "", 1, 2],
        [1, 2, "", "", "", 7, 4, "", ""],
        ["", 4, 9, 2, "", 6, "", "", 7]
    ]

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Lets play sudoku")
        self.setGeometry(100, 100, 555, 675)
        # self.showMaximized()
        self.setFixedSize(550, 550)

        self.button = QPushButton('Solve')
        self.create_button()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(3)
        self.setLayout(self.layout)
        #self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget = QTableWidget()
        self.create_table()
        self.layout.addWidget(self.tableWidget, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.button, alignment=Qt.AlignBottom)
        #self.tableWidget.setGeometry(50, 50, 500, 500)
        self.tableWidget.setFixedSize(450, 450)
        self.button.clicked.connect(self.solve)

    def create_button(self):
        self.button.setFont(self.font())
        self.button.setStyleSheet("background-color: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #8D99AA, stop:1 #8394AA)")
        self.button.setFixedHeight(25)
        self.button.setText("Lets Solve")

    def create_table(self):
        font = self.font()
        font.setPointSize(10)
        self.tableWidget.setRowCount(9)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(45)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget.setStyleSheet("border-radius:50px;")
        self.tableWidget.setFont(font)
        for row in range(0, 9):
            for column in range(0, 9):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(self.board[row][column])))
        self.tableWidget.move(20, 0)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def solve(self):
        matrix = []
        if self.button.text() == "Solve new":
            for row in range(0, 9):
                for column in range(0, 9):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(self.board[row][column])))
            self.button.setText("Lets Solve")
        else:
            for row in range(self.tableWidget.rowCount()):
                data = []
                for column in range(self.tableWidget.columnCount()):
                    try:
                        data.append(int(self.tableWidget.item(row, column).text()))
                    except ValueError:
                        data.append(self.tableWidget.item(row, column).text())
                matrix.append(data)
            sudoku_solver = Sudoku(matrix, self.tableWidget)
            for row in range(0, 9):
                for column in range(0, 9):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(sudoku_solver.matrix[row][column])))
                    self.tableWidget.item(row, column).setBackground(QColor(100, 100, 150))
            self.button.setText("Solve new")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style = QStyleFactory.create('Fusion')
    app.setStyle(style)
    window = WindowWidget()
    window.show()
    ex = app.exec_()

