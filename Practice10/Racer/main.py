import pygame
import sys
import os
import random
import time
from pygame.locals import *

# Initializing
pygame.init()
pygame.mixer.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  # Счетчик собранных монет
HIGH_SCORE = 0  # Рекорд

# Base path
BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 30)
font_large = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)

# Load background
try:
    background = pygame.image.load(
        os.path.join(IMAGES_DIR, "AnimatedStreet.png")
    )
except:
    # Создаем простой фон если нет изображения
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(GREEN)
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(background, WHITE, (SCREEN_WIDTH//2 - 5, i, 10, 30))

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game - Collect Coins!")

# Глобальные группы спрайтов
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
P1 = None
E1 = None

class Enemy(pygame.sprite.Sprite):
    """Класс вражеских машин, которые нужно избегать"""
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(
                os.path.join(IMAGES_DIR, "Enemy.png")
            )
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Движение врага вниз по экрану"""
        global SCORE
        self.rect.move_ip(0, SPEED)

        # Если враг достиг нижней части экрана, увеличиваем счет и возрождаем сверху
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    """Класс монет, которые нужно собирать"""
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(
                os.path.join(IMAGES_DIR, "Coin.png")
            )
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            # Если изображения нет, создаем монету программно
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
            pygame.draw.circle(self.image, (255, 215, 0), (12, 12), 10)
        
        self.rect = self.image.get_rect()
        # Разные веса монет (размер)
        self.weight = random.choice([1, 2, 3])
        # Позиционируем монету в случайном месте сверху
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), random.randint(-100, -20))
        
    def move(self):
        """Движение монеты вниз по экрану"""
        self.rect.move_ip(0, SPEED)
        
        # Если монета упала ниже экрана, удаляем ее
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    """Класс игрока (машина игрока)"""
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(
                os.path.join(IMAGES_DIR, "Player.png")
            )
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """Управление машиной игрока с клавиатуры"""
        pressed_keys = pygame.key.get_pressed()

        # Движение влево
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        # Движение вправо
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

def load_sounds():
    """Загрузка звуковых эффектов и фоновой музыки"""
    sounds = {
        'crash': None,
        'coin': None,
        'background': None
    }
    
    # Загружаем звук столкновения
    try:
        crash_path = os.path.join(SOUNDS_DIR, "crash.wav")
        if os.path.exists(crash_path):
            sounds['crash'] = pygame.mixer.Sound(crash_path)
            print("Crash sound loaded")
    except Exception as e:
        print(f"Could not load crash sound: {e}")
    
    # Загружаем звук монеты
    try:
        coin_path = os.path.join(SOUNDS_DIR, "coin.wav")
        if os.path.exists(coin_path):
            sounds['coin'] = pygame.mixer.Sound(coin_path)
            print("Coin sound loaded")
    except Exception as e:
        print(f"Could not load coin sound: {e}")
    
    # Загружаем фоновую музыку
    try:
        # Пробуем разные форматы
        for ext in ['.mp3', '.wav', '.ogg']:
            bg_path = os.path.join(SOUNDS_DIR, f"background{ext}")
            if os.path.exists(bg_path):
                pygame.mixer.music.load(bg_path)
                sounds['background'] = "music"
                print(f"Background music loaded from background{ext}")
                break
    except Exception as e:
        print(f"Could not load background music: {e}")
    
    return sounds

def show_game_over_screen(final_score, final_coins, high_score):
    """Показывает экран Game Over с кнопкой Play Again"""
    DISPLAYSURF.fill(RED)
    
    # Отображаем Game Over
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 100))
    DISPLAYSURF.blit(game_over_text, game_over_rect)
    
    # Отображаем финальный счет
    score_text = font_medium.render(f"Final Score: {final_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 200))
    DISPLAYSURF.blit(score_text, score_rect)
    
    # Отображаем собранные монеты
    coins_text = font_medium.render(f"Coins Collected: {final_coins}", True, YELLOW)
    coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH//2, 250))
    DISPLAYSURF.blit(coins_text, coins_rect)
    
    # Отображаем рекорд
    high_score_text = font_medium.render(f"High Score: {high_score}", True, GREEN)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
    DISPLAYSURF.blit(high_score_text, high_score_rect)
    
    # Кнопка Play Again
    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 380, 200, 50)
    pygame.draw.rect(DISPLAYSURF, GREEN, button_rect)
    pygame.draw.rect(DISPLAYSURF, WHITE, button_rect, 2)
    
    play_again_text = font_medium.render("PLAY AGAIN", True, BLACK)
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH//2, 405))
    DISPLAYSURF.blit(play_again_text, play_again_rect)
    
    # Кнопка Quit
    quit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 450, 200, 50)
    pygame.draw.rect(DISPLAYSURF, RED, quit_rect)
    pygame.draw.rect(DISPLAYSURF, WHITE, quit_rect, 2)
    
    quit_text = font_medium.render("QUIT", True, WHITE)
    quit_rect_text = quit_text.get_rect(center=(SCREEN_WIDTH//2, 475))
    DISPLAYSURF.blit(quit_text, quit_rect_text)
    
    pygame.display.update()
    
    # Ожидаем нажатия кнопки
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Проверяем нажатие на Play Again
                if button_rect.collidepoint(mouse_pos):
                    return True
                
                # Проверяем нажатие на Quit
                if quit_rect.collidepoint(mouse_pos):
                    return False
            
            if event.type == KEYDOWN:
                if event.key == K_r:  # Клавиша R для перезапуска
                    return True
                if event.key == K_q or event.key == K_ESCAPE:  # Q или ESC для выхода
                    return False
    
    return False

def reset_game():
    """Сбрасывает все переменные игры для нового раунда"""
    global SPEED, SCORE, COINS_COLLECTED, enemies, coins, all_sprites, P1, E1
    
    SPEED = 5
    SCORE = 0
    COINS_COLLECTED = 0
    
    # Очищаем все группы спрайтов
    enemies.empty()
    coins.empty()
    all_sprites.empty()
    
    # Создаем новые объекты
    P1 = Player()
    E1 = Enemy()
    
    enemies.add(E1)
    all_sprites.add(P1)
    all_sprites.add(E1)
    
    return P1, E1

def main_game():
    """Основная игровая функция"""
    global SPEED, SCORE, COINS_COLLECTED, HIGH_SCORE, enemies, coins, all_sprites, P1, E1
    
    # Загружаем звуки
    sounds = load_sounds()
    
    # Запускаем фоновую музыку (зацикленную)
    if sounds['background'] == "music":
        pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение
        pygame.mixer.music.set_volume(0.5)  # Громкость 50%
    
    # Инициализация игры
    P1, E1 = reset_game()
    
    # Таймеры событий
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)
    
    COIN_SPAWN = pygame.USEREVENT + 2
    pygame.time.set_timer(COIN_SPAWN, random.randint(500, 1500))
    
    # Игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.3
            
            if event.type == COIN_SPAWN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)
                pygame.time.set_timer(COIN_SPAWN, random.randint(500, 1500))
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Отрисовка фона
        DISPLAYSURF.blit(background, (0, 0))
        
        # Отображение счета
        score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(score_text, (10, 10))
        
        # Отображение монет (правый верхний угол)
        coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, YELLOW)
        coins_rect = coins_text.get_rect()
        coins_rect.topright = (SCREEN_WIDTH - 10, 10)
        DISPLAYSURF.blit(coins_text, coins_rect)
        
        # Отображение рекорда
        if COINS_COLLECTED > HIGH_SCORE:
            HIGH_SCORE = COINS_COLLECTED
        
        high_score_text = font_small.render(f"Best: {HIGH_SCORE}", True, GREEN)
        DISPLAYSURF.blit(high_score_text, (10, 35))
        
        # Движение и отрисовка спрайтов
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        
        # Проверка сбора монет
        collected_coins = pygame.sprite.spritecollide(P1, coins, True)
        for coin in collected_coins:
            COINS_COLLECTED += coin.weight
            if sounds['coin']:
                sounds['coin'].play()
            
            # Бонус: каждые 10 монет увеличиваем скорость
            if COINS_COLLECTED % 10 == 0:
                SPEED += 0.5
                # Визуальный эффект
                flash_text = font_medium.render("SPEED UP!", True, RED)
                DISPLAYSURF.blit(flash_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2))
                pygame.display.update()
                pygame.time.wait(100)
        
        # Проверка столкновения с врагами
        if pygame.sprite.spritecollideany(P1, enemies):
            if sounds['crash']:
                sounds['crash'].play()
            
            # Останавливаем фоновую музыку
            pygame.mixer.music.stop()
            
            time.sleep(0.5)
            
            # Показываем экран Game Over
            play_again = show_game_over_screen(SCORE, COINS_COLLECTED, HIGH_SCORE)
            
            if play_again:
                # Перезапускаем игру
                pygame.mixer.music.stop()
                P1, E1 = reset_game()
                # Сбрасываем таймеры
                pygame.time.set_timer(INC_SPEED, 1000)
                pygame.time.set_timer(COIN_SPAWN, random.randint(500, 1500))
                # Перезапускаем музыку
                if sounds['background'] == "music":
                    pygame.mixer.music.play(-1)
            else:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        FramePerSec.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    main_game()