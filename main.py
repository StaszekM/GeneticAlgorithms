from entitySelectors import TournamentSelector
from geneticAlgorithm import GeneticAlgorithm
from lossCalculator import LossWeights, LossCalculator
from randomSearch import RandomSearch
from pcbBoard import loadFromFile
from tests.methodTests import testGenRandomPopulation, testLossCalculator

from visualizer import visualize


def tryRandomSearch():
    board = loadFromFile('textTests/zad0.5.txt')
    result = RandomSearch.RandomSearch(board, 10, printOutput=True)
    if result is None:
        print("Could not find a solution")
    else:
        print("Found a solution:")
        visualize(result, board,
                  f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\randomsearch.png')
        for path in result.paths:
            print(path)


def tryGA():
    board = loadFromFile('textTests/zad1.txt')
    populationSize = 1000
    selector = TournamentSelector(150)
    crossoverThreshold = 0.2
    crossoverProbability = 0.2
    mutationProbability = 0.1
    mutationStrength = 3
    maximumLoss = 25

    lossWeights = LossWeights()
    lossWeights.intersectionCount = 20
    lossWeights.outOfBoardPathCount = 30
    lossWeights.outOfBoardLength = 25
    lossWeights.totalPathLength = 0.5
    lossWeights.segmentsCount = 0.5
    calculator = LossCalculator(lossWeights)

    alg = GeneticAlgorithm(board, populationSize, calculator, selector, crossoverThreshold, crossoverProbability,
                           mutationProbability, mutationStrength, maximumLoss)
    alg.algorithm()


if __name__ == "__main__":
    # tryRandomSearch()
    # testLossCalculator()
    # testTournamentSelector()
    tryGA()
    # testGenRandomPopulation()
    pass
