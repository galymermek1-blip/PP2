import pygame
import os
from datetime import datetime


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        self.width, self.height = self.screen.get_size()
        self.center = (self.width // 2, self.height // 2)

        current_dir = os.path.dirname(__file__)

        hand_path = os.path.join(current_dir, "images", "mickey_hand.png")
        head_path = os.path.join(current_dir, "images", "mickey_head.jpg")

        self.hand_image = pygame.image.load(hand_path).convert_alpha()
        self.head_image = pygame.image.load(head_path).convert()

        self.head_image = pygame.transform.scale(self.head_image, (500, 450))
        self.hand_image = pygame.transform.scale(self.hand_image, (160, 160))

        # точка (можешь менять)
        self.pivot = (self.center[0], self.center[1] + 60)

    def draw_background(self):
        self.screen.fill((255, 255, 255))
        head_rect = self.head_image.get_rect(center=self.center)
        self.screen.blit(self.head_image, head_rect)

    def draw_hand(self, image, angle):
        rotated_image = pygame.transform.rotate(image, -angle)

        rect = rotated_image.get_rect(center=self.pivot)

        self.screen.blit(rotated_image, rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_background()

            now = datetime.now()
            minutes = now.minute
            seconds = now.second

            minute_angle = minutes * 6 - 90
            second_angle = seconds * 6 - 90

            minute_hand = pygame.transform.scale(self.hand_image, (130, 130))
            second_hand = pygame.transform.scale(self.hand_image, (160, 160))

            self.draw_hand(minute_hand, minute_angle)
            self.draw_hand(second_hand, second_angle)

            # красная точка
            pygame.draw.circle(self.screen, (255, 0, 0), self.pivot, 6)

            pygame.display.flip()
            self.clock.tick(60)