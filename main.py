from random import randrange

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    revealed: bool = False
    isMine: bool = False
    isFlag: bool = False
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
                if cell.isMine: out += " M "
                elif cell.revealed: out += "R{} ".format(cell.surrounding)
                else: out += " {} ".format(cell.surrounding)
            out += "\n"
        return out
    
    uncoveredCells: int = 0
    active: bool = True

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

def uncoverCell(x, y, field, board):
    #uncovers cell xy in field
    if field[y][x].revealed: return 0

    if field[y][x].isMine: 
        loseGame(board)
    elif field[y][x].surrounding == 0:
        #call this function on surrounding cells
        pass
    field[y][x].revealed = True
    return 1

def flagCell(x, y, board):
    #flags cell xy in field
    pass

def winGame(board):
    board.active = False
    print(board)
    print("You won!")

def loseGame(board):
    board.active = False
    print("You Lost! haha")

def main():
    rows = 5
    cols = 5
    mines = 5
    board = MineField(cols, rows, mines)

    while board.active:
        print(board)
        selection = input("Click a square: ")
        x = int(selection[0])
        y = int(selection[2])

        board.uncoveredCells += uncoverCell(x, y, board.field, board)
        if board.uncoveredCells >= (cols * rows) - mines: winGame(board)

main()