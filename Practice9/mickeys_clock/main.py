import pygame
from clock import MickeyClock

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mickey Clock")

app = MickeyClock(screen)
app.run()

pygame.quit()