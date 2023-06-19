from random import randrange

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    revealed: bool = False
    isMine: bool = False
    surrounding: int = 0

class MineField():
    def __init__(self, x, y, mines):
        self.field = createField(x, y)
        placeMines(x, y, mines, self.field)
        countSurrounding(x, y, self.field)
    def __str__(self) -> str:
        out = ""
        for row in self.field:
            for cell in row:
                if cell.isMine: out += "M "
                else: out += "{} ".format(cell.surrounding)
            out += "\n"
        return out
    uncoveredCells: int = 0

def createField(x, y):
    #creates field of size xy
    field = []
    for i in range(y):
        field.append(createRow(x, i))
    return field
def createRow(x, y):
    row = []
    for i in range(x):
        row.append(Cell(i, y))
    return row

def placeMines(x, y, mines, field):
    #places m mines into field
    while mines > 0:
        i = randrange(x)
        j = randrange(y)
        if field[i][j].isMine:
            continue
        field[i][j].isMine = True
        mines -= 1
    return
def countSurrounding(x, y, field):
    #calculates the number of mines around each square in field
    for i in range(y):
        for j in range(x):
            if field[i][j].isMine:
                continue
            
            count = 0
            if i != 0:
                if field[i-1][j].isMine: count += 1
                if j != 0:
                    if field[i-1][j-1].isMine: count += 1
                if j+1 != x:
                    if field[i-1][j+1].isMine: count += 1
            if j != 0:
                if field[i][j-1].isMine: count += 1
            if j+1 != x:
                if field[i][j+1].isMine: count +=1
            if i+1 != y:
                if field[i+1][j].isMine: count += 1
                if j != 0:
                    if field[i+1][j-1].isMine: count += 1
                if j+1 != x:
                    if field[i+1][j+1].isMine: count += 1
            field[i][j].surrounding = count
    return