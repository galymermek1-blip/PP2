import pygame
from ball import MovingBall


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Moving Ball")

    game = MovingBall(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
