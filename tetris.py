from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block
    
    # 클래스와 같은 이름에 . 찍고 변수명을 쓴다면 그것을 클래스 변수라고 한다
    # Tetris 클래스를 이용해서 여러 객체가 생성될 수 있는데
    # 그 객체들이 모두 공유하는 공유변수가 된다.
    @classmethod
    def init(cls, setOfBlockArrays): # 최초에 단 한번만 호출되어야한다.
        Tetris.nBlockTypes = len(setOfBlockArrays) # 7
        Tetris.nBlockDegrees = len(setOfBlockArrays[0]) # 4
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j]) # 4차원 배열
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
	
    # 생성자
    def __init__(self, iScreenDy, iScreenDx): # 32, 16
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        self.top = 0
        self.left = Tetris.iScreenDw + self.iScreenDx//2 -2
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        self.arrayBlk = 0
        self.currBlk = 0
        self.tempBlk = 0
        self.blkType = 0
        return

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self): # To be implemented!!
        delLine = True
        delArray = self.iScreen.get_array()
        newLine = []

        for i in range(self.iScreenDw):
            newLine.append(1)
        for i in range(self.iScreenDx):
            newLine.append(0)
        for i in range(self.iScreenDw):
            newLine.append(1)
        
        for y in reversed(range(self.iScreenDy)):
            for x in range(self.iScreenDx):
                if delArray[y][Tetris.iScreenDw + x] == 1:
                    delLine = True
                else:
                    delLine = False
                    break

            if delLine == True:
                print("del line: ",y)
                del delArray[y]
                delArray.insert(0,newLine)

        self.iScreen = Matrix(delArray)


    # 지금 블록의 현재 위치를 알 수 있는 정보 (top, left가 필요함)
    # 근데 matrix.py를 수정할 수는 없으니.. 여기서 현재 주인공인(?) 블록을 저장해야함
    def accept(self, key): # To be implemented!!
        self.state = TetrisState.Running
        self.deleteFullLines()

        if key[0] =='0': # 새로운 블록이 필요함
            self.blkType = int(key[1])
            print("블록 타입: ", key[1])

            self.idxBlockDegree = 0
            self.arrayBlk = Tetris.setOfBlockObjects[self.blkType][self.idxBlockDegree]
            self.currBlk = Matrix(self.arrayBlk)
            self.left = Tetris.iScreenDw + self.iScreenDx//2 -2
            self.top = 0
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk

            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)
            
            return self.state

        print("입력된 키: ", key)
        if key == 'a':  # move left
            self.left -= 1
        elif key == 'd':  # move right
            self.left += 1
        elif key == 's':  # move down
            self.top += 1
        elif key == 'w':  # rotate the block clockwise
            self.idxBlockDegree = (self.idxBlockDegree+1) % 4
            self.arrayBlk = Tetris.setOfBlockObjects[self.blkType][self.idxBlockDegree]
            self.currBlk = Matrix(self.arrayBlk)
        elif key == ' ':  # drop the block
            while(True):
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                self.tempBlk = self.tempBlk + self.currBlk

                if self.tempBlk.anyGreaterThan(1):
                    break
        else:
            print('Wrong key!!!')

        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):
            if key == 'a':  # undo: move right
                self.left += 1
            elif key == 'd':  # undo: move left
                self.left -= 1
            elif key == 's':  # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w':  # undo: rotate the block counter-clockwise
                self.idxBlockDegree = (self.idxBlockDegree+3) % 4
                self.arrayBlk = Tetris.setOfBlockObjects[self.blkType][self.idxBlockDegree]
                self.currBlk = Matrix(self.arrayBlk)
            elif key == ' ':  # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock

        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)

        if self.state == TetrisState.NewBlock:
            self.iScreen = Matrix(self.oScreen)
        
        return self.state

### end of class Tetris():
    
