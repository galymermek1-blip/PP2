import pygame
import random
import sys

pygame.init()

# -------------------- FIELD SETTINGS --------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# -------------------- COLORS --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GRID_COLOR = (40, 40, 40)

# -------------------- LEVEL SETTINGS --------------------
INITIAL_SPEED = 10
SPEED_INCREMENT = 2
LEVEL_THRESHOLDS = [0, 10, 20, 30, 40]
MAX_LEVEL = 5

# Food disappears after 5 seconds
FOOD_LIFETIME = 5000

# -------------------- DIRECTIONS --------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """Class for snake body, movement, growing and collision."""

    def __init__(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2

        # Snake body is a list of cells. First element is the head.
        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]

        self.direction = RIGHT
        self.grow_flag = False

    def head(self):
        """Return snake head position."""
        return self.body[0]

    def move(self):
        """Move snake one cell forward."""
        head_x, head_y = self.head()
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail if snake does not need to grow
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        """Snake grows after eating food."""
        self.grow_flag = True

    def change_direction(self, new_dir):
        """Change direction and prevent reverse movement."""
        opposite = (new_dir[0] * -1, new_dir[1] * -1)

        if opposite != self.direction:
            self.direction = new_dir

    def check_collision(self):
        """Check collision with walls or snake body."""
        head = self.head()

        # Border collision
        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True

        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False


class Food:
    """Food has random position, weight and timer."""

    def __init__(self, snake_body):
        self.position = (0, 0)
        self.weight = 1
        self.spawn_time = 0
        self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        """Place food in a random free cell, not on snake body."""
        all_cells = []

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                all_cells.append((x, y))

        free_cells = [cell for cell in all_cells if cell not in snake_body]

        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = (0, 0)

        # Practice 11: random food weight
        self.weight = random.choice([1, 2, 3])

        # Save time when food appeared
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        """Check if food lifetime is over."""
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > FOOD_LIFETIME

    def time_left(self):
        """Return food time left in seconds."""
        current_time = pygame.time.get_ticks()
        left = FOOD_LIFETIME - (current_time - self.spawn_time)
        return max(0, left // 1000)


def get_level(score):
    """Calculate level based on score."""
    for i in range(len(LEVEL_THRESHOLDS) - 1, -1, -1):
        if score >= LEVEL_THRESHOLDS[i]:
            return min(i + 1, MAX_LEVEL)
    return 1


def calculate_speed(level):
    """Increase speed when level increases."""
    return INITIAL_SPEED + (level - 1) * SPEED_INCREMENT


def draw_grid(screen):
    """Draw grid lines."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_snake(screen, snake):
    """Draw snake on the screen."""
    for i, segment in enumerate(snake.body):
        rect = pygame.Rect(
            segment[0] * CELL_SIZE,
            segment[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        # Head is darker than body
        color = DARK_GREEN if i == 0 else GREEN

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_food(screen, food):
    """Draw food. Color depends on food weight."""
    rect = pygame.Rect(
        food.position[0] * CELL_SIZE,
        food.position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    if food.weight == 1:
        color = RED
    elif food.weight == 2:
        color = ORANGE
    else:
        color = YELLOW

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_text(screen, text, size, x, y, color=WHITE):
    """Draw text on screen."""
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def main():
    """Main game loop."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Practice 11 Snake")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.body)

    score = 0
    level = get_level(score)
    speed = calculate_speed(level)

    running = True

    while running:
        # -------------------- EVENTS --------------------
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

        # -------------------- MOVE SNAKE --------------------
        snake.move()

        # -------------------- COLLISION CHECK --------------------
        if snake.check_collision():
            running = False
            break

        # -------------------- FOOD TIMER --------------------
        # If food is not eaten in time, it disappears and respawns
        if food.is_expired():
            food.randomize_position(snake.body)

        # -------------------- EATING FOOD --------------------
        if snake.head() == food.position:
            snake.grow()

            # Practice 11: score increases by food weight
            score += food.weight

            # Practice 10: level and speed depend on score
            new_level = get_level(score)

            if new_level != level:
                level = new_level
                speed = calculate_speed(level)
                print(f"Level up! Level: {level}, Speed: {speed}")

            # Create new food
            food.randomize_position(snake.body)

        # -------------------- DRAWING --------------------
        screen.fill(BLACK)

        draw_grid(screen)
        draw_snake(screen, snake)
        draw_food(screen, food)

        draw_text(screen, f"Score: {score}", 24, 10, 10)
        draw_text(screen, f"Level: {level}", 24, SCREEN_WIDTH - 90, 10)
        draw_text(screen, f"Food weight: {food.weight}", 24, 10, 35)
        draw_text(screen, f"Food time: {food.time_left()}s", 24, 10, 60)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()