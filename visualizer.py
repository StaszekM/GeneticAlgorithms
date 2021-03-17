from random import randint
from typing import Tuple

from pcbBoard import Board
from populationEntity import PopulationEntity, Direction

from PIL import Image, ImageDraw


def getRandomColor() -> Tuple[int, int, int]:
    return randint(0, 255), randint(0, 255), randint(0, 255)


def visualize(entity: PopulationEntity, board: Board, filePath: str):
    (windowWidth, windowHeight) = (800, 800)

    (cnvWidth, cnvHeight) = (windowWidth - 100, windowHeight - 100)

    resultImage = Image.new('RGB', (cnvWidth, cnvHeight), (255, 255, 255))
    draw = ImageDraw.Draw(resultImage)

    (tileWidth, tileHeight) = ((cnvWidth - 50) / board.width, (cnvWidth - 50) / board.height)
    for x in range(board.width + 1):
        for y in range(board.height + 1):
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight
            draw.ellipse([startX - 1, startY - 1, startX + 1, startY + 1], fill=(0, 0, 0))

    for path in entity.paths:
        color = getRandomColor()
        pointWidth = 6
        startingPoint = path.startingPoint
        (x, y) = startingPoint
        for index, segment in enumerate(path.segments):
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight

            if index == 0:
                draw.ellipse([startX - pointWidth, startY - pointWidth, startX + pointWidth, startY + pointWidth],
                             fill=color)

            if segment.isHorizontal():
                distance = segment.distance if segment.direction == Direction.RIGHT else -segment.distance
                draw.line([startX, startY, startX + (tileWidth * distance), startY],
                          fill=color, width=3)
                x += distance
            else:
                distance = segment.distance if segment.direction == Direction.DOWN else -segment.distance
                draw.line([startX, startY, startX, startY + (tileHeight * distance)],
                          fill=color, width=3)
                y += distance

            if index == len(path.segments) - 1:
                endX = 25 + x * tileWidth
                endY = 25 + y * tileHeight
                draw.ellipse([endX - pointWidth, endY - pointWidth, endX + pointWidth, endY + pointWidth],
                             fill=color)
    resultImage.save(filePath)
    resultImage.close()
