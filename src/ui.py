import os

from src.controller import GameController, NotEnoughShips
from src.validation import CoordinateInvalid


class ConsoleUI:
    def __init__(self, gameController):
        self.gameController: GameController = gameController
        self.stage = 1
        self.commands1 = {
            "ship": self.addShip,
            "start": self.startGame
        }
        self.commands2 = {
            "attack": self.attack,
            "cheat": self.cheat
        }

    def run(self):
        self.showBoard()
        while self.stage != 3:
            line = input("> ")
            line = line.strip().split(" ")
            command = line[0]
            arguments = line[1:]
            if command == "exit":
                break
            try:
                if self.stage == 1:
                    self.commands1[command](arguments)
                elif self.stage == 2:
                    self.commands2[command](arguments)
            except KeyError:
                print("Command invalid")
            except CoordinateInvalid:
                print("The given coordinates are invalid!")
            except NotEnoughShips:
                print("You need to place two ships before starting the game!")
        if self.stage == 3:
            input("Game Over. Press Enter to exit")

    def addShip(self, arguments: str):
        if len(arguments) != 1:
            raise CoordinateInvalid()
        self.gameController.addShip(arguments[0].upper(), 1)
        self.showBoard()

    def showBoard(self):
        os.system("cls")
        board = self.gameController.showBoard(1, 1)
        print("Player board\n" + board)

    def startGame(self, arguments):
        self.gameController.startGame()
        self.stage = 2
        self.turn = 1
        self.showBoards()

    def attack(self, arguments: str):
        if len(arguments) != 1:
            raise CoordinateInvalid()

        gameWon, output = self.gameController.attack(arguments[0].upper(), 1)
        self.showBoards()
        print(output)
        if gameWon:
            self.stage = 3
            return
        input("Press Enter to let the computer attack")

        gameWon, output = self.gameController.attack("", 2)
        self.showBoards()
        print(output)
        if gameWon:
            self.stage = 3
            return

    def showBoards(self):
        os.system("cls")
        boards = self.gameController.showBoards(1)
        print("         Player board                  Targeting board    ")
        print(boards)

    def cheat(self, arguments):
        board = self.gameController.showBoard(2, 1)
        print("Computer board\n" + board)