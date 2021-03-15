from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board
from typing import Union

from populationEntity import PopulationEntity


class RandomSearch:
    @staticmethod
    def RandomSearch(board: Board, numberOfRounds, printOutput: bool = False) -> Union[PopulationEntity, None]:
        lossWeights = LossWeights()
        lossCalculator = LossCalculator(lossWeights)
        for i in range(numberOfRounds):
            if printOutput:
                print(f"Attempt {i + 1}/{numberOfRounds}")

            population = board.generateRandomPopulation(1000)
            for entity in population:
                (_, isValid, _) = lossCalculator.calculateLoss(entity, board)
                if isValid:
                    return entity
        return None
