import pygame
import sys
import random

# SIZE OF SCREEN =
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')
pygame.init()


class Board:
    def __init__(self, columns, rows, square_size, width, height):
        self.columns = columns
        self.rows = rows
        self.square_size = square_size
        self.squares = [[(0, 0, 0) for column in range(self.columns)] for row in range(self.rows)]
        self.start_x = (width - (columns * square_size)) // 2
        self.start_y = (height - (rows * square_size)) // 2
        self.screen_width = width
        self.screen_height = height

    def draw_title(self, text, surface):
        title_font = pygame.font.SysFont('arial', 60)
        title_text = title_font.render(text, True, (255, 255, 255))
        surface.blit(title_text, (self.screen_width // 2 - title_text.get_width()/2, self.start_y // 2 - title_text.get_height()/2))

    def draw_sides_text(self, surface, player):
        score_font = pygame.font.SysFont('arial', 40)
        score_text = score_font.render(f'Score: {player.score}', True, (255, 255, 255))
        surface.blit(score_text, (self.start_x // 2 - score_text.get_width() / 2,
                                  self.screen_height // 4 - score_text.get_height() / 2))

        max_score_text = score_font.render('Max score: 0', True, (255, 255, 255))
        surface.blit(max_score_text, (self.screen_width - self.start_x // 2 - max_score_text.get_width() / 2,
                                      self.screen_height // 4 - max_score_text.get_height() / 2))

        timer_text = score_font.render(f'Timer: {player.timer}', True, (255, 255, 255))
        surface.blit(timer_text, (self.start_x // 2 - timer_text.get_width() / 2,
                                  self.screen_height // 4 - timer_text.get_height() / 2 + 100))

    def create_squares(self, surface):
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                pygame.draw.rect(surface, self.squares[i][j], (self.start_x + j * self.square_size,
                                                               self.start_y + i * self.square_size,
                                                               self.square_size, self.square_size), 0)

    def update_board(self):
        pass

    def draw_grid(self, surface):
        for line in range(self.rows + 1):
            pygame.draw.line(surface, (125, 125, 125), (self.start_x, self.start_y + line * self.square_size),
                                                       (self.start_x + self.rows * self.square_size,
                                                        self.start_y + line * self.square_size), 3)
        for line in range(self.columns + 1):
            pygame.draw.line(surface, (125, 125, 125), (self.start_x + line * self.square_size, self.start_y),
                                                       (self.start_x + line * self.square_size,
                                                        self.start_y + self.columns * self.square_size), 3)


class Snake:
    def __init__(self, color):
        self.color = color
        self.loc_x = 10
        self.loc_y = 10
        self.move_x = 1
        self.move_y = 0
        self.len_body = 1
        self.body = []

    def place_snake(self, surface, board, apple, collision_check, player):
        if board.squares[self.loc_y][self.loc_x] == apple.color:
            self.len_body += 1
            player.score += 1
            apple.place_apple(board, apple.generate_location(board))
        collision_check(surface, board)
        board.squares[self.loc_y][self.loc_x] = self.color
        self.body.append((self.loc_y, self.loc_x))
        if len(self.body) > self.len_body:
            board.squares[self.body[0][0]][self.body[0][1]] = (0, 0, 0)
            del self.body[0]

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.move_x != 1:
                    if event.key == pygame.K_LEFT:
                        self.move_x = -1
                        self.move_y = 0
                if self.move_x != -1:
                    if event.key == pygame.K_RIGHT:
                        self.move_x = 1
                        self.move_y = 0
                if self.move_y != 1:
                    if event.key == pygame.K_UP:
                        self.move_y = -1
                        self.move_x = 0
                if self.move_y != -1:
                    if event.key == pygame.K_DOWN:
                        self.move_y = 1
                        self.move_x = 0

    def collision_check(self, surface, board):
        run = False
        if board.squares[self.loc_y][self.loc_x] == self.color:
            run = True
        while run:
            WIN.fill((0, 0, 0))
            lost_text = pygame.font.SysFont('arial', 95).render('YOU LOST!', True, (255, 255, 255))
            surface.blit(lost_text, (100, 100))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


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


class Player:
    def __init__(self):
        self.score = 0
        self.timer = 0


def main():
    board = Board(20, 20, 30, WIDTH, HEIGHT)
    apple = Apple((255, 0, 0))
    apple.place_apple(board, apple.generate_location(board))
    snake = Snake((0, 255, 0))
    player = Player()
    clock = pygame.time.Clock()
    time = 0
    run = True
    while run:
        WIN.fill((0, 0, 0))
        board.draw_title('SNAKE', WIN)
        board.create_squares(WIN)
        board.draw_grid(WIN)
        time += clock.tick(10)
        print(time)
        if time / 1000 > 1:
            time = 0
            player.timer += 1
        snake.place_snake(WIN, board, apple, snake.collision_check, player)
        snake.loc_x += snake.move_x
        snake.loc_y += snake.move_y
        if snake.loc_x == 20:
            snake.loc_x = 0
        elif snake.loc_x < 0:
            snake.loc_x = 19
        elif snake.loc_y == 20:
            snake.loc_y = 0
        elif snake.loc_y < 0:
            snake.loc_y = 19
        snake.move()
        board.draw_sides_text(WIN, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()