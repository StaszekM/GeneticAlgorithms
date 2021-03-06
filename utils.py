from random import Random, choice
from typing import List
from pcbBoard import Board
from populationEntity import Path, Direction, Segment, PopulationEntity
from utilTypes import Point
from math import ceil


def generateRandomPopulation(size: int, board: Board) -> List[PopulationEntity]:
    """Generate random population of size size that connects corresponding points on this Board"""
    if size <= 0:
        raise ValueError(f"Trying to generate population with size {size}")

    result: List[PopulationEntity] = []
    for i in range(size):
        entity: PopulationEntity = PopulationEntity()
        for pointPair in board.pointsToConnect:
            (startPoint, endPoint) = pointPair
            entity.paths.append(joinTwoPoints(startPoint, endPoint, board))
        result.append(entity)

    return result


def joinTwoPoints(startingPoint: Point, endingPoint: Point, board: Board) -> Path:
    """Joins two points with a random path and returns it."""
    distanceX = endingPoint[0] - startingPoint[0]
    distanceY = endingPoint[1] - startingPoint[1]

    if distanceX == 0 and distanceY == 0:
        raise ValueError("Starting and ending points are overlapping")

    random: Random = Random()

    resultPath: Path = Path()
    resultPath.startingPoint = (startingPoint[0], startingPoint[1])

    goTowardsEndProbability = 0.3

    (x, y) = (startingPoint[0], startingPoint[1])
    if distanceX == 0:
        if random.random() > 0.25:
            direction = choice([Direction.LEFT, Direction.RIGHT])
            distance = random.randint(1, 3 * board.width // 2)
            resultPath.segments.append(Segment(direction, distance))
            x += distance if direction == direction.RIGHT else -distance

            horizontal = False
        else:
            direction = Direction.DOWN if distanceY > 0 else Direction.UP
            resultPath.segments.append(Segment(direction.DOWN, abs(distanceY)))
            resultPath.mutateSegment(0, 1, board)
            return resultPath
    elif distanceY == 0:
        if random.random() > 0.25:
            direction = choice([Direction.UP, Direction.DOWN])
            distance = random.randint(1, 3 * board.height // 2)
            resultPath.segments.append(Segment(direction, distance))
            y += distance if direction == direction.DOWN else -distance
            horizontal = True
        else:
            direction = Direction.RIGHT if distanceX > 0 else Direction.LEFT
            resultPath.segments.append(Segment(direction, abs(distanceX)))
            resultPath.mutateSegment(0, 1, board)
            return resultPath
    else:
        horizontal: bool = random.random() >= 0.5

    while x != endingPoint[0] or y != endingPoint[1]:
        if x == endingPoint[0] or y == endingPoint[1]:
            if x == endingPoint[0]:
                yDiff = endingPoint[1] - y
                direction = Direction.DOWN if yDiff > 0 else Direction.UP
                distance = abs(yDiff)
                y += yDiff
            else:
                xDiff = endingPoint[0] - x
                direction = Direction.RIGHT if xDiff > 0 else Direction.LEFT
                distance = abs(xDiff)
                x += xDiff
        elif horizontal:
            if x <= 0 or x >= board.width:
                direction = Direction.RIGHT if x <= 0 else Direction.LEFT
            else:
                preferredDirection = Direction.LEFT if x > endingPoint[0] else Direction.RIGHT
                oppositeDirection = Direction.RIGHT if x > endingPoint[0] else Direction.LEFT

                direction = preferredDirection if random.random() > goTowardsEndProbability else oppositeDirection

            distance = random.randint(1, ceil(abs(x - endingPoint[0]) * 3))
            x += distance if direction == Direction.RIGHT else -distance
        else:
            if y <= 0 or y >= board.height:
                direction = Direction.DOWN if y <= 0 else Direction.UP
            else:
                preferredDirection = Direction.UP if y > endingPoint[1] else Direction.DOWN
                oppositeDirection = Direction.DOWN if y > endingPoint[1] else Direction.UP

                direction = preferredDirection if random.random() > goTowardsEndProbability else oppositeDirection

            distance = random.randint(1, ceil(abs(y - endingPoint[1]) * 3))
            y += distance if direction == Direction.DOWN else -distance

        horizontal = not horizontal

        resultPath.segments.append(Segment(direction, distance))

    return resultPath
