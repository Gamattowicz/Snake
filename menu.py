import pygame

pygame.font.init()

TITLE_FONT = pygame.font.SysFont('arial', 60)
BUTTON_FONT = pygame.font.SysFont('arial', 25)


def draw_menu_button(win, text, row, color, width, height):
    rows_height = {
        1: 150,
        2: 100,
        3: 50,
        4: 0,
        5: -50
    }

    label = BUTTON_FONT.render(text, True, color)
    button_x = width / 2 - label.get_width() / 2
    win.blit(label, (button_x, height / 2 - rows_height[row]))


def draw_menu(win, menu_title, buttons, width, height, active):
    menu_text = TITLE_FONT.render(menu_title, True, (255, 255, 255))
    win.blit(menu_text, (width / 2 - menu_text.get_width() / 2, height / 2 - 250))

    for i, v in enumerate(buttons, start=1):
        if i == active:
            draw_menu_button(win, v, i, (255, 0, 0), width, height)
        else:
            draw_menu_button(win, v, i, (255, 255, 255), width, height)
