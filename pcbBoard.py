from typing import List

from utilTypes import Point

from populationEntity import PopulationEntity, joinTwoPoints


class Board:
    def __init__(self, width: int, height: int):
        self.pointsToConnect: List[(Point, Point)] = []
        self.width: int = width
        self.height: int = height

    def addPointPair(self, startingPoint: Point, endingPoint: Point):
        """Add point pair to be connected to this Board"""
        (startX, startY) = startingPoint
        (endX, endY) = endingPoint

        if startX < 0 or startX > self.width or startY < 0 or startY > self.height:
            raise ValueError(f"Tried to add points ({startX}, {startY}), ({endX}, {endY}) "
                             f"to a board of size {self.width}x{self.height}")

        self.pointsToConnect.append(((startX, startY), (endX, endY)))

    def generateRandomPopulation(self, size: int) -> List[PopulationEntity]:
        """Generate random population of size size that connects corresponding points on this Board"""
        if size <= 0:
            raise ValueError(f"Trying to generate population with size {size}")

        result: List[PopulationEntity] = []
        for i in range(size):
            entity: PopulationEntity = PopulationEntity()
            for pointPair in self.pointsToConnect:
                (startPoint, endPoint) = pointPair
                entity.paths.append(joinTwoPoints(startPoint, endPoint))
                result.append(entity)

        return result


def loadFromFile(filePath: str) -> Board:
    """Reads a formatted file from a path and returns a board based on it"""
    file = open(filePath)

    lines = file.readlines()
    [width, height] = [int(value) for value in lines[0].strip().split(";")]

    result: Board = Board(width, height)
    for line in lines[1:]:
        [startX, startY, endX, endY] = [int(value) for value in line.strip().split(";")]
        result.addPointPair((startX, startY), (endX, endY))

    return result
