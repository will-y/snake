import pygame as pg
from game_state import GameState


class Main:
    def __init__(self, showGraphics, pop_size=25, generation=None, run=None):
        # Used to show graphics or not
        self.showGraphics = showGraphics
        # square root of the number of games to show
        self.games_to_show = 5
        # The size of the individual grid squares
        self.gridSize = 7
        # The number of squares on the game board
        self.gridCount = 30
        # size of the screen
        self.size = self.gridSize * self.gridCount * self.games_to_show, self.gridSize * self.gridCount * self.games_to_show
        # pygame screen
        if self.showGraphics:
            self.screen = pg.display.set_mode(self.size)
        # Clock for controlling fps
        self.clock = pg.time.Clock()
        # FPS min 1 max 1000 (default 10)
        self.fps = 50

        font = pg.font.SysFont("Arial", 12)

        if generation is not None:
            self.generationText = font.render("Generation: " + str(generation), True, (255, 255, 255))
        if run is not None:
            self.runText = font.render("Total Runs: " + str(run), True, (255, 255, 255))

        # Used to tell if a snake is trying to move back on itself
        self.opposites = {
            0: 2,
            1: 3,
            2: 0,
            3: 1
        }

        self.pop_size = pop_size
        self.game_states = self.create_game_states()

    def create_game_states(self):
        game_states = []
        for i in range(self.pop_size):
            x = i % self.games_to_show
            y = i // self.games_to_show
            game_states.append(GameState((x * self.gridCount * self.gridSize, y * self.gridCount * self.gridSize), self.gridSize))

        return game_states

    def run_generation(self, population, model, generation):
        font = pg.font.SysFont("Arial", 12)
        self.generationText = font.render("Generation: " + str(generation), True, (255, 255, 255))
        passed = 0
        size = len(population)
        scores = {}
        while passed < size:
            passed = 0
            for i in range(size):
                snake = self.game_states[i]
                if snake.active:
                    model.set_weights(population[i])
                    snake.game_tick(model)
                else:
                    passed += 1

            self.update_screen()

        for i in range(size):
            scores.update({i: self.game_states[i].get_fitness()})

        return scores

    def update_screen(self):
        if self.showGraphics:
            self.screen.fill((110, 110, 110))
            self.draw_games()

            if self.generationText is not None:
                self.screen.blit(self.generationText, (5, 0))
            if self.runText is not None:
                self.screen.blit(self.runText, (5, 20))

            # update the screen
            pg.display.flip()
            # self.clock.tick(self.fps)

    def draw_games(self):
        """
        Draws all grids on the screen
        """
        for i in range(self.games_to_show ** 2):
            self.game_states[i].draw_game(self.screen)

    def clear(self):
        self.screen.fill((110, 110, 110))
        self.game_states = self.create_game_states()
