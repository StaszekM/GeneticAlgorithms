from tkinter import Tk, Canvas

from pcbBoard import Board
from populationEntity import PopulationEntity, Direction


def visualize(entity: PopulationEntity, board: Board):
    window = Tk()

    (windowWidth, windowHeight) = (500, 500)

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

    for pointPair in board.pointsToConnect:
        (startPoint, endPoint) = (pointPair[0], pointPair[1])
        startX = 25 + startPoint[0] * tileWidth
        startY = 25 + startPoint[1] * tileHeight
        endX = 25 + endPoint[0] * tileHeight
        endY = 25 + endPoint[1] * tileHeight

        pointWidth = 3
        canvas.create_oval(startX - pointWidth, startY - pointWidth, startX + pointWidth, startY + pointWidth)
        canvas.create_oval(endX - pointWidth, endY - pointWidth, endX + pointWidth, endY + pointWidth)

    for path in entity.paths:
        startingPoint = path.startingPoint
        (x, y) = startingPoint
        for segment in path.segments:
            startX = 25 + x * tileWidth
            startY = 25 + y * tileHeight
            if segment.isHorizontal():
                distance = segment.distance if segment.direction == Direction.RIGHT else -segment.distance
                canvas.create_line(startX, startY, startX + (tileWidth * distance), startY, fill="#FF0000")
                x += distance
            else:
                distance = segment.distance if segment.direction == Direction.DOWN else -segment.distance
                canvas.create_line(startX, startY, startX, startY + (tileWidth * distance), fill="#FF0000")
                y += distance

    window.mainloop()
