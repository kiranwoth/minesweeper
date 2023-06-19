class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    revealed: bool = False
    isMine: bool = False
    surrounding: int = 0

