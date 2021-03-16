from random import Random
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

    if distanceX == 0:
        direction = Direction.DOWN if distanceY > 0 else Direction.UP
        resultPath.segments.append(Segment(direction.DOWN, abs(distanceY)))
        resultPath.mutateSegment(0, 1)
        return resultPath

    if distanceY == 0:
        direction = Direction.RIGHT if distanceX > 0 else Direction.LEFT
        resultPath.segments.append(Segment(direction, abs(distanceX)))
        resultPath.mutateSegment(0, 1)
        return resultPath

    (x, y) = (startingPoint[0], startingPoint[1])

    goTowardsEndProbability = 0.1

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

            distance = random.randint(1, ceil(abs(x - endingPoint[0]) * 1.5))
            x += distance if direction == Direction.RIGHT else -distance
        else:
            if y <= 0 or y >= board.height:
                direction = Direction.DOWN if y <= 0 else Direction.UP
            else:
                preferredDirection = Direction.UP if y > endingPoint[1] else Direction.DOWN
                oppositeDirection = Direction.DOWN if y > endingPoint[1] else Direction.UP

                direction = preferredDirection if random.random() > goTowardsEndProbability else oppositeDirection

            distance = random.randint(1, ceil(abs(y - endingPoint[1]) * 1.5))
            y += distance if direction == Direction.DOWN else -distance

        horizontal = not horizontal

        resultPath.segments.append(Segment(direction, distance))

    return resultPath
