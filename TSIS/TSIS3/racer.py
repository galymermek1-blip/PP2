import pygame
import random
import os
import time
import sys
from pygame.locals import *
from persistence import load_settings, save_score

pygame.init()
pygame.mixer.init()

FPS = 60
WIDTH, HEIGHT = 400, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (0, 200, 0)
BLUE = (0, 80, 255)
YELLOW = (255, 220, 0)
GRAY = (45, 45, 45)
ORANGE = (255, 140, 0)
PURPLE = (160, 60, 255)

font_small = pygame.font.SysFont("Verdana", 18)
font_medium = pygame.font.SysFont("Verdana", 26)
font_large = pygame.font.SysFont("Verdana", 42)

LANES = [80, 160, 240, 320]
FINISH_DISTANCE = 3000

CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW
}

DIFFICULTY_SPEED = {
    "easy": 4,
    "medium": 5,
    "hard": 7
}


def load_image(filename, size=None, fallback_color=WHITE):
    try:
        image = pygame.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:
        surface = pygame.Surface(size if size else (50, 50), pygame.SRCALPHA)
        surface.fill(fallback_color)
        return surface


def load_sounds():
    sounds = {"crash": None, "coin": None, "background": False}

    try:
        crash_path = os.path.join(SOUNDS_DIR, "crash.wav")
        if os.path.exists(crash_path):
            sounds["crash"] = pygame.mixer.Sound(crash_path)
    except:
        pass

    try:
        coin_path = os.path.join(SOUNDS_DIR, "coin.wav")
        if os.path.exists(coin_path):
            sounds["coin"] = pygame.mixer.Sound(coin_path)
    except:
        pass

    try:
        for ext in [".mp3", ".wav", ".ogg"]:
            path = os.path.join(SOUNDS_DIR, "background" + ext)
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                sounds["background"] = True
                break
    except:
        pass

    return sounds


def load_background():
    try:
        bg = pygame.image.load(os.path.join(IMAGES_DIR, "AnimatedStreet.png"))
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(GRAY)
        for y in range(0, HEIGHT, 60):
            pygame.draw.rect(bg, WHITE, (WIDTH // 2 - 5, y, 10, 35))
        return bg


def draw_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)


def draw_button(text, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    draw_text(text, font_small, WHITE, rect.centerx, rect.centery)
    return rect


def input_name_screen():
    name = ""

    while True:
        screen.fill(BLACK)
        draw_text("Enter your name", font_medium, WHITE, WIDTH // 2, 190)
        draw_text(name + "|", font_medium, YELLOW, WIDTH // 2, 250)
        draw_text("Press ENTER to start", font_small, WHITE, WIDTH // 2, 330)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return name if name.strip() else "Player"
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12:
                    name += event.unicode


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()

        color = CAR_COLORS.get(settings["car_color"], BLUE)
        self.image = load_image("Player.png", (50, 80), color)

        if not os.path.exists(os.path.join(IMAGES_DIR, "Player.png")):
            self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.center = (LANES[1], 520)

        self.speed = 6
        self.active_power = None
        self.power_end_time = 0
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()

        speed = self.speed
        if self.active_power == "nitro":
            speed = 11

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed

        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed

        if self.active_power == "nitro" and time.time() > self.power_end_time:
            self.active_power = None

    def activate_power(self, power):
        if self.active_power is not None:
            return

        if power == "nitro":
            self.active_power = "nitro"
            self.power_end_time = time.time() + 4

        elif power == "shield":
            self.active_power = "shield"
            self.shield = True

        elif power == "repair":
            self.active_power = "repair"
            self.power_end_time = time.time() + 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, player_x):
        super().__init__()
        self.image = load_image("Enemy.png", (50, 80), RED)
        self.rect = self.image.get_rect()

        lane = random.choice(LANES)
        while abs(lane - player_x) < 40:
            lane = random.choice(LANES)

        self.rect.center = (lane, random.randint(-180, -80))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.weight = random.choice([1, 2, 3])
        self.image = load_image("Coin.png", (28, 28), YELLOW)

        if not os.path.exists(os.path.join(IMAGES_DIR, "Coin.png")):
            self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (14, 14), 14)
            pygame.draw.circle(self.image, ORANGE, (14, 14), 10)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-180, -40))

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player_x):
        super().__init__()

        self.kind = random.choice(["barrier", "oil", "pothole"])
        self.image = pygame.Surface((55, 35), pygame.SRCALPHA)

        if self.kind == "barrier":
            self.image.fill(ORANGE)
        elif self.kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (0, 5, 55, 25))
        else:
            pygame.draw.ellipse(self.image, (80, 80, 80), (0, 0, 55, 35))

        self.rect = self.image.get_rect()

        lane = random.choice(LANES)
        while abs(lane - player_x) < 40:
            lane = random.choice(LANES)

        self.rect.center = (lane, random.randint(-220, -80))

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.kind = random.choice(["nitro", "shield", "repair"])
        self.spawn_time = time.time()

        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)

        if self.kind == "nitro":
            pygame.draw.circle(self.image, GREEN, (17, 17), 17)
            txt = font_small.render("N", True, BLACK)
        elif self.kind == "shield":
            pygame.draw.circle(self.image, BLUE, (17, 17), 17)
            txt = font_small.render("S", True, WHITE)
        else:
            pygame.draw.circle(self.image, WHITE, (17, 17), 17)
            txt = font_small.render("R", True, RED)

        self.image.blit(txt, txt.get_rect(center=(17, 17)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-220, -80))

    def move(self, speed):
        self.rect.y += speed

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > 6:
            self.kill()


