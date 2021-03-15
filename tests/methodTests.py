from lossCalculator import LossWeights, LossCalculator
from pcbBoard import Board, loadFromFile
from populationEntity import Path, Segment, Direction, PopulationEntity


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
                            Segment(Direction.UP, 3), Segment(Direction.LEFT, 1)]

    sampleEntity = PopulationEntity()
    sampleEntity.paths.append(samplePath)
    sampleEntity.paths.append(samplePath2)

    weights = LossWeights()
    p = LossCalculator(weights)

    # EXPECTED:
    # totalPathLength = 30
    # segmentsCount = 16
    # outOfBoardPathCount = 1
    # outOfBoardLength = 7
    # numberOfIntersections = 2
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
    board: Board = loadFromFile('zad0.txt')
    population = board.generateRandomPopulation(10)
    print()


def testFixing():
    samplePath = Path()
    samplePath.segments = [Segment(Direction.LEFT, 2), Segment(Direction.LEFT, 1), Segment(Direction.RIGHT, 2),
                           Segment(Direction.DOWN, 1), Segment(Direction.UP, 2), Segment(Direction.UP, 2),
                           Segment(Direction.RIGHT, 2), Segment(Direction.LEFT, 2), Segment(Direction.RIGHT, 1),
                           Segment(Direction.UP, 1), Segment(Direction.LEFT, 1)]

    print(f"Sample path before: {samplePath}")
    samplePath.fixPath()
    print(f"Sample path after: {samplePath}")