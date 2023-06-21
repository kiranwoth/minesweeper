from PyQt6.QtGui import (
    QAction, QFont, QPainter, QColor, QImage, QPixmap, QIcon, QPen
    )
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, 
    QGridLayout, QToolBar
    )
from random import randrange

#TODO
#colour global variables
#       in dict probably
#TODO
#image global variables
#       in dict probably

DEFAULT_LEVEL = {
    "x": 9,
    "y": 9,
    "mines": 10
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
    bomb_click = pyqtSignal()
    flagged = pyqtSignal(int)

    is_revealed = False
    is_start = False
    is_mine = False
    is_flagged = False
    adjacent = 0

    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(40, 40))
        self.x = x
        self.y = y
        
    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)

        r = event.rect()
    #                               TODO need some way to draw unrevealed bombs on game end
    #                                   might need to change way to draw the clicked bomb
    #                               TODO need way to draw wrongly flagged tiles on game end

    #                               TODO make this pseudo code actual code
        #if revealed set both inner/outer colour to background
        #else set inner/outer to tile colours
        inner_colour = None
        border_colour = QColor("gray")
        if self.is_revealed:
            inner_colour = QColor("lightGray")
        else:
            inner_colour = QColor("darkGray")
        
        #fill r with inner colour
        #draw rect around r with outer       
        p.fillRect(r, inner_colour)
        pen = QPen(border_colour)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.fillRect(r, QColor("green"))
            elif self.is_mine:
                p.fillRect(r, QColor("yellow"))
            elif self.adjacent > 0:
                pen = QPen(COLOUR_NUM[self.adjacent])
                p.setPen(pen)
                p.drawText(r, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, str(self.adjacent))

        #if flagged draw flag
        if self.is_flagged:
            p.fillRect(r, border_colour)
        
        p.end()
    
    #                               TODO func
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.flag()
        
        elif event.button() == Qt.MouseButton.LeftButton:
            self.click()

    #                               TODO func
    def click(self):
        self.reveal()
        self.clicked.emit()

    #                               TODO way to change mine remaining number when tile is flagged
    def flag(self):
        if self.is_flagged:
            self.is_flagged = False
            self.flagged.emit(1)
            self.update()

        elif not self.is_revealed:
            self.is_flagged = True
            self.flagged.emit(-1)
            self.update()
        

    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            self.update()



class MainWindow(QMainWindow):
    hb = None
    grid = None
    x = DEFAULT_LEVEL["x"]
    y = DEFAULT_LEVEL["y"]
    total_mines = DEFAULT_LEVEL["mines"]
    mines = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        w = QWidget()

        #                           TODO make MENU button bring up dialog
        #                           TODO make dialog choose difficulty
        #                                   easy, normal, expert, custom
        #                           TODO make this dialog popup on window start
        toolbar = QToolBar("Minesweeper Toolbar")

        menu_button = QAction("Menu", self)
        menu_button.triggered.connect(self.open_menu)

        toolbar.addAction(menu_button)
        self.addToolBar(toolbar)


        self.create_header()
        self.create_field(self.x, self.y, self.total_mines)

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)

        w.setLayout(vb)
        self.setCentralWidget(w)
    
    def create_header(self):
        self.hb = QHBoxLayout()

        f = QFont()
        f.setPointSize(24)
        f.setWeight(75)

        self.mines_label = QLabel()
        self.mines_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.mines_label.setFont(f)
        self.mines_label.setNum(self.mines)

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
                self.grid.addWidget(w, j, i)
        
        self.create_new_mines(x, y, m)

    def create_new_mines(self, x, y, m):
        self.mines = 0
        while self.mines < m:
            rand_x = randrange(0, x)
            rand_y = randrange(0, y)
            w = self.grid.itemAtPosition(rand_y, rand_x).widget()
            
            if not w.is_mine:
                w.is_mine = True

                self.mines += 1
        
        self.mines_label.setNum(self.mines)
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


    def tile_flagged(self, i):
        self.mines += i

        self.mines_label.setNum(self.mines)

    def restart(self):
        self.create_field(self.x, self.y, 10)
        self.create_header()

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)
        
        w = QWidget()
        w.setLayout(vb)
        self.setCentralWidget(w)

    def open_menu(self):
        self.create_header()
        self.create_field(5, 5)

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)
        
        w = QWidget()
        w.setLayout(vb)
        self.setCentralWidget(w)
        self.adjustSize()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
