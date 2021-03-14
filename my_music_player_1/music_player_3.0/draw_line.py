import pygame
from pygame.locals import *


def DrawLine(screen):
    mycolcor = (255, 255, 255)
    start = (100, 100)
    end = (500, 400)
    width = 10
    pygame.draw.line(screen, mycolcor, start, end, width)


def main():
    pygame.init()
    pygame.display.set_caption('Draw Lines')
    screen = pygame.display.set_mode([600, 500])

    mRunning = True
    while mRunning:
        for event in pygame.event.get():
            if event.type == QUIT:
                mRunning = False
        screen.fill((0, 0, 0))
        DrawLine(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
