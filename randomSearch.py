from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board
from typing import Optional

from populationEntity import PopulationEntity
from utils import generateRandomPopulation


class RandomSearch:
    @staticmethod
    def RandomSearch(board: Board, numberOfRounds, printOutput: bool = False,
                     populationSize: int = 1000) -> Optional[PopulationEntity]:
        lossWeights = LossWeights()
        lossCalculator = LossCalculator(lossWeights)

        intersectionsDict = {}
        for x in range(board.width + 1):
            for y in range(board.height + 1):
                intersectionsDict[(x, y)] = 1

        for i in range(numberOfRounds):
            if printOutput:
                print(f"Attempt {i + 1}/{numberOfRounds}")

            population = generateRandomPopulation(populationSize, board)
            alphaWeights = [1 for _ in population[0].paths]
            for entity in population:
                (_, isValid, _, _, _) = lossCalculator.calculateLoss(entity, board, alphaWeights, intersectionsDict)
                if isValid:
                    return entity
        return None