class RoadEvent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.kind = random.choice(["speed_bump", "nitro_lane", "moving_barrier"])
        self.image = pygame.Surface((80, 25), pygame.SRCALPHA)

        if self.kind == "speed_bump":
            self.image.fill(YELLOW)
        elif self.kind == "nitro_lane":
            self.image.fill(GREEN)
        else:
            self.image.fill(PURPLE)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-250, -100))
        self.direction = random.choice([-2, 2])

    def move(self, speed):
        self.rect.y += speed

        if self.kind == "moving_barrier":
            self.rect.x += self.direction
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


def game_over_screen(score, coins, distance):
    while True:
        screen.fill(RED)

        draw_text("GAME OVER", font_large, WHITE, WIDTH // 2, 100)
        draw_text(f"Score: {score}", font_medium, WHITE, WIDTH // 2, 190)
        draw_text(f"Coins: {coins}", font_medium, YELLOW, WIDTH // 2, 230)
        draw_text(f"Distance: {distance}", font_medium, WHITE, WIDTH // 2, 270)

        retry_btn = draw_button("Retry", 100, 370, 200, 50, GREEN)
        menu_btn = draw_button("Main Menu", 100, 440, 200, 50, BLUE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"


def run_game():
    settings = load_settings()
    sounds = load_sounds()
    background = load_background()

    base_speed = DIFFICULTY_SPEED[settings["difficulty"]]
    speed = base_speed

    score = 0
    coins_collected = 0
    distance = 0
    power_bonus_score = 0

    player_name = input_name_screen()
    player = Player(settings)

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    road_events = pygame.sprite.Group()

    all_sprites.add(player)

    enemy_timer = 0
    coin_timer = 0
    obstacle_timer = 0
    power_timer = 0
    road_event_timer = 0

    if settings["sound"] and sounds["background"]:
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        distance += 1

        if distance >= FINISH_DISTANCE:
            running = False

        speed = base_speed + distance // 700

        enemy_timer += 1
        coin_timer += 1
        obstacle_timer += 1
        power_timer += 1
        road_event_timer += 1

        spawn_limit = max(25, 70 - distance // 80)

        if enemy_timer > spawn_limit:
            enemy_timer = 0
            enemy = Enemy(speed, player.rect.centerx)
            enemies.add(enemy)
            all_sprites.add(enemy)

        if coin_timer > 45:
            coin_timer = 0
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        if obstacle_timer > max(45, 110 - distance // 60):
            obstacle_timer = 0
            obstacle = Obstacle(player.rect.centerx)
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        if power_timer > 320:
            power_timer = 0
            power = PowerUp()
            powerups.add(power)
            all_sprites.add(power)

        if road_event_timer > 250:
            road_event_timer = 0
            road_event = RoadEvent()
            road_events.add(road_event)
            all_sprites.add(road_event)

        screen.blit(background, (0, 0))

        player.move()

        for enemy in enemies:
            enemy.move()

        for coin in coins:
            coin.move(speed)

        for obstacle in obstacles:
            obstacle.move(speed)

        for power in powerups:
            power.move(speed)

        for event_obj in road_events:
            event_obj.move(speed)

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            coins_collected += coin.weight
            score += coin.weight * 10

            if settings["sound"] and sounds["coin"]:
                sounds["coin"].play()

        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for power in collected_powerups:
            if player.active_power is None:
                player.activate_power(power.kind)
                power_bonus_score += 20
                score += 20

        road_hits = pygame.sprite.spritecollide(player, road_events, True)
        for event_obj in road_hits:
            if event_obj.kind == "speed_bump":
                score -= 10

            elif event_obj.kind == "nitro_lane":
                if player.active_power is None:
                    player.activate_power("nitro")
                    score += 20

            elif event_obj.kind == "moving_barrier":
                if player.shield:
                    player.shield = False
                    player.active_power = None
                else:
                    running = False

        obstacle_hits = pygame.sprite.spritecollide(player, obstacles, True)
        if obstacle_hits:
            if player.shield:
                player.shield = False
                player.active_power = None
            elif player.active_power == "repair":
                player.active_power = None
            else:
                running = False

        enemy_hit = pygame.sprite.spritecollideany(player, enemies)
        if enemy_hit:
            if player.shield:
                enemy_hit.kill()
                player.shield = False
                player.active_power = None
            else:
                if settings["sound"] and sounds["crash"]:
                    sounds["crash"].play()
                running = False

        score += 1

        all_sprites.draw(screen)

        remaining = max(0, FINISH_DISTANCE - distance)

        draw_text(f"Score: {score}", font_small, BLACK, 10, 10, center=False)
        draw_text(f"Coins: {coins_collected}", font_small, YELLOW, 10, 35, center=False)
        draw_text(f"Distance: {distance}", font_small, BLACK, 10, 60, center=False)
        draw_text(f"Left: {remaining}", font_small, BLACK, 10, 85, center=False)

        if player.active_power:
            if player.active_power == "nitro":
                left = max(0, int(player.power_end_time - time.time()))
                draw_text(f"Power: Nitro {left}s", font_small, GREEN, 210, 10, center=False)
            elif player.active_power == "shield":
                draw_text("Power: Shield", font_small, BLUE, 210, 10, center=False)
            elif player.active_power == "repair":
                draw_text("Power: Repair", font_small, WHITE, 210, 10, center=False)
        else:
            draw_text("Power: None", font_small, BLACK, 210, 10, center=False)

        pygame.display.update()
        clock.tick(FPS)

    pygame.mixer.music.stop()

    final_score = score + coins_collected * 5 + distance // 2 + power_bonus_score
    save_score(player_name, final_score, distance)

    return game_over_screen(final_score, coins_collected, distance)