from randomSearch import RandomSearch
from pcbBoard import loadFromFile
from tests.methodTests import testLossCalculator
from visualizer import visualize


def tryRandomSearch():
    board = loadFromFile('tests/zad0.5.txt')
    result = RandomSearch.RandomSearch(board, 10, printOutput=True)
    if result is None:
        print("Could not find a solution")
    else:
        print("Found a solution:")
        visualize(result, board)
        for path in result.paths:
            print(path)


if __name__ == "__main__":
    tryRandomSearch()
    # testLossCalculator()
    pass
