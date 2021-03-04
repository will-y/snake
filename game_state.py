import random
import pygame as pg
import numpy as np


class GameState:
    def __init__(self, game_position, grid_size):
        self.grid_count = 30
        self.grid_size = grid_size
        # creates the game grid
        self.grid = self.createGrid(self.grid_count)
        # 0: up
        # 1: right
        # 2: down
        # 3 left
        self.direction = 1
        # Current position of the head of the snake
        self.position = int(self.grid_count / 2), int(self.grid_count / 2)
        # Is the game active?
        self.active = True
        # Stores all of the positions of the snake
        self.snake = [(int(self.grid_count / 2), int(self.grid_count / 2))]
        # If there is food on the screen
        self.food_spawned = False
        # Location of the food
        self.food_pos = (0, 0)
        # Spawn the first food
        self.spawn_food()
        # Score
        self.score = 0
        # Move Counter
        self.moves = 0
        # If the game ended in a loop
        self.ended_loop = False
        # Boolean for if the snake moved towards the food
        self.towards_food = True
        # Moves left before the snake dies, resets when food is eaten
        self.moves_left = 200
        # Used to tell if a snake is trying to move back on itself
        self.opposites = {
            0: 2,
            1: 3,
            2: 0,
            3: 1
        }
        self.game_position = game_position

        self.font = pg.font.SysFont("Arial", 12)

    def createGrid(self, grid_count):
        """
        Creates the game grid with walls on the outside
        0 = Empty
        1 = Wall
        2 = Player
        3 = Dot
        """
        grid = []
        # Set the game grid with walls on the edges
        for x in range(grid_count):
            row = []
            for y in range(grid_count):
                if x == 0 or y == 0 or x == grid_count - 1 or y == grid_count - 1:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)

        # Set the player
        grid[int(self.grid_count / 2)][int(self.grid_count / 2)] = 2

        return grid

    def spawn_food(self):
        """
        Spawns food in a random location
        Called when food is collected and when the game starts
        """
        if not self.food_spawned:
            xCoord = random.randint(1, self.grid_count - 1)
            yCoord = random.randint(1, self.grid_count - 1)
            self.food_pos = (xCoord, yCoord)
            if self.grid[xCoord][yCoord] == 0:
                self.grid[xCoord][yCoord] = 3
                self.food_spawned = True
            else:
                self.spawn_food()

    def game_tick(self, model):
        """
        One tick of the game
        Controls all motion of the game
        Can be sped up or slowed down depending on the clock
        Can be called to run the game, decide direction and then run the tick
        """

        action = np.argmax(model.predict(self.create_vision()))
        self.rotate(action)

        position_to_check = (0, 0)

        if self.direction == 0:
            position_to_check = self.position[0], self.position[1] - 1
        elif self.direction == 1:
            position_to_check = self.position[0] + 1, self.position[1]
        elif self.direction == 2:
            position_to_check = self.position[0], self.position[1] + 1
        elif self.direction == 3:
            position_to_check = self.position[0] - 1, self.position[1]

        position_value = self.grid[position_to_check[0]][position_to_check[1]]

        if position_value == 0:
            # valid space, move
            self.move(False, position_to_check)
        elif position_value == 1 or position_value == 2:
            # Hit yourself or a wall, lose
            self.end_game(False)
        elif position_value == 3:
            # Collect dot thing, grow and move into the place
            self.move(True, position_to_check)
            self.food_spawned = False
            self.spawn_food()

        self.moves += 1
        self.moves_left -= 1
        if self.moves_left <= 0:
            self.active = False
            self.ended_loop = True

    def move(self, grow, position):
        """
        Moves the snake based on the direction
        """
        self.snake.append(position)
        self.position = position

        if not grow:
            self.remove_tail()
        else:
            self.score += 1
            self.moves_left = 200

        self.grid[position[0]][position[1]] = 2

    def end_game(self, win):
        """
        Ends the game
        Pass in a boolean to know if you won or lost
        """
        self.active = False

    def remove_tail(self):
        """
        Remove the last block from the snake when it doesn't grow
        """
        # Get the tail
        position_to_remove = self.snake[0]
        # Remove it from the grid
        self.grid[position_to_remove[0]][position_to_remove[1]] = 0
        # Remove it from the array
        self.snake.__delitem__(0)

    def draw_game(self, screen):
        """
        Draws this game on the screen at its position
        """
        for x in range(0, self.grid_count):
            for y in range(0, self.grid_count):
                rect = (self.game_position[0] + self.grid_size * x, self.game_position[1] + self.grid_size * y, self.grid_size, self.grid_size)
                if self.grid[x][y] == 1:
                    pg.draw.rect(screen, (0, 0, 0), rect, 0)
                    pg.draw.rect(screen, (61, 61, 61), rect, 1)
                elif self.grid[x][y] == 2:
                    pg.draw.rect(screen, (35, 196, 14), rect, 0)
                elif self.grid[x][y] == 3:
                    pg.draw.rect(screen, (226, 242, 0), rect, 0)
                else:
                    pg.draw.rect(screen, (143, 143, 143), rect, 1)

        text = self.font.render("Score: " + str(self.get_fitness()), True, (255, 255, 255))
        screen.blit(text, (self.game_position[0] + 5, self.game_position[1] + 10))

    def create_vision(self):
        """
        Used to create the list to insert into neural network
        Consists of 16 parameters, 8 directions with distance to food and distance to a wall/body for each direction
        """
        #            N       NE      E      SE       S      SW       W      NW
        #          0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
        result = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        i = 1
        y = self.position[0]
        x = self.position[1]
        while i < self.grid_count:
            # N
            if y - i >= 0:
                temp = self.grid[y - i][x]
                if temp == 1 or temp == 2:
                    result[0] = 1 / i
                elif temp == 3:
                    result[1] = 1 / i

            # NE
            if x + i < self.grid_count and y - i >= 0:
                temp = self.grid[y - i][x + i]
                if temp == 1 or temp == 2:
                    result[2] = 1 / i
                elif temp == 3:
                    result[3] = 1 / i

            # E
            if x + i < self.grid_count:
                temp = self.grid[y][x + i]
                if temp == 1 or temp == 2:
                    result[4] = 1 / i
                elif temp == 3:
                    result[5] = 1 / i

            # SE
            if x + i < self.grid_count and y + i < self.grid_count:
                temp = self.grid[y + i][x + i]
                if temp == 1 or temp == 2:
                    result[6] = 1 / i
                elif temp == 3:
                    result[7] = 1 / i

            # S
            if y + i < self.grid_count:
                temp = self.grid[y + i][x]
                if temp == 1 or temp == 2:
                    result[8] = 1 / i
                elif temp == 3:
                    result[9] = 1 / i

            # SW
            if x - i >= 0 and y + i < self.grid_count:
                temp = self.grid[y + i][x - i]
                if temp == 1 or temp == 2:
                    result[10] = 1 / i
                elif temp == 3:
                    result[11] = 1 / i

            # W
            if x - i >= 0:
                temp = self.grid[y][x - i]
                if temp == 1 or temp == 2:
                    result[12] = 1 / i
                elif temp == 3:
                    result[13] = 1 / i

            # NW
            if x - i >= 0 and y - i >= 0:
                temp = self.grid[y - i][x - i]
                if temp == 1 or temp == 2:
                    result[14] = 1 / i
                elif temp == 3:
                    result[15] = 1 / i

            i += 1

        # print("   N     NE     E     SE      S      SW     W      NW")
        # print(result)
        return result

    def rotate(self, direction):
        if direction != self.opposites.get(self.direction):
            self.direction = direction

    def get_fitness(self):
        fitness = self.score * 10
        if not self.ended_loop:
            return fitness + self.moves / 10
        else:
            return fitness
