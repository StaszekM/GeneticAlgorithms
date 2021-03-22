from abc import ABC, abstractmethod
from random import sample as random_sample
from random import uniform
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

    @abstractmethod
    def __str__(self):
        pass


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

    def __str__(self):
        return f'Selektor turniejowy o rozmiarze {self.N}'


class RouletteSelector(Selector):

    def select(self, population: List[EntityWithLoss], board: Board,
               omitEntity: Optional[PopulationEntity] = None) -> PopulationEntity:
        minLoss: float = min(population, key=lambda element: element[1][0])[1][0]

        fitnessTotal = 0
        entitiesWithFitness = []
        for entity in population:
            fitness = minLoss / entity[1][0]
            entitiesWithFitness.append((entity[0], fitness, (fitnessTotal, fitnessTotal + fitness)))
            fitnessTotal += fitness

        while True:
            value = uniform(0, fitnessTotal)
            for entity in entitiesWithFitness:
                (minRange, maxRange) = entity[2]
                if minRange <= value < maxRange:
                    if omitEntity is None or entity[0] != omitEntity:
                        return entity[0]

    def __str__(self):
        return f'Selektor ruletkowy'
