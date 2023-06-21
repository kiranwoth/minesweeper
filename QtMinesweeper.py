from PyQt6.QtGui import QAction, QFont, QPainter, QColor
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, 
    QGridLayout, QToolBar)

class tile(QWidget):
    clicked = pyqtSignal()
    bomb_click = pyqtSignal()

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
        
    #                               TODO func
    def paintEvent(self, event):
        p = QPainter()
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()
    #                               TODO need some way to draw unrevealed bombs on game end
    #                                   might need to change way to draw the clicked bomb
    #                               TODO need way to draw wrongly flagged tiles on game end

        #if revealed set both inner/outer colour to background
        #else set inner/outer to tile colours

        #fill r with inner colour
        #draw rect around r with outer

        #if revealed
        #   if start draw start square
        #   elif mine draw revealed mine (red background)
        #   elif adjacent to at least one mine
        #       draw the number of adjacent using colour based on how many adjacent

        #if flagged draw flag
    
    #                               TODO func
    def mouseReleaseEvent(self, event):
        pass

    #                               TODO func
    def click(self):
        self.clicked.emit()

    def flag(self):
        self.is_flagged = True
        self.update()

    def reveal(self):
        self.is_revealed = True
        self.update()



class MainWindow(QMainWindow):
    hb = None
    grid = None
    x = None
    y = None

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
        #                           TODO make field with the correct things
        self.create_field(12, 12)

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

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.mines.setFont(f)
        self.mines.setText("99")

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.clock.setFont(f)
        self.clock.setText("000")

        self._timer = QTimer()
        #                           TODO make and connect timer function
        self.restart_button = QPushButton("R")
        self.restart_button.setFixedSize(QSize(32, 32))
        self.restart_button.setIconSize(QSize(32, 32))
        self.restart_button.setFlat(True)
        self.restart_button.released.connect(self.restart)
        #                           TODO MAKE BUTTON IMAGE
        #                           TODO MAKE BUTTON FUNCTION

        #                           TODO MAKE MINE IMAGE
        mineIcon = QLabel("M")
        mineIcon.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        #                           TODO MAKE CLOCK IMAGE
        clockIcon = QLabel("T")
        clockIcon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.hb.addWidget(mineIcon)
        self.hb.addWidget(self.mines)
        self.hb.addWidget(self.button)
        self.hb.addWidget(self.clock)
        self.hb.addWidget(clockIcon)

    def create_field(self, x, y):
        self.x = x
        self.y = y
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        for i in range(0, x):
            for j in range(0, y):
                w = QPushButton(f"{i},{j}")
                w.setFixedSize(QSize(40, 40))
                self.grid.addWidget(w, j, i)

    def restart(self):
        self.create_header()
        self.create_field(self.x, self.y)

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
