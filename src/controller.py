import random

from texttable import Texttable

from src.model import Ship, Board
from src.repository import ShipRepository, BoardRepository
from src.validation import Validator, CoordinateInvalid


class NotEnoughShips(RuntimeError):
    pass


class GameController:
    textTableDecorator = Texttable.BORDER

    def __init__(self, boardRepository, shipRepository):
        self.shipRepository: ShipRepository = shipRepository
        self.boardRepository: BoardRepository = boardRepository

    def startGame(self):
        if self.shipRepository.length(1) != 2:
            raise NotEnoughShips()

        self.placeRandomShip()
        self.placeRandomShip()

    def placeRandomShip(self):
        while True:
            coordinates = self.generateRandomCoordinates()
            try:
                self.addShip(coordinates, 2)
                break
            except CoordinateInvalid:
                pass

    @staticmethod
    def generateRandomCoordinates() -> str:
        try:
            coordinate = [random.randint(0, Board.dimension - 1), random.randint(0, Board.dimension - 1)]
            result = [Board.columns[coordinate[0]], str(coordinate[1])]
            change = random.choice([-1, 1])
            if random.randint(0, 100) < 50:
                # x axis
                result += [Board.columns[coordinate[0] + change], str(coordinate[1])]
                result += [Board.columns[coordinate[0] + 2 * change], str(coordinate[1])]
            else:
                # y axis
                result += [Board.columns[coordinate[0]], str(coordinate[1] + change)]
                result += [Board.columns[coordinate[0]], str(coordinate[1] + 2 * change)]
            return ''.join(result)

        except IndexError:
            return ""

    def addShip(self, coordinates, player: int):
        """
        Adds a ship to the game for the specified player at the given coordinates.
        The rest of the board is unmodified
        If all the ships are places, subsequent calls to this function replace the ships that already exist
        :param coordinates: The coordinates of the ship squares in the form C1L1C2L2C3L3
        :param player: The player that adds the ship
        :raises CoordinateInvalid: If the given string do not represent coordinates or
        the coordinates are out of the board or
        the ship intersects with another ship
        In case an exception is thrown, the board remains unmodified
        """
        if len(coordinates) != 6:
            raise CoordinateInvalid()

        coordinate1 = coordinates[0:2]
        coordinate2 = coordinates[2:4]
        coordinate3 = coordinates[4:6]

        shipCoordinates = [coordinate1, coordinate2, coordinate3]

        Validator.validateCoordinate(coordinate1)
        Validator.validateCoordinate(coordinate2)
        Validator.validateCoordinate(coordinate3)
        Validator.validateShip(coordinate1, coordinate2, coordinate3)

        board = self.boardRepository.getBoard(player, 1)

        bonusShip = None
        if self.shipRepository.length(player) == 2:
            # remove ship to be replaced
            bonusShip = self.shipRepository.getShip(self.shipRepository.shipIndex[player], player)
            for coordinate in bonusShip.coordinates:
                board.markAtCoordinate(coordinate, ".")

        for coordinate in shipCoordinates:
            if board.getMark(coordinate) != ".":
                if bonusShip is not None:
                    #  put the bonus ship back
                    for bonusShipCoordinates in bonusShip.coordinates:
                        board.markAtCoordinate(bonusShipCoordinates, "+")

                raise CoordinateInvalid()

        for coordinate in shipCoordinates:
            board.markAtCoordinate(coordinate, "+")

        ship = Ship(coordinate1, coordinate2, coordinate3)

        if self.shipRepository.length(player) != 2:
            self.shipRepository.addShip(ship, player)
        else:
            self.shipRepository.putShip(ship, self.shipRepository.shipIndex[player], player)

    def attack(self, coordinate, player):

        if player == 1:
            if len(coordinate) != 2:
                raise CoordinateInvalid()
            Validator.validateCoordinate(coordinate)
            playerCaption = "Player"
            otherPlayer = 2

        else:
            coordinate = random.choice(Board.columns) + str(random.randint(0, Board.dimension - 1))
            playerCaption = "Computer"
            otherPlayer = 1

        gameWon = False
        enemyBoard = self.boardRepository.getBoard(otherPlayer, 1)
        targetBoard = self.boardRepository.getBoard(player, 2)
        if enemyBoard.getMark(coordinate) == "+":
            output = "%s hits!" % playerCaption
            targetBoard.markAtCoordinate(coordinate, "X")
            enemyBoard.markAtCoordinate(coordinate, "X")
            if enemyBoard.countShipMarks() == 0:
                gameWon = True
                output = "%s wins!" % playerCaption
        else:
            output = "%s misses!" % playerCaption
            targetBoard.markAtCoordinate(coordinate, "O")
            enemyBoard.markAtCoordinate(coordinate, "O")

        return gameWon, output

    def showBoard(self, player, board):
        table = Texttable()
        table.set_deco(GameController.textTableDecorator)
        board = self.boardRepository.getBoard(player, board)
        table.add_row([""] + Board.columns)
        for rowNumber in range(Board.dimension):
            rowString = str(rowNumber)
            line = [rowString]
            for column in Board.columns:
                line.append(board.getMark(column + rowString))
            table.add_row(line)

        return table.draw()

    def showBoards(self, player):
        table = Texttable()
        table.set_deco(GameController.textTableDecorator)
        mainBoard = self.boardRepository.getBoard(player, 1)
        targetingBoard = self.boardRepository.getBoard(player, 2)
        table.add_row([""] + Board.columns + [""]*2 + Board.columns)

        for rowNumber in range(Board.dimension):
            rowString = str(rowNumber)
            line = [rowString]

            for column in Board.columns:
                line.append(mainBoard.getMark(column + rowString))

            line.append("")
            line.append(rowString)

            for column in Board.columns:
                line.append(targetingBoard.getMark(column + rowString))
            table.add_row(line)

        return table.draw()
