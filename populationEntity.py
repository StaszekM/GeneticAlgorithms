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

    def getCopy(self):
        return Segment(self.direction, self.distance)


class Path:
    def __init__(self):
        self.segments: List[Segment] = []
        self.startingPoint: Point = (0, 0)

    def __str__(self):
        return f"Path, starting at ({self.startingPoint[0]}, {self.startingPoint[1]}): " + ", ".join(
            [str(segment) for segment in self.segments])

    def getCopy(self):
        result = Path()
        result.startingPoint = self.startingPoint
        for segment in self.segments:
            result.segments.append(segment.getCopy())

        return result

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
                prevSegmentBalance = prevSegment.distance \
                    if prevSegment.direction == plusDirection else -prevSegment.distance
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

    def getCopy(self):
        result = PopulationEntity()
        for path in self.paths:
            result.paths.append(path.getCopy())
        return result

    def mutate(self, probability: float, strength: int):
        random = Random()
        if random.random() >= probability:
            pathIndex = random.randint(0, len(self.paths) - 1)
            segmentIndex = random.randint(0, len(self.paths[pathIndex].segments) - 1)
            self.paths[pathIndex].mutateSegment(segmentIndex, strength)


def crossover(entity1: PopulationEntity, entity2: PopulationEntity, p: float) -> PopulationEntity:
    if len(entity1.paths) != len(entity2.paths):
        raise ValueError(
            f"Trying to crossover entities that don't have the same number of paths "
            f"({len(entity1.paths)} and {len(entity2.paths)})")

    result = PopulationEntity()
    random = Random()

    for index in range(len(entity1.paths)):
        if random.random() >= p:
            result.paths.append(entity1.paths[index].getCopy())
        else:
            result.paths.append(entity2.paths[index].getCopy())
    return result


