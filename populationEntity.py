from enum import Enum
from typing import List
from random import Random
from utilTypes import Point


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Segment:
    def __init__(self, direction: Direction, distance: int):
        self.direction = direction
        self.distance = distance

    def __str__(self):
        if self.direction == Direction.UP:
            direction = "up"
        elif self.direction == Direction.RIGHT:
            direction = "right"
        elif self.direction == Direction.DOWN:
            direction = "down"
        else:
            direction = "left"

        return f"({direction}, {self.distance})"

    def isHorizontal(self) -> bool:
        return self.direction in [Direction.RIGHT, Direction.LEFT]


class Path:
    def __init__(self):
        self.segments: List[Segment] = []
        self.startingPoint: Point = (0, 0)

    def __str__(self):
        return f"Path, starting at ({self.startingPoint[0]}, {self.startingPoint[1]}): " + ", ".join(
            [str(segment) for segment in self.segments])

    def fixPath(self):
        """Fixes redundant segments, e.g. two vertical segments one after another"""
        segmentsCount = len(self.segments)
        if segmentsCount < 2:
            return

        index = 1
        while index < len(self.segments):
            segmentsCount = len(self.segments)
            if segmentsCount < 2:
                return

            segment = self.segments[index]
            prevSegment = self.segments[index - 1]

            bothHorizontal = (segment.isHorizontal() and prevSegment.isHorizontal())
            bothVertical = (not segment.isHorizontal()) and (not prevSegment.isHorizontal())

            if bothHorizontal or bothVertical:
                if bothHorizontal:
                    plusDirection = Direction.RIGHT
                    minusDirection = Direction.LEFT

                else:
                    plusDirection = Direction.DOWN
                    minusDirection = Direction.UP

                segmentBalance = segment.distance if segment.direction == plusDirection else -segment.distance
                prevSegmentBalance = prevSegment.distance if prevSegment.direction == plusDirection else -prevSegment.distance
                total = segmentBalance + prevSegmentBalance

                self.segments.pop(index - 1)
                self.segments.pop(index - 1)
                if total != 0:
                    newSegment = Segment(plusDirection if total > 0 else minusDirection, abs(total))
                    self.segments.insert(index - 1, newSegment)

                index = 1
            else:
                index += 1

    def mutateSegment(self, index: int, strength: int):
        """Mutates a segment at specified index with given offset (>=1)"""
        if not (0 <= index < len(self.segments)):
            raise ValueError(f"Trying to mutate segment with index {index} in a path with "
                             f"a number of {len(self.segments)} segments")
        if strength < 1:
            raise ValueError(f"Trying to mutate a segment with strength {strength}")

        random = Random()
        matchingSegment = self.segments[index]

        # previousSegment = None if index == 0 else self.segments[index - 1]
        # nextSegment = None if index == len(self.segments) - 1 else self.segments[index + 1]

        cutStartPoint = random.randint(0, matchingSegment.distance - 1)
        cutEndPoint = random.randint(cutStartPoint + 1, matchingSegment.distance)

        replacementSegments: List[Segment] = []

        randomResult = random.random()
        if matchingSegment.isHorizontal():
            goOutDirection = Direction.UP if randomResult > 0.5 else Direction.DOWN
            goBackDirection = Direction.DOWN if goOutDirection == Direction.UP else Direction.UP
        else:
            goOutDirection = Direction.LEFT if randomResult > 0.5 else Direction.RIGHT
            goBackDirection = Direction.RIGHT if goOutDirection == Direction.LEFT else Direction.LEFT

        # build 3 to 5 segments depending on the situation
        if cutStartPoint != 0:
            replacementSegments.append(Segment(matchingSegment.direction, cutStartPoint))

        replacementSegments.append(Segment(goOutDirection, strength))
        replacementSegments.append(Segment(matchingSegment.direction, cutEndPoint - cutStartPoint))
        replacementSegments.append(Segment(goBackDirection, strength))

        if cutEndPoint != matchingSegment.distance:
            replacementSegments.append(Segment(matchingSegment.direction, matchingSegment.distance - cutEndPoint))

        self.segments.pop(index)
        for count, replacementSegment in enumerate(replacementSegments):
            self.segments.insert(index + count, replacementSegment)

        self.fixPath()


class PopulationEntity:
    def __init__(self):
        self.paths: List[Path] = []


def joinTwoPoints(startingPoint: Point, endingPoint: Point) -> Path:
    """Joins two points with a random path and returns it."""
    distanceX = endingPoint[0] - startingPoint[0]
    distanceY = endingPoint[1] - startingPoint[1]

    if distanceX == 0 and distanceY == 0:
        raise ValueError("Starting and ending points are overlapping")

    random: Random = Random()

    resultPath: Path = Path()
    resultPath.startingPoint = (startingPoint[0], startingPoint[1])

    if distanceX > 0:
        preferredDirectionX: Direction = Direction.RIGHT
    elif distanceX < 0:
        preferredDirectionX = Direction.LEFT
    else:
        direction = Direction.DOWN if distanceY > 0 else Direction.UP
        resultPath.segments.append(Segment(direction.DOWN, abs(distanceY)))
        resultPath.mutateSegment(0, 1)
        return resultPath

    if distanceY > 0:
        preferredDirectionY: Direction = Direction.DOWN
    elif distanceY < 0:
        preferredDirectionY = Direction.UP
    else:
        direction = Direction.RIGHT if distanceX > 0 else Direction.LEFT
        resultPath.segments.append(Segment(direction, abs(distanceX)))
        resultPath.mutateSegment(0, 1)
        return resultPath

    absDistanceX = abs(distanceX)
    absDistanceY = abs(distanceY)

    horizontal: bool = random.random() >= 0.5
    while absDistanceX > 0 or absDistanceY > 0:
        if absDistanceY == 0 or absDistanceX == 0:
            if absDistanceX == 0:
                direction = preferredDirectionY
                distance = absDistanceY
                absDistanceY = 0
            else:
                direction = preferredDirectionX
                distance = absDistanceX
                absDistanceX = 0
        elif horizontal:
            direction = preferredDirectionX
            distance = 1 if absDistanceX == 1 else random.randint(1, absDistanceX)
            absDistanceX = absDistanceX - distance
        else:
            direction = preferredDirectionY
            distance = 1 if absDistanceY == 1 else random.randint(1, absDistanceY)
            absDistanceY = absDistanceY - distance

        horizontal = not horizontal

        resultPath.segments.append(Segment(direction, distance))

    return resultPath
