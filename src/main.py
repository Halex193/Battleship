# Udrea Horațiu 917
import ui, controller, repository

shipRepository = repository.ShipRepository()
boardRepository = repository.BoardRepository()
gameController = controller.GameController(boardRepository, shipRepository)
consoleUI = ui.ConsoleUI(gameController)

if __name__ == '__main__':
    consoleUI.run()
