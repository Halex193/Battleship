from unittest import TestCase

from src.controller import GameController
from src.repository import ShipRepository, BoardRepository
from src.validation import CoordinateInvalid, Validator


class TestBattleShips(TestCase):
    def setUp(self):
        self.shipRepository = ShipRepository()
        self.boardRepository = BoardRepository()
        self.gameController = GameController(self.boardRepository, self.shipRepository)

    def testAddShip(self):
        board = self.boardRepository.getBoard(1, 1)
        self.assertEqual(board.getMark("A1"), ".")
        self.assertEqual(board.getMark("A2"), ".")
        self.assertEqual(board.getMark("A3"), ".")

        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("test", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("A1A2", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("BBBBBB", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("A1A2A9", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("I8I9I7", 1)
        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("a1a2a3", 1)

        self.gameController.addShip("A1A2A3", 1)
        self.assertEqual(board.getMark("A1"), "+")
        self.assertEqual(board.getMark("A2"), "+")
        self.assertEqual(board.getMark("A3"), "+")
        self.assertEqual(board.getMark("B1"), ".")

        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("A1A2A3", 1)

        with self.assertRaises(CoordinateInvalid):
            self.gameController.addShip("A1B1C1", 1)

        self.assertEqual(board.getMark("A1"), "+")
        self.assertEqual(board.getMark("A2"), "+")
        self.assertEqual(board.getMark("A3"), "+")
        self.assertEqual(board.getMark("B1"), ".")

        self.gameController.addShip("B1B2B3", 1)
        self.assertEqual(board.getMark("B1"), "+")
        self.assertEqual(board.getMark("B2"), "+")
        self.assertEqual(board.getMark("B3"), "+")

        self.gameController.addShip("A2A3A4", 1)
        self.assertEqual(board.getMark("A1"), ".")
        self.assertEqual(board.getMark("A2"), "+")
        self.assertEqual(board.getMark("A3"), "+")
        self.assertEqual(board.getMark("A4"), "+")

        self.gameController.addShip("B3B4B5", 1)
        self.assertEqual(board.getMark("B1"), ".")
        self.assertEqual(board.getMark("B2"), ".")
        self.assertEqual(board.getMark("B3"), "+")
        self.assertEqual(board.getMark("B4"), "+")
        self.assertEqual(board.getMark("B5"), "+")

    def testCoordinateValidation(self):
        Validator.validateCoordinate("A1")
        Validator.validateCoordinate("B5")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateCoordinate("a0")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateCoordinate("f6")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateCoordinate("123")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateCoordinate("r4")

    def testShipValidatoin(self):
        Validator.validateShip("A1", "A2", "A3")
        Validator.validateShip("B0", "B1", "B2")
        Validator.validateShip("A1", "B1", "C1")
        Validator.validateShip("D2", "E2", "F2")

        with self.assertRaises(CoordinateInvalid):
            Validator.validateShip("D1", "E2", "F2")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateShip("A1", "A5", "A3")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateShip("D1", "D2", "F2")
        with self.assertRaises(CoordinateInvalid):
            Validator.validateShip("A1", "B2", "C1")