from network import NeuralNetwork
import numpy as np
import random

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


    def __init__(self):
        # Get the initial neural network model
        # TODO: Have option to read from a file
        self.model = NeuralNetwork((10, 10), 3).model
        # Create the initial population
        population = self.createInitalPopulation()

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
                    for c in range(0, len(b_layer)):  # 8
                        c_layer = b_layer[c]
                        if not isinstance(c_layer, np.ndarray):
                            initialWeights[a][b][c] = self.getRandomWeight()
                            continue
            population.append(individual)
        
        return population

    def breed(self, parent1, parent2):
        pass

    def breedAll(self, parent1, parent2):
        pass

    def gameCycle(self, model):
        pass

    def killWeak(self, population):
        pass

    def breedToFull(self, population):
        pass

    def mutate(self, population):
        pass

    def getRandomWeight(self):
        return random.uniform(-self.random_weight_range, self.random_weight_range)

Genetics()
