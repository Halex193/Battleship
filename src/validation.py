from src.model import Board

class CoordinateInvalid(RuntimeError):
    pass


class Validator:

    @staticmethod
    def validateCoordinate(coordinate):
        """
        Checks if the given coordinate is valid
        :param coordinate: A string of type C1L1
        :raises CoordinateInvalid: If the given coordinate is invalid
        """
        if len(coordinate) != 2:
            raise CoordinateInvalid()

        if coordinate[0] not in Board.columns:
            raise CoordinateInvalid()
        try:
            row = coordinate[1]
            row = int(row)
            if row < 0 or row > 5:
                raise CoordinateInvalid()
        except ValueError:
            raise CoordinateInvalid()

    @staticmethod
    def validateShip(coordinate1, coordinate2, coordinate3):
        if coordinate1[0] == coordinate2[0]:
            if coordinate3[0] != coordinate1[0]:
                raise CoordinateInvalid()
            distance = int(coordinate2[1]) - int(coordinate1[1])
            if int(coordinate3[1]) - int(coordinate2[1]) != distance:
                raise CoordinateInvalid()

        elif coordinate1[1] == coordinate2[1]:
            if coordinate3[1] != coordinate1[1]:
                raise CoordinateInvalid()
            distance = Board.columns.index(coordinate2[0]) - Board.columns.index(coordinate1[0])
            if Board.columns.index(coordinate3[0]) - Board.columns.index(coordinate2[0]) != distance:
                raise CoordinateInvalid()
        else:
            raise CoordinateInvalid()
