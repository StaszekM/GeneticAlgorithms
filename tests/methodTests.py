from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board, loadFromFile
from populationEntity import Path, Segment, Direction, PopulationEntity, crossover
from entitySelectors import TournamentSelector, RouletteSelector
from utils import generateRandomPopulation
from visualizer import visualize


def testLossCalculator():
    board: Board = Board(6, 6)
    board.addPointPair((1, 3), (5, 3))
    board.addPointPair((3, 1), (3, 3))

    samplePath = Path()
    samplePath.startingPoint = (1, 3)
    samplePath.segments = [Segment(Direction.LEFT, 2), Segment(Direction.DOWN, 1), Segment(Direction.RIGHT, 2),
                           Segment(Direction.DOWN, 1), Segment(Direction.RIGHT, 2), Segment(Direction.DOWN, 2),
                           Segment(Direction.RIGHT, 2), Segment(Direction.UP, 3), Segment(Direction.RIGHT, 1),
                           Segment(Direction.UP, 1), Segment(Direction.LEFT, 1)]

    samplePath2 = Path()
    samplePath2.startingPoint = (3, 1)
    samplePath2.segments = [Segment(Direction.LEFT, 1), Segment(Direction.DOWN, 5), Segment(Direction.RIGHT, 2),
                            Segment(Direction.UP, 4), Segment(Direction.LEFT, 3), Segment(Direction.DOWN, 1),
                            Segment(Direction.RIGHT, 2)]

    samplePath3 = Path()
    samplePath3.startingPoint = (1, 1)
    samplePath3.segments = [Segment(Direction.RIGHT, 1), Segment(Direction.DOWN, 3), Segment(Direction.RIGHT, 1)]

    sampleEntity = PopulationEntity()
    sampleEntity.paths.append(samplePath)
    sampleEntity.paths.append(samplePath2)
    sampleEntity.paths.append(samplePath3)

    weights = LossWeights()
    p = LossCalculator(weights)

    # EXPECTED:
    # totalPathLength = 41
    # segmentsCount = 21
    # outOfBoardPathCount = 1
    # outOfBoardLength = 7
    # numberOfIntersections = 9
    print(p.calculateLoss(sampleEntity, board))


def testMutatingSegments():
    verticalLine = Path()
    verticalLine.startingPoint = (13, 13)
    verticalLine.segments.append(Segment(Direction.UP, 5))

    horizontalLine = Path()
    horizontalLine.startingPoint = (2, 2)
    horizontalLine.segments.append(Segment(Direction.RIGHT, 6))

    trickyPath = Path()
    trickyPath.startingPoint = (4, 5)
    trickyPath.segments = [Segment(Direction.RIGHT, 1), Segment(Direction.UP, 1), Segment(Direction.RIGHT, 3),
                           Segment(Direction.DOWN, 1)]

    entity = PopulationEntity()
    entity.paths = [verticalLine, horizontalLine, trickyPath]

    board = Board(16, 16)
    visualize(entity, board,
              'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\testmutating-before.png')

    verticalLine.mutateSegment(0, 1)
    horizontalLine.mutateSegment(0, 1)
    trickyPath.mutateSegment(2, 1)

    visualize(entity, board,
              'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\testmutating-after.png')


def testGenRandomPopulation():
    board: Board = loadFromFile('textTests/zad1.txt')
    population = generateRandomPopulation(10, board)
    for index, element in enumerate(population):
        visualize(element, board,
                  f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\randpop-{index}.png')
    print()


def testTournamentSelector():
    board: Board = loadFromFile('textTests/zad0.txt')
    population = generateRandomPopulation(1000, board)
    selector: TournamentSelector = TournamentSelector(500)

    calculator: LossCalculator = LossCalculator(LossWeights())
    popWithLoss = [(entity, calculator.calculateLoss(entity, board)) for entity in population]
    selector.select(popWithLoss, board)


def testRouletteSelector():
    board: Board = loadFromFile('textTests/zad0.txt')
    population = generateRandomPopulation(10, board)
    selector: RouletteSelector = RouletteSelector()

    calculator: LossCalculator = LossCalculator(LossWeights())
    popWithLoss = [(entity, calculator.calculateLoss(entity, board)) for entity in population]
    selector.select(popWithLoss, board)


def testFixing():
    samplePath = Path()
    samplePath.segments = [Segment(Direction.LEFT, 2), Segment(Direction.LEFT, 1), Segment(Direction.RIGHT, 2),
                           Segment(Direction.DOWN, 1), Segment(Direction.UP, 2), Segment(Direction.UP, 2),
                           Segment(Direction.RIGHT, 2), Segment(Direction.LEFT, 2), Segment(Direction.RIGHT, 1),
                           Segment(Direction.UP, 1), Segment(Direction.LEFT, 1)]

    print(f"Sample path before: {samplePath}")
    samplePath.fixPath()
    print(f"Sample path after: {samplePath}")


def testCrossover():
    board = Board(16, 16)
    verticalLine = Path()
    verticalLine.startingPoint = (13, 13)
    verticalLine.segments.append(Segment(Direction.UP, 5))

    horizontalLine = Path()
    horizontalLine.startingPoint = (2, 2)
    horizontalLine.segments.append(Segment(Direction.RIGHT, 6))

    entity = PopulationEntity()
    entity.paths = [verticalLine, horizontalLine]

    verticalLine.mutateSegment(0, 1)
    horizontalLine.mutateSegment(0, 1)

    visualize(entity, board,
              'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\crossover-entity1.png')

    verticalLine2 = Path()
    verticalLine2.startingPoint = (13, 13)
    verticalLine2.segments.append(Segment(Direction.UP, 5))

    horizontalLine2 = Path()
    horizontalLine2.startingPoint = (2, 2)
    horizontalLine2.segments.append(Segment(Direction.RIGHT, 6))

    entity2 = PopulationEntity()
    entity2.paths = [verticalLine2, horizontalLine2]

    visualize(entity2, board,
              'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\crossover-entity2.png')

    resultEntity = crossover(entity, entity2, 0.5)

    visualize(resultEntity, board,
              'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\crossover-child.png')
