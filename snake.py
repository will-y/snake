import pygame as pg
import sys
import random
import math

class Main():
    def __init__(self, showGraphics, individual=None, generation=None, run=None):
        # Used to show graphics or not
        self.showGraphics = showGraphics
        # The size of the individual grid squares
        self.gridSize = 15
        # The number of squares on the game board
        self.gridCount = 30
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
        self.position = x, y = int(self.gridCount / 2), int(self.gridCount / 2)
        # Is the game active?
        self.active = True
        # Stores all of the positions of the snake
        self.snake = [(int(self.gridCount / 2), int(self.gridCount / 2))]
        # Clock for controlling fps
        self.clock = pg.time.Clock()
        # FPS min 1 max 1000 (default 10)
        self.fps = 50
        # If there is food on the screen
        self.foodSpawned = False
        # Location of the food
        self.foodPos = (0, 0)
        # Spawn the first food
        self.spawnFood(self.gridCount)
        # Score
        self.score = 0
        # Move Counter
        self.moves = 0
        # Last move used
        self.lastMove = -1
        # Counter to help prevent loops
        self.lastMoveCounter = 0
        # If the game ended in a loop
        self.endedLoop = False
        # Boolean for if the snake moved towards the food
        self.towardsFood = True
        # Moves left before the snake dies, resets when food is eaten
        self.movesLeft = 200

        font = pg.font.SysFont("Arial", 12)
        self.individualText = None
        self.generationText = None
        self.runTest = None
        if individual != None:
            self.individualText = font.render("Individual: " + str(individual), True, (255, 255, 255))
        if generation != None:
            self.generationText = font.render("Generation: " + str(generation), True, (255, 255, 255))
        if run != None:
            self.runText = font.render("Total Runs: " + str(run), True, (255, 255, 255))

        # Used to tell if a snake is trying to move back on itself
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

        print("Final Score: {}".format(self.score))

    def updateScreen(self):
        if self.showGraphics:
            self.screen.fill((110, 110, 110))
            self.drawGrid(self.gridSize, self.gridCount)

            if self.individualText != None:
                self.screen.blit(self.individualText, (5, 0))
            if self.generationText != None:
                self.screen.blit(self.generationText, (5, 20))
            if self.individualText != None:
                self.screen.blit(self.runText, (5, 40))

            # update the screen
            pg.display.flip()
            self.clock.tick(self.fps)
    
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
        grid[int(self.gridCount / 2)][int(self.gridCount / 2)] = 2
        
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
        
        self.moves += 1
        self.movesLeft -= 1
        if self.movesLeft <= 0:
            self.active = False

        if self.lastMoveCounter >= 100:
            self.active = False
            self.endedLoop = True

    def move(self, grow, position):
        """
        Moves the snake based on the direction
        """
        self.snake.append(position)
        self.position = position

        if not grow:
            self.removeTail()
        else:
            self.score += 1
            self.movesLeft = 200

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
        """
        Spawns food in a random location
        Called when food is collected and when the game starts
        """
        if(not self.foodSpawned):
            xCoord = random.randint(1, gridCount - 1)
            yCoord = random.randint(1, gridCount - 1)
            self.foodPos = (xCoord, yCoord)
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
    
    def rotate(self, direction):
        if direction != self.opposites.get(self.direction):
            self.direction = direction

    def getFitness(self):
        return self.score * 10 + self.moves / 10
    
    def createVision(self):
        """
        Used to create the list to insert into neural network
        Consits of 16 parameters, 8 directions with distance to food and distance to a wall/body for each direction
        """
        #            N       NE      E      SE       S      SW       W      NW
        #          0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
        result = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        
        i = 1
        y = self.position[0]
        x = self.position[1]
        while i < self.gridCount:
            #N
            if y - i >= 0:
                temp = self.grid[y - i][x]
                if temp == 1 or temp == 2:
                    result[0] = 1/i
                elif temp == 3:
                    result[1] = 1/i
                    
            #NE
            if x + i < self.gridCount and y - i >= 0:
                temp = self.grid[y - i][x + i]
                if temp == 1 or temp == 2:
                    result[2] = 1/i
                elif temp == 3:
                    result[3] = 1/i
            
            #E
            if x + i < self.gridCount:
                temp = self.grid[y][x + i]
                if temp == 1 or temp == 2:
                    result[4] = 1/i
                elif temp == 3:
                    result[5] = 1/i
            
            #SE
            if x + i < self.gridCount and y + i < self.gridCount:
                temp = self.grid[y + i][x + i]
                if temp == 1 or temp == 2:
                    result[6] = 1/i
                elif temp == 3:
                    result[7] = 1/i
                    
            #S
            if y + i < self.gridCount:
                temp = self.grid[y + i][x]
                if temp == 1 or temp == 2:
                    result[8] = 1/i
                elif temp == 3:
                    result[9] = 1/i
            
            #SW
            if x - i >= 0 and y + i < self.gridCount:
                temp = self.grid[y + i][x - i]
                if temp == 1 or temp == 2:
                    result[10] = 1/i
                elif temp == 3:
                    result[11] = 1/i
                    
            #W
            if x - i >= 0:
                temp = self.grid[y][x - i]
                if temp == 1 or temp == 2:
                    result[12] = 1/i
                elif temp == 3:
                    result[13] = 1/i
                    
            #NW
            if x - i >= 0 and y - i >= 0:
                temp = self.grid[y - i][x - i]
                if temp == 1 or temp == 2:
                    result[14] = 1/i
                elif temp == 3:
                    result[15] = 1/i
                
            i += 1

        #print("   N     NE     E     SE      S      SW     W      NW")
        #print(result)
        return result

def start():
    pg.init()
    main = Main(True)
    main.runGame()

# Uncomment this to play the game
# start()