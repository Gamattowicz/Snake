import pygame
import sys
from menu import ACTIVE_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, SIDE_FONT

BLOCK_COLOR = (41, 100, 138)
GRID_COLOR = (70, 72, 102)


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

    def draw_grid(self, surface):
        for line in range(self.rows + 1):
            pygame.draw.line(surface, GRID_COLOR, (self.start_x, self.start_y + line * self.square_size),
                                                  (self.start_x + self.rows * self.square_size,
                                                   self.start_y + line * self.square_size), 3)
        for line in range(self.columns + 1):
            pygame.draw.line(surface, GRID_COLOR, (self.start_x + line * self.square_size, self.start_y),
                                                  (self.start_x + line * self.square_size,
                                                   self.start_y + self.columns * self.square_size), 3)

    def draw_name(self, surface, player, board, main):
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
            surface.fill(BACKGROUND_COLOR)

            lost_text = SIDE_FONT.render('YOU LOST!', True, TEXT_COLOR)
            surface.blit(lost_text, (self.screen_width / 2 - lost_text.get_width() / 2, self.screen_height / 10))

            input_text = SIDE_FONT.render('Enter your name:', True, TEXT_COLOR)
            surface.blit(input_text, (self.screen_width / 2 - input_text.get_width() / 2, self.screen_height / 4 + 50))

            block = SIDE_FONT.render(player.name, True, TEXT_COLOR)
            rect = block.get_rect()
            rect.center = surface.get_rect().center
            surface.blit(block, rect)
            pygame.display.update()

        if player.score > 0:
            player.save_score(player.format_timer)
        board.draw_lost_text(surface, player, main)

    def draw_lost_text(self, surface, player, main):
        lost = True

        while lost:
            surface.fill(BACKGROUND_COLOR)

            retry_text = SIDE_FONT.render('Do you want to play again?', True, TEXT_COLOR)
            surface.blit(retry_text, (self.screen_width / 2 - retry_text.get_width() / 2, self.screen_height / 5))

            retry_options = [('YES', 150), ('NO', - 150)]
            for i, v in enumerate(retry_options, start=1):
                if i == self.active:
                    label = SIDE_FONT.render(v[0], True, ACTIVE_COLOR)
                else:
                    label = SIDE_FONT.render(v[0], True, TEXT_COLOR)
                surface.blit(label, (self.screen_width / 2 - label.get_width() / 2 - v[1], self.screen_height / 3 + 100))
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

