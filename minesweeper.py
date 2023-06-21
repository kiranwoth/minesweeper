from PyQt6.QtGui import (
    QAction, QFont, QPainter, QColor, QImage, QPixmap, QIcon, QPen
    )
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, 
    QGridLayout, QToolBar, QDialogButtonBox, QMessageBox
    )
from random import randrange

#TODO
#colour global variables
#       in dict probably
#TODO
#image global variables
#       in dict probably

DIFFICULTIES = {
    0: {
        "x": 9,
        "y": 9,
        "mines": 10
    },
    1: {
        "x": 16,
        "y": 16,
        "mines": 40
    },
    2: {
        "x": 30,
        "y": 16,
        "mines": 99
    }
}

COLOUR_NUM = {
    1: QColor("blue"),
    2: QColor("green"),
    3: QColor("red"),
    4: QColor("darkBlue"),
    5: QColor("darkRed"),
    6: QColor("darkCyan"),
    7: QColor("black"),
    8: QColor("darkGray")
}

class tile(QWidget):
    clicked = pyqtSignal()
    mine_click = pyqtSignal()
    flagged = pyqtSignal(int)
    expand = pyqtSignal(int, int)

    is_revealed = False
    is_start = False
    is_mine = False
    is_flagged = False
    game_over = False
    adjacent = 0

    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y
        
    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)

        r = event.rect()

        inner_colour = None
        border_colour = QColor("gray")
        if self.is_revealed:
            inner_colour = QColor("lightGray")
        else:
            inner_colour = QColor("darkGray")
              
        p.fillRect(r, inner_colour)
        pen = QPen(border_colour)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_flagged:
            p.fillRect(r, border_colour)
            if not self.is_mine and self.game_over:
                pen = QPen(QColor("red"))
                p.setPen(pen)
                p.drawText(r, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, "X")
        elif self.game_over and self.is_mine:
            p.fillRect(r, QColor("black"))

        if self.is_revealed:
            if self.is_start:
                p.fillRect(r, QColor("green"))
            elif self.is_mine:
                p.fillRect(r, QColor("red"))
            elif self.adjacent > 0:
                pen = QPen(COLOUR_NUM[self.adjacent])
                p.setPen(pen)
                p.drawText(r, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, str(self.adjacent))
        
        p.end()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.flag()
        
        elif event.button() == Qt.MouseButton.LeftButton:
            self.reveal()

    def flag(self):
        if self.game_over: return

        if self.is_flagged:
            self.is_flagged = False
            self.flagged.emit(1)
            self.update()

        elif not self.is_revealed :
            self.is_flagged = True
            self.flagged.emit(-1)
            self.update()

    def reveal(self):
        if self.is_flagged or self.is_revealed or self.game_over: return
        
        self.is_revealed = True
        if self.is_mine:
            self.mine_click.emit()
        elif self.adjacent == 0:
            self.expand.emit(self.x, self.y)
        self.update()


