from network import NeuralNetwork
import numpy as np
import random
from snake import Main
import pygame as pg
import copy
import operator
import matplotlib
import matplotlib.pyplot as plt

class Genetics:
    # Parameters for controlling the genetics
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
    # Number of generations to run
    maxGenerations = 3
    # List that stores the average score of every generation
    generationScores = []

    def __init__(self):
        # Set up the distribution for selecting parents
        self.distribution = []
        for i in range(0, int(self.population_size * self.selection_rate)):
            self.distribution += [i] * (int(self.population_size * self.selection_rate) - i)
        # Get the initial neural network model
        # TODO: Have option to read from a file
        self.model = NeuralNetwork(input_shape=(10, 10), action_space=3).model
        pg.init()
        # Create the initial population
        population = self.createInitalPopulation()
        self.runGenetics(population)

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
            population.append(copy.deepcopy(individual))
        return population

    def gameCycle(self, model, value):
        """
        Does a game cycle for the passed in model
        Returns the score that it got
        """
        snake = Main(self.show_graphics, value, self.generation, self.run)
        counter = 0
        while snake.active:
            q_values = model.predict(np.expand_dims(np.asarray(snake.grid).astype(np.float64), axis=0), batch_size=1)
            action = np.argmax(q_values)
            if action == 1:
                snake.goLeft()
            elif action == 2:
                snake.goRight()
            snake.gameTick()
            if self.show_graphics:
                snake.updateScreen()
            counter += 1
            if counter > 10000:
                self.run = self.run + 1
                return {value: self.calculateScore(snake)}

        score = self.calculateScore(snake)
        self.run = self.run + 1
        return {value : score}
        # return {value : score}

    def runGenetics(self, population):
        """
        Runs the simulation
        """

        # Scores for all of the populations
        scores = {}

        # Run game for all members
        for i in range(0, self.population_size):
            self.model.set_weights(population[i])
            scores.update(self.gameCycle(self.model, i))
        
        print(scores)
        self.generationScores.append(self.average(scores))
        self.generation += 1

        # Kill the bottom 90% of the population
        parents = self.killWeak(population, scores)

        # Breed new ones from the top 10% of performers
        newPopulation = self.breedToFull(parents)
        #newPopulation = self.mutate(newPopulation)
        print("Generation: {}".format(self.generation))
        if self.generation < self.maxGenerations:
            self.runGenetics(newPopulation)
        else:
            # Ending things
            print(self.generationScores)
            x = range(0, self.maxGenerations)

            fig, ax = plt.subplots()
            ax.plot(x, self.generationScores)
            ax.set(xlabel='generation', ylabel='avg score', title='Generations Over Time')
            ax.grid()
            fig.savefig("test.png")
            plt.show()

    def killWeak(self, population, scores):
        sortedScores = sorted(scores.items(), key=operator.itemgetter(1))
        sortedScores.reverse()
        # TODO: Change later to get random amounts of 0's at end
        sortedScores = sortedScores[:int(self.population_size * self.selection_rate)]
        
        newPopulationIds = []
        for i in range(0, len(sortedScores)):
            newPopulationIds.append(sortedScores[i][0])
        print(newPopulationIds)

        newPopulation = []
        
        for i in range(0, len(newPopulationIds)):
            newPopulation.append(population[i])
        
        return newPopulation

    def breedToFull(self, parents):
        newPopulation = copy.deepcopy(parents)

        while len(newPopulation) < self.population_size:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if not np.array_equiv(parent1, parent2):
                newPopulation.append(self.breed(parent1, parent2))
        
        return newPopulation

    def breed(self, parent1, parent2):
        """
        Breeds two parents together to get a child
        The child gets attributes from both of its parents
        """
        child = parent1
        for a in range(0, len(child)):
            a_layer = child[a]
            for b in range(0, len(a_layer)):
                b_layer = a_layer[b]
                if not isinstance(b_layer, np.ndarray):
                    if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                        child[a][b] = self.getRandomWeight()
                    elif random.choice((True, False)):
                            child[a][b] = parent2[a][b]
                    continue
                for c in range(0, len(b_layer)):
                    c_layer = b_layer[c]
                    if not isinstance(c_layer, np.ndarray):
                        if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                            child[a][b][c] = self.getRandomWeight()
                        elif random.choice((True, False)):
                            child[a][b][c] = parent2[a][b][c]
                        continue

        return child

    def mutate(self, population):
        """
        Mutates the population randomly based on the mutation rate
        """
        for i in range(0, len(population)):
            toMutate = population[i]
            for a in range(0, len(toMutate)):
                a_layer = toMutate[a]
                for b in range(0, len(a_layer)):
                    b_layer = a_layer[b]
                    if not isinstance(b_layer, np.ndarray):
                        if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                            toMutate[a][b] = self.getRandomWeight()
                        continue
                    for c in range(0, len(b_layer)):
                        c_layer = b_layer[c]
                        if not isinstance(c_layer, np.ndarray):
                            if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                                toMutate[a][b][c] = self.getRandomWeight()
                            continue
        return population

    def getRandomWeight(self):
        return random.uniform(-self.random_weight_range, self.random_weight_range)

    def calculateScore(self, snake):
        score = snake.score + snake.moves / 100
        if snake.moves > 10000:
            score -= 1000
        if snake.endedLoop:
            score -= 1

        return score

    def average(self, list):
        total = 0
        for i in range(len(list)):
            total += list[i]
        
        return total / len(list)

Genetics()
