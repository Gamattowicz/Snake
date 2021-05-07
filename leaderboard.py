import pygame
import csv
import sys
from menu import TITLE_FONT, SIDE_FONT


def draw_leaderboard(win, leaderboard, width, height):
    menu_text = TITLE_FONT.render('LEADERBOARD', True, (255, 255, 255))
    win.blit(menu_text, (width / 2 - menu_text.get_width() / 2, height / 2 - 350))

    width_btn = -400
    height_btn = -100
    for i, v in enumerate(leaderboard):
        for index, j in enumerate(v):
            # draw title row
            if i == 0:
                label = SIDE_FONT.render(j, True, (255, 255, 255))
                button_x = width / 2 - label.get_width() / 2
                win.blit(label, (button_x + width_btn, height / 3 - 100))
            else:
                # draw place of score
                if index == 0:
                    label = SIDE_FONT.render(str(i), True, (255, 255, 255))
                    button_x = width / 2 - label.get_width() / 2
                    win.blit(label, (button_x + width_btn, height / 3 + height_btn))
                    width_btn += 150
                # draw score and time
                label = SIDE_FONT.render(j, True, (255, 255, 255))
                button_x = width / 2 - label.get_width() / 2
                win.blit(label, (button_x + width_btn, height / 3 + height_btn))
            width_btn += 150
        width_btn = -400
        height_btn += 50


def get_leaderboard(win, width, height):
    rows = [['No.', 'Name', 'Score', 'Speed level', 'Time', 'Date']]
    with open('scores.csv', 'a+') as f:
        f.seek(0)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows.append(row)
    try:
        leaderboard = [rows[0]] + sorted(rows[1:], key=lambda x: int(x[1]), reverse=True)[:10]
    except:
        leaderboard = [rows[0]]

    high_scores = True

    while high_scores:
        win.fill((0, 0, 0))
        draw_leaderboard(win, leaderboard, width, height)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    high_scores = False