from pcbBoard import Board
from populationEntity import PopulationEntity, Direction

from typing import List, Tuple


class LossWeights:
    def __init__(self):
        self.outOfBoardPathCount = 1
        self.outOfBoardLength = 1
        self.intersectionCount = 1
        self.totalPathLength = 1
        self.segmentsCount = 1


CalculatorResult = Tuple[float, bool, Tuple[int, int, int, int, int]]


class LossCalculator:
    def __init__(self, lossWeights: LossWeights):
        self.lossWeights = lossWeights

    @staticmethod
    def __safeAdd(tupleKey: Tuple[int, int], dictionary: dict):
        if tupleKey in dictionary:
            dictionary[tupleKey] += 1
        else:
            dictionary[tupleKey] = 1

    def calculateLoss(self, populationEntity: PopulationEntity, board: Board) -> CalculatorResult:
        """Calculates loss for a specific Entity on a specific Board, using this Calculator's punishment weights,
        returns float - total loss, boolean - true if path is valid (no intersections or paths outside of the board),
        a tuple of ints containing (total paths length, number of segments, number of paths out of the board,
        total length of segments out of the board, number of intersections)"""
        totalPathLength = 0
        segmentsCount = 0
        outOfBoardPathCount = 0
        outOfBoardLength = 0
        numberOfIntersections = 0

        # map of path locations on the board, 0 means no path on the specific intersection,
        # 1 means 1 path, 2 means 2 paths...
        pathLocationsDict = {}

        for path in populationEntity.paths:
            (x, y) = path.startingPoint
            self.__safeAdd((x, y), pathLocationsDict)

            pathOutOfBoard = False
            isCurrentlyOutside = False

            for segment in path.segments:
                segmentsCount += 1
                totalPathLength += segment.distance

                # update location matrix based on segment direction and current point
                if segment.direction == Direction.UP:
                    deltaX = 0
                    deltaY = -segment.distance
                    for i in range(1, segment.distance + 1):
                        if 0 <= y - i <= board.height and 0 <= x <= board.width:
                            self.__safeAdd((x, y - i), pathLocationsDict)
                elif segment.direction == Direction.RIGHT:
                    deltaX = segment.distance
                    deltaY = 0
                    for i in range(1, segment.distance + 1):
                        if 0 <= x + i <= board.width and 0 <= y <= board.height:
                            self.__safeAdd((x + i, y), pathLocationsDict)
                elif segment.direction == Direction.DOWN:
                    deltaX = 0
                    deltaY = segment.distance
                    for i in range(1, segment.distance + 1):
                        if 0 <= y + i <= board.height and 0 <= x <= board.width:
                            self.__safeAdd((x, y + i), pathLocationsDict)
                else:
                    deltaX = -segment.distance
                    deltaY = 0
                    for i in range(1, segment.distance + 1):
                        if 0 <= x - i <= board.width and 0 <= y <= board.height:
                            self.__safeAdd((x - i, y), pathLocationsDict)

                # check if segment goes at least partially outside of the board
                if 0 <= x + deltaX <= board.width and 0 <= y + deltaY <= board.height:
                    if isCurrentlyOutside:
                        # case 1: segment started outside and finishes inside
                        isCurrentlyOutside = False
                        if segment.isHorizontal():
                            outOfBoardLength += abs(x) if x < 0 else abs(x - board.width)
                        else:
                            outOfBoardLength += abs(y) if y < 0 else abs(y - board.height)
                else:
                    if not pathOutOfBoard:
                        pathOutOfBoard = True
                        outOfBoardPathCount += 1
                    if not isCurrentlyOutside:
                        # case 2: segment started inside and finishes outside
                        isCurrentlyOutside = True
                        if segment.isHorizontal():
                            outOfBoardLength += abs(x + deltaX) if x + deltaX < 0 else abs(x + deltaX - board.width)
                        else:
                            outOfBoardLength += abs(y + deltaY) if y + deltaY < 0 else abs(y + deltaY - board.height)
                    else:
                        # case 3: segment started outside and finishes outside
                        if segment.isHorizontal():
                            outOfBoardLength += abs(deltaX)
                        else:
                            outOfBoardLength += abs(deltaY)
                x += deltaX
                y += deltaY

        for value in pathLocationsDict.values():
            if value > 1:
                numberOfIntersections += value - 1

        isValid = numberOfIntersections == 0 and outOfBoardPathCount == 0

        return (
            totalPathLength * self.lossWeights.totalPathLength +
            segmentsCount * self.lossWeights.segmentsCount +
            outOfBoardPathCount * self.lossWeights.outOfBoardPathCount +
            outOfBoardLength * self.lossWeights.outOfBoardLength +
            numberOfIntersections * self.lossWeights.intersectionCount,
            isValid, (totalPathLength,
                      segmentsCount,
                      outOfBoardPathCount,
                      outOfBoardLength,
                      numberOfIntersections))
