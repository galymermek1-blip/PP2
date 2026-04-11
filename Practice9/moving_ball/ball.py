import pygame


class MovingBall:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.width, self.height = self.screen.get_size()

        self.radius = 25
        self.step = 5

        self.x = self.width // 2
        self.y = self.height // 2

        self.bg_color = (255, 255, 255)
        self.ball_color = (255, 0, 0)
        self.platform_color = (0, 180, 0)

        self.platform1 = pygame.Rect(120, 180, 180, 20)
        self.platform2 = pygame.Rect(500, 380, 180, 20)

    def draw(self):
        self.screen.fill(self.bg_color)

        pygame.draw.rect(self.screen, self.platform_color, self.platform1)
        pygame.draw.rect(self.screen, self.platform_color, self.platform2)

        pygame.draw.circle(self.screen, self.ball_color, (self.x, self.y), self.radius)

    def move_up(self):
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step

    def move_down(self):
        if self.y + self.step + self.radius <= self.height:
            self.y += self.step

    def move_left(self):
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step

    def move_right(self):
        if self.x + self.step + self.radius <= self.width:
            self.x += self.step

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                self.move_up()
            if pressed[pygame.K_DOWN]:
                self.move_down()
            if pressed[pygame.K_LEFT]:
                self.move_left()
            if pressed[pygame.K_RIGHT]:
                self.move_right()

            self.draw()
            pygame.display.flip()
            self.clock.tick(10)