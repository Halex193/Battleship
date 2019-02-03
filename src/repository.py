from src.model import Ship, Board


class ShipRepository(object):
    def __init__(self):
        self.collection = {1:[], 2:[]}
        self.shipIndex = {1: 0, 2: 0}

    def addShip(self, ship: Ship, player):
        self.collection[player].append(ship)

    def length(self, player):
        return len(self.collection[player])

    def putShip(self, ship, index, player):
        self.collection[player][index] = ship
        self.shipIndex[player] = 0 if self.shipIndex[player] == 1 else 1

    def getShip(self, index, player):
        return self.collection[player][index]

class BoardRepository(object):
    def __init__(self):
        self.boards = {
            # player 1, 2
            1: {
                # boards 1 -> ship board
                # 2-> attack board
                1: Board(),
                2: Board()
            },
            2: {
                # boards 1 -> ship board
                # 2-> attack board
                1: Board(),
                2: Board()
            }
        }

    def getBoard(self, player, board) -> Board:
        return self.boards[player][board]