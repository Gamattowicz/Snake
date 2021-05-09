import pygame
import sys
from menu import draw_menu, pause, BACKGROUND_COLOR
from leaderboard import get_leaderboard
from apple import Apple
from player import Player
from board import Board

# SIZE OF SCREEN =
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')
pygame.init()
BLOCK_COLOR = (41, 100, 138)
APPLE_COLOR = (240, 112, 161)
SNAKE_COLOR = (22, 255, 189)


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
            board.draw_name(surface, player, board, main)


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