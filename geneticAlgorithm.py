from random import Random
from typing import List, Set, Dict, Tuple

from entitySelectors import EntityWithLoss, Selector
from lossCalculator import LossCalculator
from pcbBoard import Board
from populationEntity import PopulationEntity, crossover
from utils import generateRandomPopulation
from visualizer import visualize

import os

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
        initialPopulation = generateRandomPopulation(self.populationSize, self.board)
        alphaWeights = [1 for _ in initialPopulation[0].paths]
        intersectionPointsWeights: Dict[Tuple[int, int], int] = {}

        for x in range(self.board.width + 1):
            for y in range(self.board.height + 1):
                intersectionPointsWeights[(x, y)] = 1

        populationWithLoss: List[EntityWithLoss] = [
            (entity, self.lossCalculator.calculateLoss(entity, self.board, alphaWeights, intersectionPointsWeights)) for
            entity in initialPopulation]

        populationWithLoss.sort(key=lambda entity: entity[1][0])
        bestEntity = populationWithLoss[0]
        currentPopulation = populationWithLoss

        self.generation = 0
        plotX = []
        plotY = []
        while not self.__stopCondition(currentPopulation):
            newPopulation: List[EntityWithLoss] = []
            self.generation += 1
            print(f"Creating generation {self.generation}")
            while len(newPopulation) != self.populationSize:
                P1: PopulationEntity = self.selector.select(currentPopulation, self.board)
                P2: PopulationEntity = self.selector.select(currentPopulation, self.board, omitEntity=P1)

                if random.random() >= self.crossoverThreshold:
                    O1: PopulationEntity = crossover(P1, P2, self.crossoverProbability)
                else:
                    O1: PopulationEntity = P1.getCopy()

                O1.mutate(self.mutationProbability, self.mutationStrength, self.board)
                entityWithLoss: EntityWithLoss = (
                    O1, self.lossCalculator.calculateLoss(O1, self.board, alphaWeights, intersectionPointsWeights))
                newPopulation.append(entityWithLoss)

            bestInGeneration = min(newPopulation, key=lambda ent: ent[1][0])
            if bestEntity[1][0] > bestInGeneration[1][0]:
                bestEntity = bestInGeneration
            else:
                intersectingPaths: Set[int] = bestInGeneration[1][3]
                intersectionPoints: Set[Tuple[int, int]] = bestInGeneration[1][4]
                for element in intersectingPaths:
                    alphaWeights[element] += 1
                for point in intersectionPoints:
                    intersectionPointsWeights[point] += 1
            currentPopulation = newPopulation
            plotX.append(self.generation)
            plotY.append(bestInGeneration[1][0])
            if self.generation % 10 == 0:
                visualize(bestInGeneration[0], self.board,
                          f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\generation-{self.generation}.png')

        end = datetime.now()
        diff = end - start
        print(f"Alg finished, time: {diff.total_seconds()}")
        print(f"Best solution, found after {self.generation} generations")
        visualize(bestEntity[0], self.board,
                  f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\bestsolution.png')
        fig, ax = plt.subplots()
        ax.plot(plotX, plotY)
        plt.show()

    def __stopCondition(self, population: List[EntityWithLoss]) -> bool:
        for entity in population:
            if entity[1][1] or self.generation > 2000:
                return True

        return False

    def plot(self):
        # plt.savefig(f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\generation-stats-{self.generation}.png')
        pass
