import pygame
import sys
import os
import random
import time
from pygame.locals import *

# -------------------- INITIALIZATION --------------------
# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

# FPS controls how fast the game loop runs
FPS = 60
FramePerSec = pygame.time.Clock()

# -------------------- COLORS --------------------
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# -------------------- GAME SETTINGS --------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Enemy speed
SPEED = 5

# Score increases when enemy passes the screen
SCORE = 0

# Total collected coin value
COINS_COLLECTED = 0

# Best collected coins in current program run
HIGH_SCORE = 0

# After every N coin points, enemy speed increases
N = 10

# -------------------- FILE PATHS --------------------
# These paths allow the game to load images and sounds from folders
BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# -------------------- FONTS --------------------
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 30)

# -------------------- BACKGROUND --------------------
try:
    background = pygame.image.load(os.path.join(IMAGES_DIR, "AnimatedStreet.png"))
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    # If background image is missing, create a simple road manually
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(GREEN)

    # Draw dashed road line
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(background, WHITE, (SCREEN_WIDTH // 2 - 5, i, 10, 30))

# -------------------- DISPLAY --------------------
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Practice11 Racer")

# -------------------- SPRITE GROUPS --------------------
# Groups help update and draw many objects easily
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

P1 = None
E1 = None


class Enemy(pygame.sprite.Sprite):
    """Enemy car class. The player must avoid this car."""

    def __init__(self):
        super().__init__()

        # Try to load enemy image
        try:
            self.image = pygame.image.load(os.path.join(IMAGES_DIR, "Enemy.png"))
        except:
            # If image is missing, use a red rectangle
            self.image = pygame.Surface((50, 80))
            self.image.fill(RED)

        self.rect = self.image.get_rect()

        # Enemy appears at random x position at the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move enemy car down the screen."""
        global SCORE

        self.rect.move_ip(0, SPEED)

        # If enemy passes the screen, player gets score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    """Coin class. Coins have different weights: 1, 2 or 3."""

    def __init__(self):
        super().__init__()

        # Coin weight means how many points it gives
        self.weight = random.choice([1, 2, 3])

        try:
            self.image = pygame.image.load(os.path.join(IMAGES_DIR, "Coin.png"))
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            # If coin image is missing, draw coin manually
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

            # Different colors show different coin weights
            if self.weight == 1:
                color = YELLOW
            elif self.weight == 2:
                color = ORANGE
            else:
                color = (255, 215, 0)

            pygame.draw.circle(self.image, color, (15, 15), 15)
            pygame.draw.circle(self.image, BLACK, (15, 15), 15, 1)

        self.rect = self.image.get_rect()

        # Coin appears at random position above the screen
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-150, -30)
        )

    def move(self):
        """Move coin down the screen."""
        self.rect.move_ip(0, SPEED)

        # If coin leaves screen, remove it
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    """Player car class. Controlled with left and right arrows."""

    def __init__(self):
        super().__init__()

        try:
            self.image = pygame.image.load(os.path.join(IMAGES_DIR, "Player.png"))
        except:
            # If image is missing, use a blue rectangle
            self.image = pygame.Surface((50, 80))
            self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def move(self):
        """Move player car left and right."""
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


def load_sounds():
    """Load optional sound effects."""
    sounds = {
        "crash": None,
        "coin": None,
        "background": None
    }

    # Load crash sound
    try:
        crash_path = os.path.join(SOUNDS_DIR, "crash.wav")
        if os.path.exists(crash_path):
            sounds["crash"] = pygame.mixer.Sound(crash_path)
    except:
        pass

    # Load coin sound
    try:
        coin_path = os.path.join(SOUNDS_DIR, "coin.wav")
        if os.path.exists(coin_path):
            sounds["coin"] = pygame.mixer.Sound(coin_path)
    except:
        pass

    # Load background music
    try:
        for ext in [".mp3", ".wav", ".ogg"]:
            bg_path = os.path.join(SOUNDS_DIR, "background" + ext)
            if os.path.exists(bg_path):
                pygame.mixer.music.load(bg_path)
                sounds["background"] = "music"
                break
    except:
        pass

    return sounds


