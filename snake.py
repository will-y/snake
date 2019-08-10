import pygame as pg
import sys
import random

class Main():
    def __init__(self, showGraphics):
        # Used to show graphics or not
        self.showGraphics = showGraphics
        # The size of the individual grid squares
        self.gridSize = 50
        # The number of squares on the game board
        self.gridCount = 10
        # size of the screen
        self.size = self.gridSize * self.gridCount, self.gridSize * self.gridCount
        # pygame screen
        if self.showGraphics:
            self.screen = pg.display.set_mode(self.size)
        # creates the game grid
        self.grid = self.createGrid(self.gridCount)
        # 0: up
        # 1: right
        # 2: down
        # 3 left
        self.direction = 1
        # Current position of the head of the snake
        self.position = x, y = 1, 1
        # Is the game active?
        self.active = True
        # Stores all of the positions of the snake
        self.snake = [(1, 1)]
        # Clock for controlling fps
        self.clock = pg.time.Clock()
        # FPS min 1 max 1000 (default 10)
        self.fps = 10
        # If there is food on the screen
        self.foodSpawned = False
        # Spawn the first food
        self.spawnFood(self.gridCount)
        # Score
        self.score = 0

        self.opposites = {
            0 : 2,
            1 : 3,
            2 : 0,
            3 : 1
        }

    def runGame(self):
        """
        Runs the game with an infinte while loop
        Shouldn't be called frmo the machine learning unless it is showing graphics
        """
        while self.active:
            # If exited, don't crash
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    sys.exit()
            
            # game tick
            self.gameTick()

            # draw things for the game
            self.updateScreen()
            
            # Game Clock
            self.clock.tick(self.fps)

        print("Final Score: {}".format(self.score))

    def updateScreen(self):
        if self.showGraphics:
            self.screen.fill((110, 110, 110))
            self.drawGrid(self.gridSize, self.gridCount)

            # update the screen
            pg.display.flip()
    
    def createGrid(self, gridCount):
        """
        Creates the game grid with walls on the outside
        0 = Empty
        1 = Wall
        2 = Player
        3 = Dot
        """
        grid = []
        # Set the game grid with walls on the edges
        for x in range(gridCount):
            row = []
            for y in range(gridCount):
                if x == 0 or y == 0 or x == gridCount - 1 or y == gridCount - 1:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        
        # Set the player
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
                elif self.grid[x][y] == 3:
                    pg.draw.rect(self.screen, (226, 242, 0), (gridSize * x, gridSize * y, gridSize, gridSize), 0)
                else:
                    pg.draw.rect(self.screen, (143, 143, 143), (gridSize * x, gridSize * y, gridSize, gridSize), 1)
        
    def gameTick(self):
        """
        One tick of the game
        Controlls all motion of the game
        Can be sped up or slowed down depending on the clock
        Can be called to run the game, decide direction and then run the tick
        """

        # get the current keys pressed
        key = pg.key.get_pressed()
            
        # Change the direction of the snake
        self.changeDirection(key)

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
            # valid space, move
            self.move(False, positionToCheck)
        elif positionValue == 1 or positionValue == 2:
            # Hit yourself or a wall, lose
            self.endGame(False)
        elif positionValue == 3:
            # Collect dot thing, grow and move into the place
            self.move(True, positionToCheck)
            self.foodSpawned = False
            self.spawnFood(self.gridCount)

    def move(self, grow, position):
        """
        Moves the snake based on the direction
        """
        self.snake.append(position)
        self.position = position
        if not grow:
            self.removeTail()
        else:
            self.score += 10

        self.grid[position[0]][position[1]] = 2

    def removeTail(self):
        """
        Remove the last block from the snake when it doesn't grow
        """
        # Get the tail
        positionToRemove = self.snake[0]
        # Remove it from the grid
        self.grid[positionToRemove[0]][positionToRemove[1]] = 0
        # Remove it from the array
        self.snake.__delitem__(0)


    def endGame(self, win):
        """
        Ends the game
        Pass in a boolean to know if you won or lost
        """
        self.active = False
    
    def spawnFood(self, gridCount):
        if(not self.foodSpawned):
            xCoord = random.randint(1, gridCount - 1)
            yCoord = random.randint(1, gridCount - 1)
            if self.grid[xCoord][yCoord] == 0:
                self.grid[xCoord][yCoord] = 3
                self.foodSpawned = True
            else:
                self.spawnFood(gridCount)
    
    def changeDirection(self, key):
        direction = -1
        if(key[pg.K_UP] or key[pg.K_w]):
            direction = 0
        elif key[pg.K_RIGHT] or key[pg.K_d]:
            direction = 1
        elif key[pg.K_DOWN] or key[pg.K_s]:
            direction = 2
        elif key[pg.K_LEFT] or key[pg.K_a]:
            direction = 3
        
        # Make sure you can't turn back on yourself
        if not self.opposites.get(direction) == self.direction and direction != -1:
            self.direction = direction

def start():
    pg.init()
    main = Main(False)
    main.runGame()

# Uncomment this to play the game
# start()