from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board
from typing import Optional

from populationEntity import PopulationEntity
from utils import generateRandomPopulation


class RandomSearch:
    @staticmethod
    def RandomSearch(board: Board, numberOfRounds, printOutput: bool = False) -> Optional[PopulationEntity]:
        lossWeights = LossWeights()
        lossCalculator = LossCalculator(lossWeights)
        for i in range(numberOfRounds):
            if printOutput:
                print(f"Attempt {i + 1}/{numberOfRounds}")

            population = generateRandomPopulation(1000, board)
            for entity in population:
                (_, isValid, _) = lossCalculator.calculateLoss(entity, board)
                if isValid:
                    return entity
        return None
