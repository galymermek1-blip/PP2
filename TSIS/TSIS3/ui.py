import pygame
import sys
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (0, 180, 0)
BLUE = (0, 80, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)

font_small = pygame.font.SysFont("Verdana", 18)
font_medium = pygame.font.SysFont("Verdana", 26)
font_large = pygame.font.SysFont("Verdana", 42)

settings = load_settings()


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


def main_menu():
    while True:
        screen.fill(BLACK)

        draw_text("TSIS3 RACER", font_large, YELLOW, WIDTH // 2, 90)

        play_btn = draw_button("Play", 100, 190, 200, 50, GREEN)
        leaderboard_btn = draw_button("Leaderboard", 100, 260, 200, 50, BLUE)
        settings_btn = draw_button("Settings", 100, 330, 200, 50, ORANGE)
        quit_btn = draw_button("Quit", 100, 400, 200, 50, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return "play"
                if leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard"
                if settings_btn.collidepoint(event.pos):
                    return "settings"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    while True:
        screen.fill(BLACK)

        draw_text("TOP 10", font_large, YELLOW, WIDTH // 2, 60)

        data = load_leaderboard()

        y = 120
        if not data:
            draw_text("No scores yet", font_medium, WHITE, WIDTH // 2, 260)
        else:
            for i, item in enumerate(data):
                text = f"{i + 1}. {item['name']} | Score: {item['score']} | Dist: {item['distance']}"
                draw_text(text, font_small, WHITE, 20, y, center=False)
                y += 35

        back_btn = draw_button("Back", 125, 520, 150, 45, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen():
    global settings

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "medium", "hard"]

    while True:
        screen.fill(BLACK)

        draw_text("SETTINGS", font_large, YELLOW, WIDTH // 2, 70)

        sound_btn = draw_button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 70, 150, 260, 45, BLUE)
        color_btn = draw_button(f"Car color: {settings['car_color']}", 70, 220, 260, 45, GREEN)
        diff_btn = draw_button(f"Difficulty: {settings['difficulty']}", 70, 290, 260, 45, ORANGE)
        back_btn = draw_button("Save & Back", 100, 500, 200, 45, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                if color_btn.collidepoint(event.pos):
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i + 1) % len(colors)]

                if diff_btn.collidepoint(event.pos):
                    i = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]

                if back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return