import pygame
import time
pygame.font.init()
from sudoku_solver import solve

class Board:

    start = time.time()

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

    memory=list(map(lambda x: list(map(lambda y: True if y==0 else False,x)), board))

    solution = solve(board)

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width 
        self.height = height
        self.cubes = [[Cube(self.board[row][col], row, col, self.width, self.height) for col in range(self.cols)] for row in range(self.rows)]
        self.strikeCounter = StrikeCounter(550,400)
        self.timer = Timer(10, 550, time.time())

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

        for i in range(self.cols):
            for j in range(self.rows):
                self.cubes[i][j].displayFrame(win)

    def click(self, row, col, win):
        self.update(win)
        if row<9 and col<9:
            if self.memory[row][col]: 
                self.cubes[row][col].status = 'SELECTED'
                return True
        return False

    def update(self, win):
        win.fill((255, 255, 255))
        self.timer.update(win)
        self.strikeCounter.draw(win)
        self.draw(win)

    def check(self, row, col, win):
        if self.cubes[row][col].tempValue == self.solution[row][col]:
            self.cubes[row][col].value = self.cubes[row][col].tempValue
            self.cubes[row][col].tempValue = 0
            self.memory[row][col] = False
            self.cubes[row][col].status = 'CORRECT'
            return True
        else:
            self.cubes[row][col].incorrect(win)
            self.strikeCounter.add()
            self.cubes[row][col].status = 'INCORRECT'
            return False

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width 
        self.height = height
        self.tempValue = 0
        self.status = None

    def draw(self, win):
        fnt = pygame.font.SysFont('comicsans', 40)
        fnt2 = pygame.font.SysFont('comicsans', 25)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value:
            text = fnt.render(str(self.value), 1, (0,0,0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.tempValue:
            text = fnt2.render(str(self.tempValue), 1, (100,100,100))
            win.blit(text, (x + text.get_width()/2, y + text.get_height()/2))

    def displayFrame(self, win):
        if self.status == 'SELECTED': self.select(win)
        if self.status == 'CORRECT': self.correct(win)
        if self.status == 'INCORRECT': self.incorrect(win)
        if self.status == None: self.hideFrame()

    def frame(self, win, color):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, color, pygame.Rect(x, y, gap, gap), 4)

    def select(self, win):
        self.frame(win, (0, 0, 255))

    def correct(self, win):
        self.frame(win, (0, 255, 0))
        pygame.display.update()
        pygame.time.delay(1000)
        self.status = None

    def incorrect(self, win):
        self.frame(win, (255, 0, 0))
        pygame.display.update()
        pygame.time.delay(250)
        self.status = 'SELECTED'

    def hideFrame(self):
        pass

class Timer:
    def __init__(self, x, y, start):
        self.x = x 
        self.y = y
        self.start = start
        self.secs = 0

    def update(self, win):
        self.secs = round(time.time() - self.start)
        fnt3 = pygame.font.SysFont('timesnewroman', 20)
        text = fnt3.render(self.design(), 1, (0, 0, 0))
        win.blit(text, (self.x, self.y))

    def design(self):
        self.mins = self.secs // 60
        self.secs = self.secs % 60
        if self.secs<10:
            self.secs = "0{0}".format(self.secs)
        else:
            self.secs = str(self.secs)
        if self.mins<10:
            self.mins = "0{0}".format(self.mins)
        else:
            self.mins = str(self.mins)
        return self.mins+':'+self.secs

class StrikeCounter:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.strikes = 0

    def draw(self, win):
        fnt3 = pygame.font.SysFont('timesnewroman', 20)
        fnt4 = pygame.font.SysFont('comicsans', 30)
        text1 = fnt3.render(str(self.strikes), 1, (0, 0, 0))
        text2 = fnt4.render('X', 4, (255, 0, 0))
        win.blit(text1, (400, 547))
        win.blit(text2, (400 + text1.get_width(), 550))

    def add(self):
        self.strikes += 1

def loadingScreen(win, width, height):
    fnt = pygame.font.SysFont('comicsans', 150)  
    fnt2 = pygame.font.SysFont('comicsans', 20)  
    text = fnt.render('SUDOKU', 1, (0, 0, 0))
    text2 = fnt2.render('Loading...', 1, (0, 0, 0))
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    win.blit(text2, (width/2 - text2.get_width()/2, height/2 + text.get_height()/2))
    pygame.draw.rect(win, (0, 0, 0), pygame.Rect(width/2 - text.get_width()/2-10, height/2 - text.get_height()/2-10, text.get_width()+20, 20+text.get_height()+text2.get_height()), 4)
    pygame.display.update()
    pygame.time.delay(2500)


def main():
    width = 540
    height = 600

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Sudoku')
    win.fill((255, 255, 255))
    loadingScreen(win, width, height)
    board = Board(9, 9, width, width)

    run = True
    selected = correct = False
    key = clock = row = col = 0

    while run:
        if clock != round(time.time(), 1):
            clock = round(time.time(), 1)
            if selected:
                selected = board.click(row, col, win)
            else:
                board.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.cubes[row][col].status = None
                pos = pygame.mouse.get_pos()
                row = pos[1] // 60
                col = pos[0] // 60
                selected = board.click(row, col, win)
            if selected:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        correct = board.check(row, col, win)
                        board.update(win)                     
                    else:
                        if event.key == pygame.K_1: key = 1
                        if event.key == pygame.K_2: key = 2
                        if event.key == pygame.K_3: key = 3
                        if event.key == pygame.K_4: key = 4
                        if event.key == pygame.K_5: key = 5
                        if event.key == pygame.K_6: key = 6
                        if event.key == pygame.K_7: key = 7
                        if event.key == pygame.K_8: key = 8
                        if event.key == pygame.K_9: key = 9
                        if event.key == pygame.K_BACKSPACE: key = 0
                        board.cubes[row][col].tempValue = key
                        selected = board.click(row, col, win)

        pygame.display.update()

main()