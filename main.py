import schemas

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
    print(board)
    board.active = False
    print("You won!")

def loseGame(board):
    print(board)
    board.active = False
    print("You Lost! haha")

def main():
    rows = 5
    cols = 5
    mines = 5
    board = schemas.MineField(cols, rows, mines)

    while board.active:
        print(board)
        selection = input("Click a square: ")
        x = int(selection[0])
        y = int(selection[2])

        board.uncoveredCells += uncoverCell(x, y, board.field, board)
        if board.uncoveredCells >= (cols * rows) - mines: winGame(board)

main()