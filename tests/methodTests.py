from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board, loadFromFile
from populationEntity import Path, Segment, Direction, PopulationEntity
from entitySelectors import TournamentSelector
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
                            Segment(Direction.UP, 4), Segment(Direction.LEFT, 3), Segment(Direction.DOWN, 1), Segment(Direction.RIGHT, 2)]

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
    verticalLine.startingPoint = (1, 1)
    verticalLine.segments.append(Segment(Direction.UP, 5))

    horizontalLine = Path()
    horizontalLine.startingPoint = (2, 3)
    horizontalLine.segments.append(Segment(Direction.RIGHT, 6))

    trickyPath = Path()
    trickyPath.startingPoint = (4, 5)
    trickyPath.segments = [Segment(Direction.RIGHT, 1), Segment(Direction.UP, 1), Segment(Direction.RIGHT, 3),
                           Segment(Direction.DOWN, 1)]

    print(f"Vertical line before: {verticalLine}")
    verticalLine.mutateSegment(0, 2)
    print(f"Vertical line after: {verticalLine}")

    print(f"Horizontal line before: {horizontalLine}")
    horizontalLine.mutateSegment(0, 2)
    print(f"Vertical line after: {horizontalLine}")

    print(f"Tricky path before: {trickyPath}")
    trickyPath.mutateSegment(2, 2)
    print(f"Tricky path after: {trickyPath}")


def testGenRandomPopulation():
    board: Board = loadFromFile('textTests/zad1.txt')
    population = generateRandomPopulation(10, board)
    for index, element in enumerate(population):
        visualize(element, board, f'C:\\Users\\Staszek\\PycharmProjects\\GeneticAlgorithmsPCB\\testresults\\randpop-{index}.png')
    print()


def testTournamentSelector():
    board: Board = loadFromFile('textTests/zad0.txt')
    population = generateRandomPopulation(1000, board)
    selector: TournamentSelector = TournamentSelector(500)

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
