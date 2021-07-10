import pygame
import time
pygame.font.init()

class Grid:

    board = [
        [0,4,0,9,0,0,6,0,1],
        [7,8,0,0,0,0,0,3,0],
        [1,0,5,0,0,4,9,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,9,0,5,4,0,2,0,6],
        [0,0,0,0,0,1,0,0,7],
        [0,7,0,0,8,9,1,0,0],
        [0,0,0,1,2,0,0,0,4],
        [8,0,0,0,0,0,0,9,0]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width 
        self.height = height
        self.cubes = [[Cube(self.board[row][col], row, col, self.width, self.height) for col in range(self.cols)] for row in range(self.rows)]

    def draw(self, win):
        gap = self.width / self.rows
        for i in range(0, self.rows+1):
            if i % 3 == 0: 
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0,0,0), (0, gap*i), (self.width, gap*i), thickness)
            pygame.draw.line(win, (0,0,0), (gap*i, 0), (gap*i, self.height), thickness)
        
        for i in range(self.cols):
            for j in range(self.rows):
                self.cubes[i][j].draw(win)

    def changeVal(self, row, col, win):
        self.cubes[row][col].value +=1
        if self.cubes[row][col].value == 10: self.cubes[row][col].value = 0
        self.update(win)

    def update(self, win):
        win.fill((255, 255, 255))
        self.draw(win)

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width 
        self.height = height

    def draw(self, win):
        fnt = pygame.font.SysFont('comicsans', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value:
            text = fnt.render(str(self.value), 1, (0,0,0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption('Sudoku')
    win.fill((255, 255, 255))
    board = Grid(9, 9, 540, 540)
    board.draw(win)
    run=True
    start = time.time()
    key = 1
    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // 60
                col = pos[0] // 60
                board.changeVal(row, col, win)
                print(row, col)

        pygame.display.update()

main()