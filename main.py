import pygame
import sys
import random

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

    def create_squares(self, surface):
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                pygame.draw.rect(surface, self.squares[i][j], (j * self.square_size, i * self.square_size,
                                                               self.square_size, self.square_size), 0)

    def update_board(self):
        pass

    def draw_grid(self, surface):
        for line in range(self.rows):
            pygame.draw.line(surface, (125, 125, 125), (0, line * self.square_size), (self.rows * self.square_size,
                                                                                        line * self.square_size), 3)
        for line in range(self.columns):
            pygame.draw.line(surface, (125, 125, 125), (line * self.square_size, 0), (line * self.square_size,
                                                                                          self.columns * self.square_size), 3)


class Snake(object):
    def __init__(self, color):
        self.color = color
        self.loc_x = 10
        self.loc_y = 10

    def place_snake(self, board):
        board.squares[self.loc_y][self.loc_x] = self.color

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.loc_x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.loc_x += 1
                elif event.key == pygame.K_UP:
                    self.loc_y -= 1
                elif event.key == pygame.K_DOWN:
                    self.loc_y += 1

    def valid_space(self):
        pass


class Apple(object):
    def __init__(self, color):
        self.color = color

    @staticmethod
    def generate_location(board):
        squares = [[(j, i) for j in range(board.columns)] for i in range(board.rows)]
        squares = [j for sub in squares for j in sub]

        location = random.choice(squares)
        return location

    def place_apple(self, board, location):
        board.squares[location[0]][location[1]] = self.color
        print(board.squares)


def main():
    board = Board(20, 20, 30)
    apple = Apple((255, 0, 0))
    apple.place_apple(board, apple.generate_location(board))
    snake = Snake((0, 255, 0))
    snake.place_snake(board)
    clock = pygame.time.Clock()
    time = 0
    run = True
    while run:
        snake.move()
        board.create_squares(WIN)
        board.draw_grid(WIN)
        time += clock.get_rawtime()
        clock.tick()
        snake.place_snake(board)

        if time / 1000 > 1:
            print(time)
            time = 0
            snake.loc_x += 1
            snake.move()
            print(snake.loc_x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()