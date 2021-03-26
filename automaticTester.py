import os
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import wait, ALL_COMPLETED

from entitySelectors import TournamentSelector
from geneticAlgorithm import GeneticAlgorithm
from lossCalculator import LossWeights, LossCalculator
from pcbBoard import loadFromFile
import statistics

path = f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults'


def createDefaultLossCalculator():
    lossWeights = LossWeights()
    lossWeights.intersectionCount = 20
    lossWeights.outOfBoardPathCount = 30
    lossWeights.outOfBoardLength = 40
    lossWeights.totalPathLength = 0.5
    lossWeights.segmentsCount = 0.5
    return LossCalculator(lossWeights)


def immediatelyCall(algorithm: GeneticAlgorithm):
    return algorithm.algorithm()


def runTournamentSizeTests():
    size = 1000
    selectors = [TournamentSelector(150), TournamentSelector(350), TournamentSelector(500)]
    crossoverThreshold = 0.2
    mutationProbability = 0.1

    # internal params
    crossoverProbability = 0.2
    mutationStrength = 1
    calculator = createDefaultLossCalculator()

    subDirectory = 'tournamentSize'
    os.makedirs(os.path.join(path, subDirectory), exist_ok=True)
    file = open(os.path.join(path, subDirectory, 'results.txt'), 'w+')
    board = loadFromFile('textTests/zad1.txt')
    file.write(f'Parametry testow:\n'
               f'Rozmiar populacji: {size}\n'
               f'Prawdopodobienstwo krzyzowania: {(1 - crossoverThreshold)}\n'
               f'Prawdopodobienstwo mutacji: {(1 - mutationProbability)}\n\n'
               f'Wyniki testow:\nParametr:\tBest:\tWorst:\tAvg:\tStdDev:\n')

    for selector in selectors:
        bestSolutionLosses = []
        worstSolutionLosses = []
        file.write(f'{selector}\t')

        pool = ProcessPoolExecutor(max_workers=10)
        futures = []
        for i in range(10):
            futures.append(pool.submit(immediatelyCall,
                                       GeneticAlgorithm(board, size, calculator, selector, crossoverThreshold,
                                                        crossoverProbability,
                                                        mutationProbability, mutationStrength)))
        result = wait(futures, return_when=ALL_COMPLETED)
        for index, value in enumerate(result[0]):
            (best, worst, _, image) = value.result()
            bestSolutionLosses.append(best)
            worstSolutionLosses.append(worst)
            image.save(os.path.join(path, subDirectory, f'{selector}-test-{index}.png'))
            image.close()
        best = min(bestSolutionLosses)
        worst = max(worstSolutionLosses)
        avg = statistics.mean(bestSolutionLosses)
        stdDev = statistics.stdev(bestSolutionLosses)
        file.write(f'{best}\t{worst}\t{avg}\t{stdDev}\n')
    file.close()


def runPopulationSizeTests():
    sizes = [300, 500, 800, 1000]
    selector = TournamentSelector(150)
    crossoverThreshold = 0.2
    mutationProbability = 0.1

    # internal params
    crossoverProbability = 0.2
    mutationStrength = 1
    calculator = createDefaultLossCalculator()

    board = loadFromFile('textTests/zad1.txt')

    os.makedirs(os.path.join(path, 'populationSize'), exist_ok=True)

    file = open(os.path.join(path, 'populationSize', 'results.txt'), 'w+')
    file.write(f'Parametry testow:\n'
               f'Selektor: {selector}\n'
               f'Prawdopodobienstwo krzyzowania: {(1 - crossoverThreshold)}\n'
               f'Prawdopodobienstwo mutacji: {(1 - mutationProbability)}\n\n'
               f'Wyniki testow:\nParametr:\tBest:\tWorst:\tAvg:\tStdDev:\n')
    for size in sizes:
        bestSolutionLosses = []
        worstSolutionLosses = []
        file.write(f'rozmiar = {size}\t')

        pool = ProcessPoolExecutor(max_workers=10)
        futures = []
        for i in range(10):
            futures.append(pool.submit(immediatelyCall,
                                       GeneticAlgorithm(board, size, calculator, selector, crossoverThreshold,
                                                        crossoverProbability,
                                                        mutationProbability, mutationStrength)))
        result = wait(futures, return_when=ALL_COMPLETED)
        for index, value in enumerate(result[0]):
            (best, worst, _, image) = value.result()
            bestSolutionLosses.append(best)
            worstSolutionLosses.append(worst)
            image.save(os.path.join(path, 'populationSize', f'size-{size}-test-{index}.png'))
            image.close()
        best = min(bestSolutionLosses)
        worst = max(worstSolutionLosses)
        avg = statistics.mean(bestSolutionLosses)
        stdDev = statistics.stdev(bestSolutionLosses)
        file.write(f'{best}\t{worst}\t{avg}\t{stdDev}\n')
    file.close()


def runTests():
    runTournamentSizeTests()
