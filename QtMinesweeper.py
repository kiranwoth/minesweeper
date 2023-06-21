from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, 
    QGridLayout, QToolBar)

class tile(QWidget):
    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y


class MainWindow(QMainWindow):
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

        self.hb = None
        self.create_header()

        #                           TODO make field with the correct things
        self.grid = None
        self.init_field(12, 12)

        vb = QVBoxLayout()
        vb.addLayout(self.hb)
        vb.addLayout(self.grid)

        w.setLayout(vb)
        self.setCentralWidget(w)
    
    def create_header(self):
        self.hb = QHBoxLayout()

        f = QLabel().font()
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
        self.button = QPushButton("R")
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setFlat(True)
        #connect button.pressed to self.button_pressed or something
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

    def init_field(self, x, y):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        for i in range(0, x):
            for j in range(0, y):
                w = QPushButton(f"{i},{j}")
                w.setFixedSize(QSize(40, 40))
                self.grid.addWidget(w, j, i)

    def open_menu(self):
        self.create_header()
        self.init_field(5, 5)

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
