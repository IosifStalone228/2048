from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRect
import sys
import os
import copy
import random


class GameForm(QMainWindow):
    def __init__(self, parent=None):
        super(GameForm, self).__init__(parent)
        self.initUi()
        # Определяет цвет для каждого элемента с номером
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
                       8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                       64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 207, 114),
                       512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114),
                       32768: (237, 207, 114), 65536: (237, 207, 114), 131072: (237, 207, 114),
                       262144: (237, 207, 114), 524288: (237, 207, 114), 1048576: (237, 207, 114)}
        self.initGameData()

    def initUi(self):
        self.setWindowTitle("2048")
        self.resize(505, 720)
        self.setFixedSize(self.width(), self.height())
        self.initGameOpt()

    def initGameOpt(self):
        ''' Initialize game configuration'''
        self.lbFont = QFont('SimSun', 12)
        self.lgFont = QFont('SimSun', 50)
        self.nmFont = QFont('SimSun', 36)
    def initGameData(self):
        ''' Initialize game numbers'''
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1

        self.curScore = 0
        self.bstScore = 0
        # Выгружает максимально-набранный счёт
        if os.path.exists("top_score.iniscore.ini"):
            with open("top_score.iniscore.ini", "r") as f:
                self.bstScore = int(f.read())

    def paintEvent(self, e):
        ''' Rewrite drawing events'''
        qp = QPainter()
        qp.begin(self)
        self.drawGameGraph(qp)
        qp.end()

    def keyPressEvent(self, e):
        keyCode = e.key()
        ret = False
        if keyCode == Qt.Key_Left:
            ret = self.move("Left")
        elif keyCode == Qt.Key_Right:
            ret = self.move("Right")
        elif keyCode == Qt.Key_Up:
            ret = self.move("Up")
        elif keyCode == Qt.Key_Down:
            ret = self.move("Down")
        else:
            pass

        if ret:
            self.repaint()

    def closeEvent(self, e):
        # Save the highest score
        with open("top_score.ini", "w") as f:
            f.write(str(self.bstScore))

    def drawGameGraph(self, qp):
        ''' Draw game graphics'''
        self.drawLog(qp)
        self.drawLabel(qp)
        self.drawScore(qp)
        self.drawBg(qp)
        self.drawTiles(qp)

    def drawScore(self, qp):
        ''' draw score'''
        qp.setFont(self.lbFont)
        fontsize = self.lbFont.pointSize()
        scoreLabelSize = len(u"SCORE") * fontsize
        bestLabelSize = len(u"BEST") * fontsize
        curScoreBoardMinW = 15 * 2 + scoreLabelSize  # Минимальная ширина колонки со счётом
        bstScoreBoardMinW = 15 * 2 + bestLabelSize  # Идеальная ширина колонки со счётом
        curScoreSize = len(str(self.curScore)) * fontsize
        bstScoreSize = len(str(self.bstScore)) * fontsize
        curScoreBoardNedW = 10 + curScoreSize
        bstScoreBoardNedW = 10 + bstScoreSize
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)
        bstScoreBoardW = max(bstScoreBoardMinW, bstScoreBoardNedW)
        qp.setBrush(QColor(187, 173, 160))
        qp.setPen(QColor(187, 173, 160))
        qp.drawRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 50)
        qp.drawRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 50)

        bstLabelRect = QRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 25)
        bstScoreRect = QRect(505 - 15 - bstScoreBoardW, 65, bstScoreBoardW, 25)
        scoerLabelRect = QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 25)
        curScoreRect = QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 65, curScoreBoardW, 25)

        qp.setPen(QColor(238, 228, 218))
        qp.drawText(bstLabelRect, Qt.AlignCenter, u"BEST")
        qp.drawText(scoerLabelRect, Qt.AlignCenter, u"SCORE")

        qp.setPen(QColor(255, 255, 255))
        qp.drawText(bstScoreRect, Qt.AlignCenter, str(self.bstScore))
        qp.drawText(curScoreRect, Qt.AlignCenter, str(self.curScore))

    def drawBg(self, qp):
        ''' Draw a background image'''
        col = QColor(187, 173, 160)
        qp.setPen(col)

        qp.setBrush(QColor(187, 173, 160))
        qp.drawRect(15, 150, 475, 475)  # Создаёт игровое поле

    def drawLog(self, qp):
        ''' Draw Logo'''
        pen = QPen(QColor(255, 93, 29), 15)
        qp.setFont(self.lgFont)
        qp.setPen(pen)
        qp.drawText(QRect(10, 0, 150, 130), Qt.AlignCenter, "2048")

    def drawLabel(self, qp):
        ''' Draw all label information'''
        qp.setFont(self.lbFont)
        qp.setPen(QColor(119, 110, 101))
        qp.drawText(15, 134, u"Merge the same numbers and get 2048!")
        qp.drawText(15, 660, u"How to play:")
        qp.drawText(45, 680, u"Use -> <- arrow keys to move the square.")
        qp.drawText(45, 700, u"When two squares with the same number meet together, they will form one!")

    def drawTiles(self, qp):
        ''' Draw a digital background'''
        qp.setFont(self.nmFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]

                qp.setPen(QColor(*color))
                qp.setBrush(QColor(*color))
                qp.drawRect(30 + col * 115, 165 + row * 115, 100, 100)
                size = self.nmFont.pointSize() * len(str(value))
                while size > 100 - 15 * 2:
                    self.nmFont = QFont('SimSun', self.nmFont.pointSize() * 4 // 5)
                    qp.setFont(self.nmFont)
                    size = self.nmFont.pointSize() * len(str(value))
                print("[%d][%d]: value[%d] weight: %d" % (row, col, value, size))

                # Как планируется отображение квадратиков с номерами
                if value == 2 or value == 4:
                    qp.setPen(QColor(119, 110, 101))
                else:
                    qp.setPen(QColor(255, 255, 255))
                if value != 0:
                    rect = QRect(30 + col * 115, 165 + row * 115, 100, 100)
                    qp.drawText(rect, Qt.AlignCenter, str(value))

    def putTile(self):
        ''' Find an empty position (the value is 0) and fill it with 2 or 4 randomly'''
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:
                    available.append((row, col))
        if available:
            row, col = available[random.randint(0, len(available) - 1)]
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            return True
        return False

    def merge(self, row):
        ''' merge a row or column'''
        pair = False
        newRow = []
        for i in range(len(row)):
            if pair:
                newRow.append(2 * row[i])
                self.curScore += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                else:
                    newRow.append(row[i])
        return newRow

    def slideUpDown(self, isUp):
        ''' Move the number grid up and down'''
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            cvl = []
            for row in range(numRows):
                if self.data[row][col] != 0:
                    cvl.append(self.data[row][col])
            if len(cvl) >= 2:
                cvl = self.merge(cvl)  # Добавляет одинаковые числа
            for i in range(numRows - len(cvl)):
                if isUp:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)

            print("row=%d" % row)
            row = 0
            for row in range(numRows):
                self.data[row][col] = cvl[row]

        return oldData != self.data  # ВОзвращает ответ на запрос изменились ли данные объекта

    def slideLeftRight(self, isLeft):
        ''' Move the number grid in the left and right directions'''
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = []
            for col in range(numCols):
                if self.data[row][col] != 0:
                    rvl.append(self.data[row][col])

            if len(rvl) >= 2:
                rvl = self.merge(rvl)

            for i in range(numCols - len(rvl)):
                if isLeft:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)

            col = 0
            for col in range(numCols):
                self.data[row][col] = rvl[col]

        return oldData != self.data

    def move(self, direction):
        ''' Move the number grid'''
        isMove = False
        if direction == "Up":
            isMove = self.slideUpDown(True)
        elif direction == "Down":
            isMove = self.slideUpDown(False)
        elif direction == "Left":
            isMove = self.slideLeftRight(True)
        elif direction == "Right":
            isMove = self.slideLeftRight(False)
        else:
            pass

        if not isMove:
            return False

        self.putTile()  # Add a number
        if self.curScore > self.bstScore:
            self.bstScore = self.curScore

        if self.isGameOver():
            button = QMessageBox.warning(self, "Warning", u"The game is over, do you want to start again?",
                                         QMessageBox.Ok | QMessageBox.No,
                                         QMessageBox.Ok)

            if button == QMessageBox.Ok:
                self.initGameOpt()
                bstScore = self.bstScore
                self.initGameData()
                self.bstScore = bstScore
                return True
            else:
                return False
        else:
            return True

    def isGameOver(self):
        ''' Determine whether the game cannot continue'''
        copyData = copy.deepcopy(self.data)  # Сохраняет данные
        curScore = self.curScore

        flag = False
        if not self.slideUpDown(True) and not self.slideUpDown(False) and \
                not self.slideLeftRight(True) and not self.slideLeftRight(False):
            flag = True  # не может больше перемещаться
        self.curScore = curScore
        if not flag:
            self.data = copyData  # Всё ещё может перемещаться и хранить первоначальные данные
        return flag


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = GameForm()
    form.show()
    sys.exit(app.exec_())