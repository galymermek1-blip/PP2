import pygame
import random
import sys
import json
import os
from db import init_db, save_game, get_top10, get_personal_best

pygame.init()

# -------------------- DATABASE --------------------
init_db()

# -------------------- SCREEN SETTINGS --------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS4 Snake")
clock = pygame.time.Clock()

# -------------------- COLORS --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (160, 60, 255)
ORANGE = (255, 140, 0)
GRAY = (45, 45, 45)
GRID_COLOR = (40, 40, 40)

# -------------------- GAME SETTINGS --------------------
INITIAL_SPEED = 10
SPEED_INCREMENT = 2
LEVEL_STEP = 10
MAX_LEVEL = 5

SETTINGS_FILE = "settings.json"

# -------------------- DIRECTIONS --------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def load_settings():
    """Loads settings from settings.json."""
    default_settings = {
        "snake_color": [0, 255, 0],
        "grid": True,
        "sound": True
    }

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                data = json.load(file)
                default_settings.update(data)
        except:
            pass

    return default_settings


def save_settings(settings):
    """Saves settings to settings.json."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


def draw_text(text, size, x, y, color=WHITE, center=False):
    """Draws text on the screen."""
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(surface, rect)
    return rect


def draw_button(text, x, y, w, h, color=BLUE):
    """Draws a simple button."""
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    draw_text(text, 28, rect.centerx, rect.centery, WHITE, center=True)
    return rect


class Snake:
    """Snake class. Stores body, direction and movement logic."""

    def __init__(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2

        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]

        self.direction = RIGHT
        self.grow_flag = False
        self.shield = False

    def head(self):
        """Returns snake head."""
        return self.body[0]

    def move(self):
        """Moves snake by one cell."""
        head_x, head_y = self.head()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        """Makes snake grow after eating food."""
        self.grow_flag = True

    def shorten(self, amount):
        """Shortens snake after eating poison food."""
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()

    def change_direction(self, new_direction):
        """Changes direction but prevents 180-degree turn."""
        opposite = (-new_direction[0], -new_direction[1])

        if opposite != self.direction:
            self.direction = new_direction

    def check_collision(self, obstacles):
        """Checks wall, body and obstacle collision."""
        head = self.head()

        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True

        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True

        if head in self.body[1:]:
            return True

        if head in obstacles:
            return True

        return False


class Food:
    """Food class. Food can be normal or poison and has timer."""

    def __init__(self, snake_body, obstacles):
        self.position = (0, 0)
        self.weight = 1
        self.poison = False
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 5000
        self.randomize_position(snake_body, obstacles)

    def randomize_position(self, snake_body, obstacles):
        """Randomly places food away from snake and obstacles."""
        all_cells = []

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                all_cells.append((x, y))

        free_cells = [
            cell for cell in all_cells
            if cell not in snake_body and cell not in obstacles
        ]

        if free_cells:
            self.position = random.choice(free_cells)

        # 20% chance for poison food
        self.poison = random.randint(1, 5) == 1

        if self.poison:
            self.weight = 0
            self.life_time = 6000
        else:
            self.weight = random.choice([1, 2, 3])

            if self.weight == 1:
                self.life_time = 7000
            elif self.weight == 2:
                self.life_time = 5000
            else:
                self.life_time = 3000

        self.spawn_time = pygame.time.get_ticks()

    def expired(self):
        """Checks if food disappeared by timer."""
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.life_time

    def time_left(self):
        """Returns food time left in seconds."""
        current_time = pygame.time.get_ticks()
        left = self.life_time - (current_time - self.spawn_time)
        return max(0, left // 1000)


class Bonus:
    """Bonus class. Only one bonus can be on the field."""

    def __init__(self, snake_body, obstacles, food_position):
        self.position = (0, 0)
        self.kind = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000
        self.randomize_position(snake_body, obstacles, food_position)

    def randomize_position(self, snake_body, obstacles, food_position):
        """Places bonus on a free cell."""
        all_cells = []

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                all_cells.append((x, y))

        free_cells = [
            cell for cell in all_cells
            if cell not in snake_body
            and cell not in obstacles
            and cell != food_position
        ]

        if free_cells:
            self.position = random.choice(free_cells)

    def expired(self):
        """Checks if bonus disappeared."""
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.life_time


def get_level(score):
    """Calculates level from score."""
    level = score // LEVEL_STEP + 1
    return min(level, MAX_LEVEL)


def calculate_speed(level):
    """Calculates snake speed from level."""
    return INITIAL_SPEED + (level - 1) * SPEED_INCREMENT


def generate_obstacles(snake, level):
    """Generates static wall blocks from level 3."""
    obstacles = []

    if level < 3:
        return obstacles

    count = level * 3

    forbidden = set(snake.body)

    head_x, head_y = snake.head()

    # Keep cells around snake head free, so snake is not trapped.
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            forbidden.add((head_x + dx, head_y + dy))

    while len(obstacles) < count:
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        cell = (x, y)

        if cell not in forbidden and cell not in obstacles:
            obstacles.append(cell)

    return obstacles


def draw_grid():
    """Draws grid overlay."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_snake(snake):
    """Draws snake."""
    snake_color = tuple(settings["snake_color"])

    for i, segment in enumerate(snake.body):
        rect = pygame.Rect(
            segment[0] * CELL_SIZE,
            segment[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        color = DARK_GREEN if i == 0 else snake_color

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_food(food):
    """Draws normal or poison food."""
    rect = pygame.Rect(
        food.position[0] * CELL_SIZE,
        food.position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    if food.poison:
        color = DARK_RED
    elif food.weight == 1:
        color = RED
    elif food.weight == 2:
        color = YELLOW
    else:
        color = PURPLE

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_bonus(bonus):
    """Draws bonus."""
    if bonus is None:
        return

    rect = pygame.Rect(
        bonus.position[0] * CELL_SIZE,
        bonus.position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    if bonus.kind == "speed":
        color = ORANGE
        label = "F"
    elif bonus.kind == "slow":
        color = BLUE
        label = "S"
    else:
        color = WHITE
        label = "H"

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GRID_COLOR, rect, 1)
    draw_text(label, 22, rect.centerx, rect.centery, BLACK, center=True)


def draw_obstacles(obstacles):
    """Draws wall blocks."""
    for cell in obstacles:
        rect = pygame.Rect(
            cell[0] * CELL_SIZE,
            cell[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)


def input_name_screen():
    """Username input screen."""
    username = ""

    while True:
        screen.fill(BLACK)

        draw_text("Enter username", 42, SCREEN_WIDTH // 2, 160, YELLOW, center=True)
        draw_text(username + "|", 36, SCREEN_WIDTH // 2, 240, WHITE, center=True)
        draw_text("Press ENTER to start", 26, SCREEN_WIDTH // 2, 320, WHITE, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username.strip() if username.strip() else "Player"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 15:
                        username += event.unicode


def main_menu():
    """Main menu screen."""
    while True:
        screen.fill(BLACK)

        draw_text("TSIS4 SNAKE", 54, SCREEN_WIDTH // 2, 100, YELLOW, center=True)

        play_btn = draw_button("Play", 200, 190, 200, 45, GREEN)
        leader_btn = draw_button("Leaderboard", 200, 250, 200, 45, BLUE)
        settings_btn = draw_button("Settings", 200, 310, 200, 45, ORANGE)
        exit_btn = draw_button("Exit", 200, 370, 200, 45, RED)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    username = input_name_screen()
                    return username

                if leader_btn.collidepoint(event.pos):
                    leaderboard_screen()

                if settings_btn.collidepoint(event.pos):
                    settings_screen()

                if exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    """Leaderboard screen from PostgreSQL."""
    while True:
        screen.fill(BLACK)

        draw_text("LEADERBOARD", 46, SCREEN_WIDTH // 2, 50, YELLOW, center=True)

        data = get_top10()

        y = 110

        if not data:
            draw_text("No database data", 32, SCREEN_WIDTH // 2, 250, WHITE, center=True)
        else:
            draw_text("Rank  Name     Score  Level  Date", 24, 60, 90, WHITE)

            for i, row in enumerate(data):
                username, score, level, played_at = row
                date_text = str(played_at).split(".")[0]

                text = f"{i + 1}. {username} | {score} | L{level} | {date_text}"
                draw_text(text, 22, 40, y, WHITE)
                y += 35

        back_btn = draw_button("Back", 200, 530, 200, 45, RED)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen():
    """Settings screen. Saves settings to JSON."""
    color_options = [
        [0, 255, 0],
        [255, 255, 0],
        [0, 120, 255],
        [255, 0, 0],
        [160, 60, 255]
    ]

    while True:
        screen.fill(BLACK)

        draw_text("SETTINGS", 48, SCREEN_WIDTH // 2, 70, YELLOW, center=True)

        grid_btn = draw_button(
            f"Grid: {'ON' if settings['grid'] else 'OFF'}",
            170, 160, 260, 45, BLUE
        )

        sound_btn = draw_button(
            f"Sound: {'ON' if settings['sound'] else 'OFF'}",
            170, 230, 260, 45, BLUE
        )

        color_btn = draw_button(
            "Change Snake Color",
            170, 300, 260, 45, ORANGE
        )

        save_btn = draw_button(
            "Save and Back",
            170, 450, 260, 45, GREEN
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                if color_btn.collidepoint(event.pos):
                    current = settings["snake_color"]
                    index = color_options.index(current) if current in color_options else 0
                    settings["snake_color"] = color_options[(index + 1) % len(color_options)]

                if save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return


def game_over_screen(score, level, personal_best):
    """Game over screen."""
    while True:
        screen.fill(BLACK)

        draw_text("GAME OVER", 54, SCREEN_WIDTH // 2, 120, RED, center=True)
        draw_text(f"Score: {score}", 34, SCREEN_WIDTH // 2, 210, WHITE, center=True)
        draw_text(f"Level reached: {level}", 34, SCREEN_WIDTH // 2, 255, WHITE, center=True)
        draw_text(f"Personal best: {personal_best}", 34, SCREEN_WIDTH // 2, 300, YELLOW, center=True)

        retry_btn = draw_button("Retry", 200, 390, 200, 45, GREEN)
        menu_btn = draw_button("Main Menu", 200, 455, 200, 45, BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"


def run_game(username):
    """Main game loop."""
    snake = Snake()

    score = 0
    level = get_level(score)
    speed = calculate_speed(level)

    obstacles = generate_obstacles(snake, level)
    food = Food(snake.body, obstacles)

    bonus = None
    bonus_spawn_time = pygame.time.get_ticks()

    active_bonus = None
    active_bonus_start = 0
    active_bonus_duration = 5000

    personal_best = get_personal_best(username)

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        # -------------------- EVENTS --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(username, score, level)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        # -------------------- BONUS TIMER --------------------
        current_speed = speed

        if active_bonus == "speed":
            current_speed = speed + 5

            if current_time - active_bonus_start > active_bonus_duration:
                active_bonus = None

        elif active_bonus == "slow":
            current_speed = max(4, speed - 5)

            if current_time - active_bonus_start > active_bonus_duration:
                active_bonus = None

        elif active_bonus == "shield":
            pass

        # -------------------- SPAWN BONUS --------------------
        if bonus is None and current_time - bonus_spawn_time > 6000:
            bonus = Bonus(snake.body, obstacles, food.position)
            bonus_spawn_time = current_time

        if bonus is not None and bonus.expired():
            bonus = None
            bonus_spawn_time = current_time

        # -------------------- MOVE --------------------
        snake.move()

        # -------------------- COLLISION --------------------
        if snake.check_collision(obstacles):
            if active_bonus == "shield":
                active_bonus = None
                snake.shield = False

                # Move snake back to safe start if shield saved it.
                snake.body[0] = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
            else:
                running = False
                break

        # -------------------- FOOD LOGIC --------------------
        if snake.head() == food.position:
            if food.poison:
                snake.shorten(2)

                if len(snake.body) <= 1:
                    running = False
                    break
            else:
                snake.grow()
                score += food.weight

            new_level = get_level(score)

            if new_level != level:
                level = new_level
                speed = calculate_speed(level)
                obstacles = generate_obstacles(snake, level)

            food.randomize_position(snake.body, obstacles)

        if food.expired():
            food.randomize_position(snake.body, obstacles)

        # -------------------- BONUS PICKUP --------------------
        if bonus is not None and snake.head() == bonus.position:
            active_bonus = bonus.kind
            active_bonus_start = current_time

            if bonus.kind == "shield":
                snake.shield = True

            bonus = None
            bonus_spawn_time = current_time

        # -------------------- DRAW --------------------
        screen.fill(BLACK)

        if settings["grid"]:
            draw_grid()

        draw_obstacles(obstacles)
        draw_snake(snake)
        draw_food(food)
        draw_bonus(bonus)

        draw_text(f"Score: {score}", 24, 10, 10)
        draw_text(f"Level: {level}", 24, 10, 35)
        draw_text(f"Best: {personal_best}", 24, 10, 60)
        draw_text(f"Food: {'Poison' if food.poison else food.weight}", 24, 10, 85)
        draw_text(f"Food time: {food.time_left()}s", 24, 10, 110)

        if active_bonus:
            draw_text(f"Bonus: {active_bonus}", 24, 400, 10, YELLOW)
        else:
            draw_text("Bonus: None", 24, 400, 10, WHITE)

        pygame.display.flip()
        clock.tick(current_speed)

    save_game(username, score, level)
    personal_best = max(personal_best, score)

    return game_over_screen(score, level, personal_best)


# -------------------- MAIN PROGRAM --------------------
while True:
    username = main_menu()

    while True:
        result = run_game(username)

        if result == "menu":
            break