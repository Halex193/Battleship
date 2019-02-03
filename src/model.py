class Ship:
    def __init__(self, coordinate1, coordinate2, coordinate3):
        self.coordinate3 = coordinate3
        self.coordinate2 = coordinate2
        self.coordinate1 = coordinate1
        self.coordinates = [coordinate1, coordinate2, coordinate3]


class Board:
    dimension = 6
    columns = ['A', 'B', 'C', 'D', 'E', 'F']
    def __init__(self):
        self.board = {}

        for i in Board.columns:
            self.board[i] = {}
            for j in range(Board.dimension):
                self.board[i][str(j)] = "."

    def markAtCoordinate(self, coordinate: str, mark):
        self.board[coordinate[0]][coordinate[1]] = mark

    def getMark(self, coordinate: str):
        return self.board[coordinate[0]][coordinate[1]]

    def countShipMarks(self):
        count = 0
        for i in Board.columns:
            for j in range(Board.dimension):
                if self.board[i][str(j)] == "+":
                    count += 1
        return count