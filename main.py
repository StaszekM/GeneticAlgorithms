from entitySelectors import TournamentSelector
from geneticAlgorithm import GeneticAlgorithm
from lossCalculator import LossWeights, LossCalculator
from randomSearch import RandomSearch
from pcbBoard import loadFromFile
from tests.methodTests import testGenRandomPopulation

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
    selector = TournamentSelector(400)
    crossoverThreshold = 0.3
    crossoverProbability = 0.3
    mutationProbability = 0.3
    mutationStrength = 3
    maximumLoss = 25

    lossWeights = LossWeights()
    lossWeights.intersectionCount = 20
    lossWeights.outOfBoardPathCount = 30
    lossWeights.outOfBoardLength = 25
    lossWeights.totalPathLength = 1
    lossWeights.segmentsCount = 1
    calculator = LossCalculator(lossWeights)

    alg = GeneticAlgorithm(board, populationSize, calculator, selector, crossoverThreshold, crossoverProbability,
                           mutationProbability, mutationStrength, maximumLoss)
    alg.algorithm()


if __name__ == "__main__":
    # tryRandomSearch()
    # testLossCalculator()
    # testTournamentSelector()
    # tryGA()
    testGenRandomPopulation()
    pass
