import pygame
from player import MusicPlayer
def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("Music Player")

    app = MusicPlayer(screen)
    app.run()

    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()