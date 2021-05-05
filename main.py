import pygame
import sys
import random
import csv
from datetime import date
from menu import draw_menu
from leaderboard import get_leaderboard

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
        self.active = 1

    def draw_title(self, text, surface):
        title_font = pygame.font.SysFont('arial', 60)
        title_text = title_font.render(text, True, (255, 255, 255))
        surface.blit(title_text, (self.screen_width // 2 - title_text.get_width()/2, self.start_y // 2 - title_text.get_height()/2))

    def draw_sides_text(self, surface, player, format_timer, get_max_score):
        score_font = pygame.font.SysFont('arial', 40)
        score_text = score_font.render(f'Score: {player.score}', True, (255, 255, 255))
        surface.blit(score_text, (self.start_x // 2 - score_text.get_width() / 2,
                                  self.screen_height // 4 - score_text.get_height() / 2))

        max_score_text = score_font.render(f'Max score: {get_max_score() if get_max_score() else 0}', True, (255, 255, 255))
        surface.blit(max_score_text, (self.screen_width - self.start_x // 2 - max_score_text.get_width() / 2,
                                      self.screen_height // 4 - max_score_text.get_height() / 2))

        timer_text = score_font.render(f'Timer: {format_timer()}', True, (255, 255, 255))
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

    @staticmethod
    def draw_name(surface, player, board):
        draw = True
        while draw:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        player.name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        player.name = player.name[:-1]
                    elif event.key == pygame.K_RETURN or event.type == pygame.QUIT:
                        draw = False
            surface.fill((0, 0, 0))

            LOST_FONT = pygame.font.SysFont('arial', 95)
            lost_text = LOST_FONT.render('YOU LOST!', True, (255, 255, 255))
            surface.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 10))

            TITLE_FONT = pygame.font.SysFont('arial', 60)
            input_text = TITLE_FONT.render('Enter your name:', True, (255, 255, 255))
            surface.blit(input_text, (WIDTH / 2 - input_text.get_width() / 2, HEIGHT / 4 + 50))

            PREVIEW_FONT = pygame.font.SysFont('arial', 20)
            block = PREVIEW_FONT.render(player.name, True, (255, 255, 255))
            rect = block.get_rect()
            rect.center = surface.get_rect().center
            surface.blit(block, rect)
            pygame.display.update()

        if player.score > 0:
            player.save_score(player.format_timer)
        # player.restart_stats()
        board.draw_lost_text(WIN)

    def draw_lost_text(self, surface):
        lost = True

        while lost:
            surface.fill((0, 0, 0))

            TITLE_FONT = pygame.font.SysFont('arial', 60)
            retry_text = TITLE_FONT.render('Do you want to play again?', True, (255, 255, 255))
            surface.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 5))

            retry_options = [('YES', 150), ('NO', - 150)]
            for i, v in enumerate(retry_options, start=1):
                if i == self.active:
                    label = TITLE_FONT.render(v[0], True, (255, 0, 0))
                else:
                    label = TITLE_FONT.render(v[0], True, (255, 255, 255))
                surface.blit(label, (WIDTH / 2 - label.get_width() / 2 - v[1], HEIGHT / 3 + 100))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.active == 2:
                            self.active = 1
                        else:
                            self.active += 1
                    elif event.key == pygame.K_LEFT:
                        if self.active == 1:
                            self.active = 2
                        else:
                            self.active -= 1
                    elif event.key == pygame.K_RETURN:
                        if self.active == 1:
                            main()
                        elif self.active == 2:
                            pygame.quit()
                            sys.exit()


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
        collision_check(surface, board, player)
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

    def collision_check(self, surface, board, player):
        if board.squares[self.loc_y][self.loc_x] == self.color:
            board.draw_name(surface, player, board)


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
        self.name = ''

    def format_timer(self):
        mins = self.timer // 60
        formatted_mins = f'0{mins}' if mins < 10 else mins
        secs = self.timer - mins * 60
        formatted_secs = f'0{secs}' if secs < 10 else secs
        formatted_timer = f'{formatted_mins}:{formatted_secs}'

        return formatted_timer

    def save_score(self, format_timer):
        with open('scores.csv', 'a+') as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0:
                f.write('\n')
            f.write(
                f'{self.name},{str(self.score)},{format_timer()},{date.today()}')

    @staticmethod
    def get_max_score():
        rows = []
        with open('scores.csv', 'a+') as f:
            f.seek(0)
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                rows.append(int(row[1]))
        if len(rows) > 0:
            max_score = sorted(rows, reverse=True)
            return max_score[0]


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
        board.draw_sides_text(WIN, player, player.format_timer, player.get_max_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
    sys.exit()


def main_menu(surface):
    active = 1
    run = True

    while run:
        surface.fill((0, 0, 0))
        buttons = ['NEW GAME', 'LEADERBOARD', 'EXIT']
        draw_menu(surface, 'MAIN MENU', buttons, WIDTH, HEIGHT, active)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 3:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 3
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main()
                    elif active == 2:
                        get_leaderboard(surface, WIDTH, HEIGHT)
                    elif active == 3:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)