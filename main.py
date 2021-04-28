import pygame
import sys

# SIZE OF SCREEN =
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')
pygame.init()


class Board(object):
    def __init__(self, columns, rows, square_size):
        self.columns = columns
        self.rows = rows
        self.square_size = square_size
        self.squares = [[(0, 0, 0) for row in range(self.columns)] for columns in range(self.rows)]

    def update_board(self):
        pass

    def draw_grid(self, surface):
        print(len(self.squares))
        for line in range(self.rows):
            pygame.draw.line(surface, (125, 125, 125), (0, 0 + line * self.square_size), (0 + self.rows * self.square_size,
                                                                                          0 + line * self.square_size), 3)
        for line in range(self.columns):
            pygame.draw.line(surface, (125, 125, 125), (0 + line * self.square_size, 0), (0 + line * self.square_size,
                                                                                          0 + self.columns * self.square_size), 3)


class Snake(object):
    def __init__(self):
        pass


def main():
    board = Board(20, 20, 30)
    board.draw_grid(WIN)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()