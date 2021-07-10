import numpy as np

def printSudoku(sudoku): #board design in console
    result=sudoku
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

def check(num, posX, posY, sudoku):
    sudoku=np.array(sudoku) #enabling numpy functionalities in the matrix
    if(num in sudoku[posX]): return False #row
    elif(num in sudoku[:, posY]): return False #column
    elif(num in sudoku[3*(posX//3):3*(posX//3)+3, 3*(posY//3):3*(posY//3)+3]): return False #submatrix 3x3
    else: return True

def solve(board):
    sudoku = list(map(lambda x: list(map(lambda y: y, x)), board)) #avoiding array mutability
    memory=list(map(lambda x: list(map(lambda y: True if y==0 else False,x)), sudoku))
    i=j=0
    while i<len(sudoku):
        while j<len(sudoku):
            if memory[i][j]:
                i, j= writeNum(i,j,sudoku, memory) #resetting indexes
            j+=1
        i+=1
        j=0
    return sudoku

def writeNum(i, j, sudoku, memory):
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