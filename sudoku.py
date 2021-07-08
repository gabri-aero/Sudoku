import numpy as np

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

def printSudoku(sudoku): #board design in console
    result=sudoku.tolist()
    for i in range(len(result)):
        result[i].insert(9,'|')
        result[i].insert(6,'|')
        result[i].insert(3,'|')
        result[i].insert(0,'|')
    result.insert(6,['-' for i in range(len(result[0]))])
    result.insert(3,['-' for i in range(len(result[0]))])
    for item in result:
        for jtem in item:
            print(jtem, end=' ')
        print('\n', end='')

board=np.array(board) #enabling numpy functionalities in the board matrix

def check(num,posX,posY, sudoku):
    if(num in sudoku[posX]): return False #row
    elif(num in sudoku[:,posY]): return False #column
    elif(num in sudoku[3*(posX//3):3*(posX//3)+3, 3*(posY//3):3*(posY//3)+3]): return False #submatrix 3x3
    else: return True

def solve(sudoku):
    i=j=0
    while i<len(sudoku):
        while j<len(sudoku):
            if memory[i][j]:
                i, j= writeNum(i,j,sudoku) #resetting indexes
            j+=1
        i+=1
        j=0
    print('\nSolution: ')
    printSudoku(sudoku)
    pass

def writeNum(i,j,sudoku):
    num=sudoku[i][j]
    while(num<9):
        num+=1
        if check(num, i, j, sudoku):
            sudoku[i][j]=num #writing num in pos i,j
            return i,j
    #backtrack detected
    sudoku[i][j]=0
    while(num==9):
        j-=1
        if j<0:
            j=8
            i-=1
        if memory[i][j]:
            return i, j-1 #backtracking to position i,j

print('Board to solve: ')
printSudoku(board)
solve(board)