class MainWindow(QMainWindow):
    hb = None
    grid = None
    x = DIFFICULTIES[1]["x"]
    y = DIFFICULTIES[1]["y"]
    total_mines = DIFFICULTIES[1]["mines"]
    mines = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        
        toolbar = QToolBar("Minesweeper Toolbar")
        toolbar.addWidget(QLabel("New Game"))
        toolbar.addSeparator()
        mode = QAction("Easy", self)
        mode.triggered.connect(self.start_easy)
        toolbar.addAction(mode)
        mode = QAction("Normal", self)
        mode.triggered.connect(self.start_normal)
        toolbar.addAction(mode)
        mode = QAction("Expert", self)
        mode.triggered.connect(self.start_expert)
        toolbar.addAction(mode)

        self.addToolBar(toolbar)

        self.startGame()
    
    def create_header(self):
        self.hb = QHBoxLayout()

        f = QFont()
        f.setPointSize(24)
        f.setWeight(75)

        self.mines_label = QLabel()
        self.mines_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.mines_label.setFont(f)
        self.mines_label.setNum(self.total_mines)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("000")

        #                           TODO make and connect timer function
        self._timer = QTimer()

        #                           TODO MAKE BUTTON IMAGE
        self.restart_button = QPushButton("R")
        self.restart_button.setFixedSize(QSize(32, 32))
        self.restart_button.setIconSize(QSize(32, 32))
        #self.restart_button.setIcon(QIcon("./images/bomb.png"))
        self.restart_button.setFlat(True)
        self.restart_button.released.connect(self.restart)

        #                           TODO MAKE MINE IMAGE
        mineIcon = QLabel("M")
        mineIcon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        #mineIcon.setPixmap(QPixmap.fromImage(QImage("./images/bomb.png")))

        #                           TODO MAKE CLOCK IMAGE
        clockIcon = QLabel("T")
        clockIcon.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.hb.addWidget(mineIcon)
        self.hb.addWidget(self.mines_label)
        self.hb.addWidget(self.restart_button)
        self.hb.addWidget(self.clock)
        self.hb.addWidget(clockIcon)

    def create_field(self, x, y, m):
        self.x = x
        self.y = y
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        for i in range(0, x):
            for j in range(0, y):
                w = tile(i, j)
                w.flagged.connect(self.tile_flagged)
                w.expand.connect(self.reveal_adjacent)
                w.mine_click.connect(self.gameOver)
                self.grid.addWidget(w, j, i)
        
        self.create_new_mines(m)

    def create_new_mines(self, m):
        self.mines = 0
        while self.mines < m:
            rand_x = randrange(0, self.x)
            rand_y = randrange(0, self.y)
            w = self.grid.itemAtPosition(rand_y, rand_x).widget()
            
            if not w.is_mine:
                w.is_mine = True

                self.mines += 1

        self.find_adjacent_bombs()

    def find_adjacent_bombs(self):
        for i in range(self.y):
            for j in range(self.x):
                w = self.grid.itemAtPosition(i, j).widget()

                if not w.is_mine:
                    count = 0
                    if i != 0:
                        if self.grid.itemAtPosition(i-1, j).widget().is_mine: count += 1
                        if j != 0:
                            if self.grid.itemAtPosition(i-1, j-1).widget().is_mine: count += 1
                        if j+1 != self.x:
                            if self.grid.itemAtPosition(i-1, j+1).widget().is_mine: count += 1
                    if j != 0:
                        if self.grid.itemAtPosition(i, j-1).widget().is_mine: count += 1
                    if j+1 != self.x:
                        if self.grid.itemAtPosition(i, j+1).widget().is_mine: count +=1
                    if i+1 != self.y:
                        if self.grid.itemAtPosition(i+1, j).widget().is_mine: count += 1
                        if j != 0:
                            if self.grid.itemAtPosition(i+1, j-1).widget().is_mine: count += 1
                        if j+1 != self.x:
                            if self.grid.itemAtPosition(i+1, j+1).widget().is_mine: count += 1
                    w.adjacent = count

    def reveal_adjacent(self, x, y):
        for i in range(max(0, y - 1), min(y+2, self.y)):
            for j in range(max(0, x - 1), min(x+2, self.x)):
                self.grid.itemAtPosition(i, j).widget().reveal()

    def tile_flagged(self, i):
        self.mines += i

        self.mines_label.setNum(self.mines)

    def restart(self):
        self.create_field(self.x, self.y, self.total_mines)
        self.create_header()

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)
        
        w = QWidget()
        w.setLayout(vb)
        self.setCentralWidget(w)

        while True:
            i = randrange(self.y)
            j = randrange(self.x)
            w = self.grid.itemAtPosition(i, j).widget()
            if not w.is_mine and w.adjacent == 0:
                w.is_start = True
                w.reveal()
                break

    def start_easy(self):
        self.x = DIFFICULTIES[0]["x"]
        self.y = DIFFICULTIES[0]["y"]
        self.total_mines = DIFFICULTIES[0]["mines"]
        self.startGame()

    def start_normal(self):
        self.x = DIFFICULTIES[1]["x"]
        self.y = DIFFICULTIES[1]["y"]
        self.total_mines = DIFFICULTIES[1]["mines"]
        self.startGame()

    def start_expert(self):
        self.x = DIFFICULTIES[2]["x"]
        self.y = DIFFICULTIES[2]["y"]
        self.total_mines = DIFFICULTIES[2]["mines"]
        self.startGame()
    
    def startGame(self):
        self.create_header()
        self.create_field(self.x, self.y, self.total_mines)

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)
        
        w = QWidget()
        w.setLayout(vb)
        self.setCentralWidget(w)
        self.adjustSize()
        
        while True:
            i = randrange(self.y)
            j = randrange(self.x)
            w = self.grid.itemAtPosition(i, j).widget()
            if not w.is_mine and w.adjacent == 0:
                w.is_start = True
                w.reveal()
                break

    def gameOver(self):
        for i in range(self.y):
            for j in range(self.x):
                w = self.grid.itemAtPosition(i, j).widget()
                w.game_over = True
                w.update()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