def show_game_over_screen(final_score, final_coins, high_score):
    """Show game over screen and return True if player wants to restart."""
    DISPLAYSURF.fill(RED)

    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    DISPLAYSURF.blit(game_over_text, game_over_rect)

    score_text = font_medium.render(f"Final Score: {final_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    DISPLAYSURF.blit(score_text, score_rect)

    coins_text = font_medium.render(f"Coins: {final_coins}", True, YELLOW)
    coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
    DISPLAYSURF.blit(coins_text, coins_rect)

    high_score_text = font_medium.render(f"Best Coins: {high_score}", True, GREEN)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    DISPLAYSURF.blit(high_score_text, high_score_rect)

    play_again_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 50)
    pygame.draw.rect(DISPLAYSURF, GREEN, play_again_btn)
    pygame.draw.rect(DISPLAYSURF, WHITE, play_again_btn, 2)

    play_again_text = font_medium.render("PLAY AGAIN", True, BLACK)
    DISPLAYSURF.blit(play_again_text, play_again_text.get_rect(center=play_again_btn.center))

    quit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
    pygame.draw.rect(DISPLAYSURF, BLACK, quit_btn)
    pygame.draw.rect(DISPLAYSURF, WHITE, quit_btn, 2)

    quit_text = font_medium.render("QUIT", True, WHITE)
    DISPLAYSURF.blit(quit_text, quit_text.get_rect(center=quit_btn.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == MOUSEBUTTONDOWN:
                if play_again_btn.collidepoint(event.pos):
                    return True

                if quit_btn.collidepoint(event.pos):
                    return False

            if event.type == KEYDOWN:
                if event.key == K_r:
                    return True

                if event.key == K_q or event.key == K_ESCAPE:
                    return False


def reset_game():
    """Reset all game variables for a new round."""
    global SPEED, SCORE, COINS_COLLECTED, enemies, coins, all_sprites, P1, E1

    SPEED = 5
    SCORE = 0
    COINS_COLLECTED = 0

    # Clear all old sprites
    enemies.empty()
    coins.empty()
    all_sprites.empty()

    # Create new player and enemy
    P1 = Player()
    E1 = Enemy()

    enemies.add(E1)
    all_sprites.add(P1)
    all_sprites.add(E1)

    return P1, E1


def main_game():
    """Main game function."""
    global SPEED, SCORE, COINS_COLLECTED, HIGH_SCORE, P1, E1

    sounds = load_sounds()

    # Play background music if it exists
    if sounds["background"] == "music":
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    P1, E1 = reset_game()

    # Timer for spawning coins
    COIN_SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(COIN_SPAWN, random.randint(700, 1500))

    running = True

    while running:
        # -------------------- EVENTS --------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Create new coin at random time
            if event.type == COIN_SPAWN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

                pygame.time.set_timer(COIN_SPAWN, random.randint(700, 1500))

        # -------------------- DRAW BACKGROUND --------------------
        DISPLAYSURF.blit(background, (0, 0))

        # -------------------- UI --------------------
        score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(score_text, (10, 10))

        coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, YELLOW)
        coins_rect = coins_text.get_rect()
        coins_rect.topright = (SCREEN_WIDTH - 10, 10)
        DISPLAYSURF.blit(coins_text, coins_rect)

        speed_text = font_small.render(f"Speed: {round(SPEED, 1)}", True, BLACK)
        DISPLAYSURF.blit(speed_text, (10, 35))

        # Update high score
        if COINS_COLLECTED > HIGH_SCORE:
            HIGH_SCORE = COINS_COLLECTED

        # -------------------- MOVE AND DRAW SPRITES --------------------
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # -------------------- COIN COLLISION --------------------
        collected_coins = pygame.sprite.spritecollide(P1, coins, True)

        for coin in collected_coins:
            # Add coin value according to its weight
            COINS_COLLECTED += coin.weight

            if sounds["coin"]:
                sounds["coin"].play()

            # Increase enemy speed after every N collected coin points
            if COINS_COLLECTED % N == 0:
                SPEED += 1

                flash_text = font_medium.render("SPEED UP!", True, RED)
                DISPLAYSURF.blit(flash_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
                pygame.display.update()
                pygame.time.wait(150)

        # -------------------- ENEMY COLLISION --------------------
        if pygame.sprite.spritecollideany(P1, enemies):
            if sounds["crash"]:
                sounds["crash"].play()

            pygame.mixer.music.stop()
            time.sleep(0.5)

            play_again = show_game_over_screen(SCORE, COINS_COLLECTED, HIGH_SCORE)

            if play_again:
                P1, E1 = reset_game()

                pygame.time.set_timer(COIN_SPAWN, random.randint(700, 1500))

                if sounds["background"] == "music":
                    pygame.mixer.music.play(-1)
            else:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main_game()