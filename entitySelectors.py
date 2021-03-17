from abc import ABC, abstractmethod
from random import sample as random_sample
from typing import List, Tuple, Optional

from populationEntity import PopulationEntity
from pcbBoard import Board
from lossCalculator import CalculatorResult

EntityWithLoss = Tuple[PopulationEntity, CalculatorResult]


class Selector(ABC):
    @abstractmethod
    def select(self, population: List[EntityWithLoss], board: Board,
               omitEntity: Optional[PopulationEntity] = None) -> PopulationEntity:
        """Allows to select an Entity from population with
        optional omitting of a specific Entity to avoid duplication"""


class TournamentSelector(Selector):
    def __init__(self, N: int):
        self.N = N

    def select(self, population: List[EntityWithLoss], board: Board,
               omitEntity: Optional[PopulationEntity] = None) -> PopulationEntity:

        populationLength = len(population)
        if self.N < 1 or self.N > populationLength:
            raise ValueError(
                f"TournamentSelector - trying to select {self.N} from a population with {populationLength} entities.")
        while True:
            populationSample: List[Tuple[PopulationEntity, CalculatorResult]] = random_sample(population, self.N)
            bestSample: PopulationEntity = min(populationSample, key=lambda pair: pair[1][0])[0]

            if omitEntity is None or bestSample != omitEntity:
                return bestSample
