from network import NeuralNetwork
import numpy as np
import random
from snake import Main
import pygame as pg
import copy
class Genetics:
    # Variables for controlling the genetics
    # Current itteration of the genetics
    run = 0
    # Current generation
    generation = 0
    # Number of individuals that will be selected to breed
    selection_rate = 0.1
    # Chance that a gene will mutate
    mutation_rate = 0.01
    # Size of the population
    population_size = 100
    # Range of weights
    random_weight_range = 1.0
    # Display the graphics or not
    show_graphics = True

    def __init__(self):
        # Get the initial neural network model
        # TODO: Have option to read from a file
        self.model = NeuralNetwork(input_shape=(10, 10), action_space=3).model
        pg.init()
        self.snake = Main(self.show_graphics)
        # Create the initial population
        population = self.createInitalPopulation()
        self.run(population)
        

    def run(self, population):
        """
        Runs the simulation
        """

        # Scores for all of the populations
        scores = {}
        actions = []

        # Run game for all members
        for i in range(0, self.population_size):
            self.model.set_weights(population[i])
            # scores.update(self.gameCycle(self.model, i))
            actions.append(self.gameCycle(self.model, i))
        
        print(actions)

    def createInitalPopulation(self):
        """
        Creates the initial population for the model to work off of
        """

        # Will be a list of weights
        population = []
        # Initial weights from the model
        initialWeights = self.model.get_weights()
        # Randomly set weight values
        for i in range(0, self.population_size):
            individual = initialWeights
            for a in range(0, len(initialWeights)):
                a_layer = initialWeights[a]
                for b in range(0, len(a_layer)):
                    b_layer = a_layer[b]
                    if not isinstance(b_layer, np.ndarray):
                        initialWeights[a][b] = self.getRandomWeight()
                        continue
                    for c in range(0, len(b_layer)):
                        c_layer = b_layer[c]
                        if not isinstance(c_layer, np.ndarray):
                            initialWeights[a][b][c] = self.getRandomWeight()
                            continue
                        for d in range(0, len(c_layer)):
                            d_layer = c_layer[d]
                            for e in range(0, len(d_layer)):
                                initialWeights[a][b][c][d][e] = self.getRandomWeight()
            population.append(copy.deepcopy(individual))
        return population

    def breed(self, parent1, parent2):
        pass

    def breedAll(self, parent1, parent2):
        pass

    def gameCycle(self, model, value):
        #print("{}: \nWeights:\n{}".format(value, model.get_weights()))
        # q_values = model.predict(np.expand_dims(np.asarray(self.snake.grid).astype(np.float64), axis=0), batch_size=1)
        #print(np.asarray(self.snake.grid).astype(np.float64))

        q_values = model.predict(np.expand_dims(np.asarray(self.snake.grid).astype(np.float64), axis=0), batch_size=1)
        print(q_values)
        print(np.argmax(q_values))
        action = np.argmax(q_values)
        
        score = random.randint(0, 10)
        return action
        # return {value : score}

    def killWeak(self, population):
        pass

    def breedToFull(self, population):
        pass

    def mutate(self, population):
        pass

    def getRandomWeight(self):
        return random.uniform(-self.random_weight_range, self.random_weight_range)

Genetics()
