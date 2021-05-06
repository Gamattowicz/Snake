import random


class Apple:
    def __init__(self, color):
        self.color = color

    @staticmethod
    def generate_location(board):
        squares = [[(j, i) for j in range(board.columns)] for i in range(board.rows)]
        squares = [j for sub in squares for j in sub]

        for i in range(10):
            location = random.choice(squares)
            if board.squares[location[0]][location[1]] != (0, 255, 0):
                return location

    def place_apple(self, board, location):
        board.squares[location[0]][location[1]] = self.color