import pygame
import sys

# SIZE OF SCREEN =
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')
pygame.init()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()