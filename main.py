import pygame as pg
import sys

class Main():
    def __init__(self):
        self.gridSize = 50
        self.gridCount = 10
        self.size = width, height = self.gridSize * self.gridCount, self.gridSize * self.gridCount
        self.screen = pg.display.set_mode(self.size)
        self.createGrid(10)
        self.grid = self.createGrid(self.gridCount)
    def runGame(self):
        while 1:
            # If exited, don't crash
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    sys.exit()
            
            #draw things for the game
            self.screen.fill((110, 110, 110))
            self.drawGrid(self.gridSize, self.gridCount)

            #update the screen
            pg.display.flip()
    
    def createGrid(self, gridCount):
        """
        Creates the game grid with walls on the outside
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
        
        return grid
    
    def drawGrid(self, gridSize, gridCount):
        for x in range(0, gridCount):
            for y in range(0, gridCount):
                if self.grid[x][y] == 1:
                    pg.draw.rect(self.screen, (0, 0, 0), (gridSize * x, gridSize * y, gridSize, gridSize), 0)
                    pg.draw.rect(self.screen, (61, 61, 61), (gridSize * x, gridSize * y, gridSize, gridSize), 1)
                else:
                    pg.draw.rect(self.screen, (143, 143, 143), (gridSize * x, gridSize * y, gridSize, gridSize), 1)

def main():
    pg.init()
    main = Main()
    main.runGame()

main()