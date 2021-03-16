from random import choice
from tkinter import Tk, Canvas

from pcbBoard import Board
from populationEntity import PopulationEntity, Direction


def getRandomColor() -> str:
    return "#" + ''.join([choice('0123456789ABCDEF') for _ in range(6)])


def visualize(entity: PopulationEntity, board: Board):
    window = Tk()

    (windowWidth, windowHeight) = (800, 800)

    window.geometry(f"{windowWidth}x{windowHeight}")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    (cnvWidth, cnvHeight) = (windowWidth - 100, windowHeight - 100)
    canvas = Canvas(window, bg="#FFFFFF", width=cnvWidth, height=cnvHeight)
    canvas.grid(row=0, column=0)

    (tileWidth, tileHeight) = ((cnvWidth - 50) / board.width, (cnvWidth - 50) / board.height)
    for x in range(board.width + 1):
        for y in range(board.height + 1):
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight
            canvas.create_oval(startX - 1, startY - 1, startX + 1, startY + 1)

    for path in entity.paths:
        color = getRandomColor()
        pointWidth = 6
        startingPoint = path.startingPoint
        (x, y) = startingPoint
        for index, segment in enumerate(path.segments):
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight

            if index == 0:
                canvas.create_oval(startX - pointWidth, startY - pointWidth, startX + pointWidth, startY + pointWidth,
                                   fill=color)

            if segment.isHorizontal():
                distance = segment.distance if segment.direction == Direction.RIGHT else -segment.distance
                canvas.create_line(startX, startY, startX + (tileWidth * distance), startY, fill=color, width=3)
                x += distance
            else:
                distance = segment.distance if segment.direction == Direction.DOWN else -segment.distance
                canvas.create_line(startX, startY, startX, startY + (tileHeight * distance), fill=color, width=3)
                y += distance

            if index == len(path.segments) - 1:
                endX = 25 + x * tileWidth
                endY = 25 + y * tileHeight
                canvas.create_oval(endX - pointWidth, endY - pointWidth, endX + pointWidth, endY + pointWidth,
                                   fill=color)

    window.mainloop()
