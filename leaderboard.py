import pygame
import csv
import sys
from menu import TITLE_FONT, SIDE_FONT, BACKGROUND_COLOR, TEXT_COLOR

MAIN_ROW_COLOR = (41, 100, 138)


def draw_leaderboard(surface, leaderboard, width, height):
    menu_text = TITLE_FONT.render('LEADERBOARD', True, TEXT_COLOR)
    surface.blit(menu_text, (width / 2 - menu_text.get_width() / 2, height / 2 - 350))

    width_btn = -400
    height_btn = -100
    for i, v in enumerate(leaderboard):
        for index, j in enumerate(v):
            # draw title row
            if i == 0:
                label = SIDE_FONT.render(j, True, MAIN_ROW_COLOR)
                button_x = width / 2 - label.get_width() / 2
                surface.blit(label, (button_x + width_btn, height / 3 - 100))
            else:
                # draw place of score
                if index == 0:
                    label = SIDE_FONT.render(str(i), True, TEXT_COLOR)
                    button_x = width / 2 - label.get_width() / 2
                    surface.blit(label, (button_x + width_btn, height / 3 + height_btn))
                    width_btn += 150
                # draw score and time
                label = SIDE_FONT.render(j, True, TEXT_COLOR)
                button_x = width / 2 - label.get_width() / 2
                surface.blit(label, (button_x + width_btn, height / 3 + height_btn))
            width_btn += 150
        width_btn = -400
        height_btn += 50


def get_leaderboard(surface, width, height):
    rows = [['No.', 'Name', 'Score', 'Speed level', 'Time', 'Date']]
    with open('scores.csv', 'a+') as f:
        f.seek(0)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows.append(row)
    leaderboard = [rows[0]] + sorted(rows[1:], key=lambda x: int(x[1]), reverse=True)[:10]
    high_scores = True

    while high_scores:
        surface.fill(BACKGROUND_COLOR)
        draw_leaderboard(surface, leaderboard, width, height)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    high_scores = False