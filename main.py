import pygame
import sys
import csv
from datetime import date
from menu import draw_menu, pause, ACTIVE_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, SIDE_FONT
from leaderboard import get_leaderboard
from apple import Apple

# SIZE OF SCREEN =
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')
pygame.init()
BLOCK_COLOR = (41, 100, 138)
GRID_COLOR = (70, 72, 102)
APPLE_COLOR = (240, 112, 161)
SNAKE_COLOR = (22, 255, 189)


class Board:
    def __init__(self, columns, rows, square_size, width, height):
        self.columns = columns
        self.rows = rows
        self.square_size = square_size
        self.squares = [[BLOCK_COLOR for column in range(self.columns)] for row in range(self.rows)]
        self.start_x = (width - (columns * square_size)) // 2
        self.start_y = (height - (rows * square_size)) // 2
        self.screen_width = width
        self.screen_height = height
        self.active = 1

    def draw_title(self, text, surface):
        title_text = TITLE_FONT.render(text, True, TEXT_COLOR)
        surface.blit(title_text, (self.screen_width // 2 - title_text.get_width()/2, self.start_y // 2 - title_text.get_height()/2))

    def draw_sides_text(self, surface, player, format_timer, get_max_score):
        score_text = SIDE_FONT.render(f'Score: {player.score}', True, TEXT_COLOR)
        surface.blit(score_text, (self.start_x // 2 - score_text.get_width() / 2,
                                  self.screen_height // 4 - score_text.get_height() / 2))

        max_score_text = SIDE_FONT.render(f'Max score: {get_max_score() if get_max_score() else 0}', True, TEXT_COLOR)
        surface.blit(max_score_text, (self.screen_width - self.start_x // 2 - max_score_text.get_width() / 2,
                                      self.screen_height // 4 - max_score_text.get_height() / 2))

        timer_text = SIDE_FONT.render(f'Timer: {format_timer()}', True, TEXT_COLOR)
        surface.blit(timer_text, (self.start_x // 2 - timer_text.get_width() / 2,
                                  self.screen_height // 4 - timer_text.get_height() / 2 + 100))

        speed_text = SIDE_FONT.render(f'Speed: {round(player.speed, 1)}', True, TEXT_COLOR)
        surface.blit(speed_text, (self.screen_width - self.start_x // 2 - speed_text.get_width() / 2,
                                  self.screen_height // 4 - speed_text.get_height() / 2 + 100))

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
            pygame.draw.line(surface, GRID_COLOR, (self.start_x, self.start_y + line * self.square_size),
                                                       (self.start_x + self.rows * self.square_size,
                                                        self.start_y + line * self.square_size), 3)
        for line in range(self.columns + 1):
            pygame.draw.line(surface, GRID_COLOR, (self.start_x + line * self.square_size, self.start_y),
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

            lost_text = SIDE_FONT.render('YOU LOST!', True, TEXT_COLOR)
            surface.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 10))

            input_text = SIDE_FONT.render('Enter your name:', True, TEXT_COLOR)
            surface.blit(input_text, (WIDTH / 2 - input_text.get_width() / 2, HEIGHT / 4 + 50))

            block = SIDE_FONT.render(player.name, True, TEXT_COLOR)
            rect = block.get_rect()
            rect.center = surface.get_rect().center
            surface.blit(block, rect)
            pygame.display.update()

        if player.score > 0:
            player.save_score(player.format_timer)
        board.draw_lost_text(WIN, player)

    def draw_lost_text(self, surface, player):
        lost = True

        while lost:
            surface.fill(BACKGROUND_COLOR)

            retry_text = SIDE_FONT.render('Do you want to play again?', True, TEXT_COLOR)
            surface.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 5))

            retry_options = [('YES', 150), ('NO', - 150)]
            for i, v in enumerate(retry_options, start=1):
                if i == self.active:
                    label = SIDE_FONT.render(v[0], True, ACTIVE_COLOR)
                else:
                    label = SIDE_FONT.render(v[0], True, TEXT_COLOR)
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
                            player.restart_stats()
                            main(player)
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
            player.score += round(10 + player.speed * player.mode)
            if player.mode == 2:
                player.speed += 1
            apple.place_apple(board, apple.generate_location(board, SNAKE_COLOR))
        collision_check(surface, board, player)
        board.squares[self.loc_y][self.loc_x] = self.color
        self.body.append((self.loc_y, self.loc_x))
        if len(self.body) > self.len_body:
            board.squares[self.body[0][0]][self.body[0][1]] = BLOCK_COLOR
            del self.body[0]

    def move(self, surface, active, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(surface, active, WIDTH, HEIGHT, main, main_menu, get_leaderboard, player)
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


class Player:
    def __init__(self):
        self.score = 0
        self.timer = 0
        self.name = ''
        self.speed = 1
        self.mode = 1
        self.start_speed = 1

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
                f'{self.name},{str(self.score)},{round(self.speed, 1)},{format_timer()},{date.today()}')

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

    def restart_stats(self):
        self.score = 0
        self.timer = 0
        self.name = ''
        self.speed = self.start_speed


def main(player):
    board = Board(20, 20, 30, WIDTH, HEIGHT)
    apple = Apple(APPLE_COLOR)
    apple.place_apple(board, apple.generate_location(board, SNAKE_COLOR))
    snake = Snake(SNAKE_COLOR)
    clock = pygame.time.Clock()
    time = 0
    run = True
    while run:
        WIN.fill(BACKGROUND_COLOR)
        board.draw_title('SNAKE', WIN)
        board.create_squares(WIN)
        board.draw_grid(WIN)
        time += clock.tick(8 + player.speed * 1)

        if time / 1000 > 1:
            time = 0
            if player.mode == 3:
                player.speed += 0.1
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
        snake.move(WIN, board.active, player)
        board.draw_sides_text(WIN, player, player.format_timer, player.get_max_score)
        pygame.display.update()

    pygame.display.quit()


def main_menu(surface):
    active = 1
    player = Player()
    run = True
    speeds = ['LOW', 'MEDIUM', 'HIGH']
    modes = ['ENDLESS (CONSTANT SPEED)', 'SURVIVAL (INCREASING SPEED AFTER EATING APPLE)',
             'HARDCORE (INCREASING SPEED OVER TIME)']

    while run:
        surface.fill(BACKGROUND_COLOR)
        buttons = ['NEW GAME', f'SPEED: {speeds[(player.speed // 5)]}', f'MODE: {modes[player.mode - 1]}', 'LEADERBOARD', 'EXIT']
        draw_menu(surface, 'MAIN MENU', buttons, WIDTH, HEIGHT, active)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 5:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 5
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main(player)
                    elif active == 2:
                        if player.speed == 11:
                            player.speed = 1
                            player.start_speed = 1
                        else:
                            player.speed += 5
                            player.start_speed += 5
                    elif active == 3:
                        if player.mode == 3:
                            player.mode = 1
                        else:
                            player.mode += 1
                    elif active == 4:
                        get_leaderboard(surface, WIDTH, HEIGHT)
                    elif active == 5:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)