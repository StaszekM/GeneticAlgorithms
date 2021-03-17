from pcbBoard import Board
from populationEntity import PopulationEntity, Direction

from PIL import Image, ImageDraw

colors = [(194, 150, 203), (135, 72, 55), (123, 11, 8), (98, 136, 196), (81, 108, 194), (174, 185, 206), (141, 134, 6),
          (221, 237, 147), (224, 63, 43), (12, 63, 31), (57, 66, 42), (234, 55, 213), (132, 76, 73), (102, 19, 209),
          (83, 35, 185), (250, 99, 245), (14, 163, 46), (123, 193, 5), (208, 197, 249), (88, 148, 74), (42, 76, 177),
          (73, 67, 6), (143, 98, 253), (195, 105, 124), (9, 37, 136), (60, 64, 191), (98, 89, 141), (214, 235, 238),
          (68, 254, 42), (13, 236, 44), (31, 83, 11), (154, 76, 27), (102, 81, 106), (103, 48, 205), (74, 122, 111),
          (154, 206, 127), (45, 208, 133), (230, 198, 207), (203, 23, 19), (216, 82, 156), (117, 65, 186),
          (109, 14, 129), (118, 227, 78), (130, 189, 86), (54, 44, 176), (73, 194, 167), (223, 101, 204),
          (255, 18, 168), (15, 5, 193), (173, 246, 147), (209, 193, 54), (140, 58, 106), (123, 159, 168), (76, 83, 149),
          (28, 41, 124), (117, 174, 31), (20, 219, 212), (108, 166, 40), (108, 41, 181), (216, 14, 116),
          (201, 159, 205), (191, 180, 134), (236, 13, 7), (222, 60, 44), (150, 96, 94), (56, 84, 250), (68, 188, 216),
          (242, 20, 231), (153, 20, 89), (179, 168, 53), (208, 171, 60), (42, 87, 77), (78, 4, 199), (194, 156, 47),
          (161, 161, 180), (195, 155, 4), (102, 163, 73), (10, 59, 107), (133, 63, 27), (210, 237, 250), (146, 92, 63),
          (68, 27, 252), (212, 118, 76), (236, 207, 172), (173, 69, 39), (52, 143, 60), (4, 152, 146), (211, 180, 243),
          (65, 45, 160), (133, 81, 52), (97, 248, 42), (84, 66, 170), (47, 229, 70), (52, 251, 135), (184, 180, 218),
          (61, 98, 29), (17, 31, 204), (173, 67, 139), (194, 232, 203), (207, 135, 225)]


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

    for pathIndex, path in enumerate(entity.paths):
        color = colors[pathIndex % len(colors)]
        pointWidth = 6
        startingPoint = path.startingPoint
        (x, y) = startingPoint
        for segmentIndex, segment in enumerate(path.segments):
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight

            if segmentIndex == 0:
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

            if segmentIndex == len(path.segments) - 1:
                endX = 25 + x * tileWidth
                endY = 25 + y * tileHeight
                draw.ellipse([endX - pointWidth, endY - pointWidth, endX + pointWidth, endY + pointWidth],
                             fill=color)
    resultImage.save(filePath)
    resultImage.close()
