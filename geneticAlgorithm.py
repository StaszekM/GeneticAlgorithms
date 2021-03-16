from random import Random
from typing import List

from entitySelectors import EntityWithLoss, Selector
from lossCalculator import LossCalculator
from pcbBoard import Board
from populationEntity import PopulationEntity, crossover
from visualizer import visualize

import matplotlib.pyplot as plt
from datetime import datetime


class GeneticAlgorithm:
    def __init__(self, board: Board, populationSize: int, lossCalculator: LossCalculator, selector: Selector,
                 crossoverThreshold: float, crossoverProbability: float, mutationProbability: float,
                 mutationStrength: int, maximumLoss: float):
        self.board = board
        self.populationSize = populationSize
        self.selector = selector
        self.lossCalculator = lossCalculator
        self.crossoverThreshold = crossoverThreshold
        self.crossoverProbability = crossoverProbability
        self.mutationProbability = mutationProbability
        self.mutationStrength = mutationStrength
        self.maximumLoss = maximumLoss

        self.generation = 0

    def algorithm(self):
        start = datetime.now()
        random = Random()
        initialPopulation = self.board.generateRandomPopulation(self.populationSize)
        populationWithLoss: List[EntityWithLoss] = [(entity, self.lossCalculator.calculateLoss(entity, self.board)) for
                                                    entity in initialPopulation]

        populationWithLoss.sort(key=lambda entity: entity[1][0])
        bestEntity = populationWithLoss[0]
        currentPopulation = populationWithLoss

        self.generation = 0
        plotX = []
        plotY = []
        while not self.__stopCondition(currentPopulation):
            newPopulation: List[EntityWithLoss] = []
            while len(newPopulation) != self.populationSize:
                P1: PopulationEntity = self.selector.select(currentPopulation, self.board)
                P2: PopulationEntity = self.selector.select(currentPopulation, self.board, omitEntity=P1)

                if random.random() >= self.crossoverThreshold:
                    O1: PopulationEntity = crossover(P1, P2, self.crossoverProbability)
                else:
                    O1: PopulationEntity = P1.getCopy()

                O1.mutate(self.mutationProbability, self.mutationStrength)
                entityWithLoss = (O1, self.lossCalculator.calculateLoss(O1, self.board))
                if bestEntity[1][0] > entityWithLoss[1][0]:
                    bestEntity = entityWithLoss
                newPopulation.append(entityWithLoss)
            currentPopulation = newPopulation
            self.generation += 1
            print(f"Generation {self.generation}")
            plotX.append(self.generation)
            plotY.append(bestEntity[1][0])

        end = datetime.now()
        diff = end - start
        print(f"Alg finished, time: {diff.total_seconds()}")
        print(f"Best solution, found after {self.generation - 1} generations")
        fig, ax = plt.subplots()
        ax.plot(plotX, plotY)
        plt.show()
        visualize(bestEntity[0], self.board)

    def __stopCondition(self, population: List[EntityWithLoss]) -> bool:
        for entity in population:
            if entity[1][1] or entity[1][0] <= self.maximumLoss or self.generation > 500:
                return True

        return False

    def plot(self):
        pass