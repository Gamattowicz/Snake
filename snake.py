import pygame
import sys


SNAKE_COLOR = (22, 255, 189)
BLOCK_COLOR = (41, 100, 138)


class Snake:
    def __init__(self, color):
        self.color = color
        self.loc_x = 10
        self.loc_y = 10
        self.move_x = 1
        self.move_y = 0
        self.len_body = 1
        self.body = []

    def place_snake(self, surface, board, apple, collision_check, player, main):
        if board.squares[self.loc_y][self.loc_x] == apple.color:
            self.len_body += 1
            player.score += round(10 + player.speed * player.mode)
            if player.mode == 2:
                player.speed += 1
            apple.place_apple(board, apple.generate_location(board, SNAKE_COLOR))
        collision_check(surface, board, player, main)
        board.squares[self.loc_y][self.loc_x] = self.color
        self.body.append((self.loc_y, self.loc_x))
        if len(self.body) > self.len_body:
            board.squares[self.body[0][0]][self.body[0][1]] = BLOCK_COLOR
            del self.body[0]

    def move(self, surface, active, player, width, height, main, main_menu, get_leaderboard, pause):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(surface, active, width, height, main, main_menu, get_leaderboard, player)
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

    def collision_check(self, surface, board, player, main):
        if board.squares[self.loc_y][self.loc_x] == self.color:
            board.draw_name(surface, player, board, main)

