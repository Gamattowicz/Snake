import pygame
import sys

pygame.font.init()

TITLE_FONT = pygame.font.SysFont('arial', 60)
BUTTON_FONT = pygame.font.SysFont('arial', 25)
BACKGROUND_COLOR = (37, 39, 77)


def draw_menu_button(surface, text, row, color, width, height):
    rows_height = {
        1: 150,
        2: 100,
        3: 50,
        4: 0,
        5: -50
    }

    label = BUTTON_FONT.render(text, True, color)
    button_x = width / 2 - label.get_width() / 2
    surface.blit(label, (button_x, height / 2 - rows_height[row]))


def draw_menu(surface, menu_title, buttons, width, height, active):
    menu_text = TITLE_FONT.render(menu_title, True, (255, 255, 255))
    surface.blit(menu_text, (width / 2 - menu_text.get_width() / 2, height / 2 - 250))

    for i, v in enumerate(buttons, start=1):
        if i == active:
            draw_menu_button(surface, v, i, (255, 0, 0), width, height)
        else:
            draw_menu_button(surface, v, i, (255, 255, 255), width, height)


def pause(win, active, width, height, main, main_menu, get_leaderboard, player):
    buttons = ['RESUME', 'RESTART', 'MAIN MENU', 'LEADERBOARD', 'EXIT']
    paused = True

    while paused:
        win.fill(BACKGROUND_COLOR)
        draw_menu(win, 'PAUSE', buttons, width, height, active)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_DOWN:
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
                        paused = False
                    elif active == 2:
                        player.restart_stats()
                        main(player)
                    elif active == 3:
                        main_menu(win)
                    elif active == 4:
                        get_leaderboard(win, width, height)
                    elif active == 5:
                        pygame.quit()
                        sys.exit()

