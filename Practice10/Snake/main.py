import pygame
import random
import sys

pygame.init()

# Параметры поля
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
GRID_COLOR = (40, 40, 40)  # цвет линий сетки

# Настройки уровней
INITIAL_SPEED = 10
SPEED_INCREMENT = 2
LEVEL_THRESHOLDS = [0, 10, 20, 30, 40]
MAX_LEVEL = 5

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.body = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = RIGHT
        self.grow_flag = False

    def head(self):
        return self.body[0]

    def move(self):
        head_x, head_y = self.head()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def check_collision(self):
        head = self.head()
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        all_cells = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        free_cells = [cell for cell in all_cells if cell not in snake_body]
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = (0, 0)

def get_level(score):
    for i in range(len(LEVEL_THRESHOLDS) - 1, -1, -1):
        if score >= LEVEL_THRESHOLDS[i]:
            return min(i + 1, MAX_LEVEL)
    return 1

def calculate_speed(level):
    return INITIAL_SPEED + (level - 1) * SPEED_INCREMENT

def draw_grid(screen):
    """Рисует сетку из линий"""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_snake(screen, snake):
    for i, segment in enumerate(snake.body):
        rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)  # обводка клетки

def draw_food(screen, food):
    rect = pygame.Rect(food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake with Levels and Grid")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.body)
    score = 0
    level = get_level(score)
    speed = calculate_speed(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        snake.move()

        if snake.check_collision():
            running = False
            break

        if snake.head() == food.position:
            snake.grow()
            score += 1
            new_level = get_level(score)
            if new_level != level:
                level = new_level
                speed = calculate_speed(level)
                print(f"Повышение уровня! Теперь уровень {level}, скорость {speed} FPS")
            food.randomize_position(snake.body)

        screen.fill(BLACK)
        draw_grid(screen)            # рисуем сетку
        draw_snake(screen, snake)
        draw_food(screen, food)
        draw_text(screen, f"Score: {score}", 24, 10, 10)
        draw_text(screen, f"Level: {level}", 24, SCREEN_WIDTH - 80, 10)
        pygame.display.flip()

        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()