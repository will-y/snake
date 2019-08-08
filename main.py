import pygame as pg
import sys

class Main():
    def __init__(self):
        #The size of the individual grid squares
        self.gridSize = 50
        #The number of squares on the game board
        self.gridCount = 10
        #size of the screen
        self.size = width, height = self.gridSize * self.gridCount, self.gridSize * self.gridCount
        #pygame screen
        self.screen = pg.display.set_mode(self.size)
        #creates the game grid
        self.grid = self.createGrid(self.gridCount)
        #0: up
        #1: right
        #2: down
        #3 left
        self.direction = 1
        #Current position of the head of the snake
        self.position = x, y = 1, 1
        #Is the game active?
        self.active = True
        #Stores all of the positions of the snake
        self.snake = [(1, 1)]
        #Clock for controlling fps
        self.clock = pg.time.Clock()
        #FPS min 1 max 1000 (default 4)
        self.fps = 4

    def runGame(self):
        """
        Runs the game with an infinte while loop
        """
        while 1:
            # If exited, don't crash
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    sys.exit()

            #get the current keys pressed
            self.key = pg.key.get_pressed()
            
            #game tick
            self.gameTick()
            #draw things for the game
            self.screen.fill((110, 110, 110))
            self.drawGrid(self.gridSize, self.gridCount)

            #update the screen
            pg.display.flip()

            #Game Clock
            self.clock.tick(self.fps)
    
    def createGrid(self, gridCount):
        """
        Creates the game grid with walls on the outside
        0 = Empty
        1 = Wall
        2, 3 = Player
        4 = Dot
        """
        grid = []
        for x in range(gridCount):
            row = []
            for y in range(gridCount):
                if x == 0 or y == 0 or x == gridCount - 1 or y == gridCount - 1:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        
        grid[1][1] = 2
        
        return grid
    
    def drawGrid(self, gridSize, gridCount):
        """
        Draws the grid on the screen
        """
        for x in range(0, gridCount):
            for y in range(0, gridCount):
                if self.grid[x][y] == 1:
                    pg.draw.rect(self.screen, (0, 0, 0), (gridSize * x, gridSize * y, gridSize, gridSize), 0)
                    pg.draw.rect(self.screen, (61, 61, 61), (gridSize * x, gridSize * y, gridSize, gridSize), 1)
                elif self.grid[x][y] == 2:
                    pg.draw.rect(self.screen, (35, 196, 14), (gridSize * x, gridSize * y, gridSize, gridSize), 0)
                else:
                    pg.draw.rect(self.screen, (143, 143, 143), (gridSize * x, gridSize * y, gridSize, gridSize), 1)
        
        

    def gameTick(self):
        """
        One tick of the game
        Controlls all motion of the game
        Can be sped up or slowed down depending on the clock
        """
        positionToCheck = (0, 0)

        if(self.direction == 0):
            positionToCheck = self.position[0], self.position[1] - 1
        elif(self.direction == 1):
            positionToCheck = self.position[0] + 1, self.position[1]
        elif(self.direction == 2):
            positionToCheck = self.position[0], self.position[1] + 1
        elif(self.direction == 3):
            positionToCheck = self.position[0] - 1, self.position[1]
        
        positionValue = self.grid[positionToCheck[0]][positionToCheck[1]]

        if(positionValue == 0):
            #valid space, move
            self.move(False, positionToCheck)
        elif positionValue == 1 or positionValue == 2 or positionValue == 3:
            #Hit yourself or a wall, lose
            self.endGame(False)
        elif positionValue == 4:
            #Collect dot thing, grow and move into the place
            self.move(True, positionToCheck)

    def move(self, grow, position):
        """
        Moves the snake based on the direction
        """
        self.snake.append(position)
        self.position = position
        if not grow:
            self.removeTail()

        self.grid[position[0]][position[1]] = 2

    def removeTail(self):
        """
        Remove the last block from the snake when it doesn't grow
        """
        #Get the tail
        positionToRemove = self.snake[0]
        #Remove it from the grid
        self.grid[positionToRemove[0]][positionToRemove[1]] = 0
        #Remove it from the array
        self.snake.__delitem__(0)
        print(self.snake)
        print(self.grid)


    def endGame(self, win):
        """
        Ends the game
        Pass in a boolean to know if you won or lost
        """
        self.active = False

def main():
    pg.init()
    main = Main()
    main.runGame()

main()