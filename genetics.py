from network import NeuralNetwork
import numpy as np
import random
from snake import Main
import pygame as pg
import copy
import operator
import matplotlib
import matplotlib.pyplot as plt
import os

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
    # Number of generations to run
    max_generations = 100
    # Display the graphics or not
    show_graphics = True
    # If true, will save the last generation that can be loaded and started from later
    save_population = False
    # If true, will save the best individual from every generation
    save_best = False
    # If true, will save the graph at the end to a png 
    save_graph = False
    # List that stores the average score of every generation
    generationScores = []
    # Generation max scores
    generationMaxScores = []

    def __init__(self):
        # Get the initial neural network model
        # TODO: Have option to read from a file
        self.model = NeuralNetwork(input_shape=(16), action_space=4).model
        # The number of the run the program is on, used for saving the models
        self.overallRun = 0
        # Stuff for reading the file
        runFile = open("./runs/run.txt", 'r')
        self.overallRun = int(runFile.read(1))
        runFile.close()
        pg.init()
        # Create the initial population
        population = self.createInitalPopulation()
        self.runGenetics(population)
        runFile = open("./runs/run.txt", 'w')
        runFile.write(str(self.overallRun + 1))
        runFile.close()

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
                        #initialWeights[a][b] = test
                        continue
                    for c in range(0, len(b_layer)):
                        c_layer = b_layer[c]
                        if not isinstance(c_layer, np.ndarray):
                            initialWeights[a][b][c] = self.getRandomWeight()
                            #initialWeights[a][b][c] = test
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
            q_values = model.predict(np.expand_dims(np.asarray(snake.createVision()).astype(np.float64), axis=0), batch_size=1)
            action = np.argmax(q_values)
            snake.rotate(action)
            snake.gameTick()
            if self.show_graphics:
                snake.updateScreen()
            counter += 1
            if counter > 10000:
                self.run = self.run + 1
                return {value: snake.getFitness()}

        score = snake.getFitness()
        self.run = self.run + 1
        return {value : score}
        # return {value : score}

    def runGenetics(self, population):
        """
        Runs the simulation
        """
        while self.generation < self.max_generations:
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
            population = newPopulation
            #newPopulation = self.mutate(newPopulation)
            print("Generation: {}".format(self.generation))
        # Ending things
        print(self.generationScores)
        print(self.generationMaxScores)
        x = range(0, self.max_generations)

        fig, ax = plt.subplots()
        ax.plot(x, self.generationScores, x, self.generationMaxScores)
        ax.set(xlabel='generation', ylabel='avg score', title='Generations Over Time')
        ax.grid()
        if self.save_graph:
            fig.savefig("graph{}.png".format(self.overallRun))
        plt.show()

        self.savePopulation(population)


    def killWeak(self, population, scores):
        sortedScores = sorted(scores.items(), key=operator.itemgetter(1))
        sortedScores.reverse()
        self.generationMaxScores.append(sortedScores[0][1])
        # TODO: Change later to get random amounts of 0's at end
        sortedScores = sortedScores[:int(self.population_size * self.selection_rate)]
        newPopulationIds = []
        for i in range(0, len(sortedScores)):
            newPopulationIds.append(sortedScores[i][0])
        print(newPopulationIds)

        newPopulation = []
        
        for i in range(0, len(newPopulationIds)):
            newPopulation.append(population[newPopulationIds[i]])
        return newPopulation

    def breedToFull(self, parents):
        newPopulation = copy.deepcopy(parents)
        i=0
        while len(newPopulation) < self.population_size:
            #print("running: {}".format(i))
            i+=1
            rand1 = random.choice(range(0, int(self.population_size * self.selection_rate)))
            rand2 = rand1
            while(rand2 == rand1):
                rand2 = random.choice(range(0, int(self.population_size * self.selection_rate)))
            parent1 = parents[rand1]
            parent2 = parents[rand2]
            if not np.array_equal(parent1, parent2):
                newPopulation.append(self.breed(parent1, parent2))
            else:
                print("same")
                pass
        
        return newPopulation

    def breed(self, parent1, parent2):
        """
        Breeds two parents together to get a child
        The child gets attributes from both of its parents
        """
        child = copy.deepcopy(parent1)
        for a in range(0, len(child)):
            a_layer = child[a]
            for b in range(0, len(a_layer)):
                b_layer = a_layer[b]
                if not isinstance(b_layer, np.ndarray):
                    if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                        child[a][b] = self.getRandomWeight()
                    elif random.choice((True, False)):
                            child[a][b] = copy.deepcopy(parent2[a][b])
                    continue
                for c in range(0, len(b_layer)):
                    c_layer = b_layer[c]
                    if not isinstance(c_layer, np.ndarray):
                        if np.random.choice((True, False), p=[self.mutation_rate, 1-self.mutation_rate]):
                            child[a][b][c] = self.getRandomWeight()
                        elif random.choice((True, False)):
                            child[a][b][c] = copy.deepcopy(parent2[a][b][c])
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
        """
        Gets a random weight for the model
        """
        return random.uniform(-self.random_weight_range, self.random_weight_range)

    def savePopulation(self, population):
        """
        Saves the entire population
        """
        if self.save_population:
            os.makedirs('./runs/run{}/population'.format(self.overallRun), exist_ok=True)
            for i in range(len(population)):
                self.model.set_weights(population[i])
                self.model.save('./runs/run{}/population/individual{}.h5'.format(self.overallRun, i))

    def saveBest(self, best):
        """
        Saves the best model for a generation
        """
        if self.save_best:
            os.makedirs('./runs/run{}/best'.format(self.overallRun), exist_ok=True)
            self.model.set_weights(best)
            self.model.save('./runs/run{}/best/generation{}/h5'.format(self.overallRun, self.generation))

    def average(self, list):
        total = 0
        for i in range(len(list)):
            total += list[i]
        
        return total / len(list)

Genetics()
