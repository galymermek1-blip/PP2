import pygame
import math
import sys

# ВАЖНО: pygame и font нужно инициализировать до создания PaintScene
pygame.init()
pygame.font.init()


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


def run_game(width, height, fps, starting_scene):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Practice11 Paint")
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []

        for event in pygame.event.get():
            quit_attempt = False

            if event.type == pygame.QUIT:
                quit_attempt = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


class PaintScene(SceneBase):
    def __init__(self):
        super().__init__()

        self.radius = 15
        self.mode = "blue"
        self.drawing_mode = "brush"
        self.start_pos = None
        self.drawing = False

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.UI_HEIGHT = 100

        self.COLORS = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (255, 0, 255),
            "cyan": (0, 255, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "orange": (255, 165, 0),
            "pink": (255, 192, 203)
        }

        self.canvas = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.canvas.fill((255, 255, 255))

        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def get_color(self):
        """Возвращает текущий цвет. Для ластика используется белый."""
        if self.drawing_mode == "eraser":
            return (255, 255, 255)
        return self.COLORS.get(self.mode, (0, 0, 0))

    def draw_brush(self, pos):
        """Рисует кистью или ластиком."""
        pygame.draw.circle(self.canvas, self.get_color(), pos, self.radius)

    def draw_rectangle(self, surface, start, end):
        """Рисует прямоугольник."""
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
        pygame.draw.rect(surface, self.get_color(), rect, 2)

    def draw_circle(self, surface, start, end):
        """Рисует круг."""
        x1, y1 = start
        x2, y2 = end
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, self.get_color(), start, radius, 2)

    def draw_square(self, surface, start, end):
        """Рисует квадрат."""
        x1, y1 = start
        x2, y2 = end

        size = min(abs(x2 - x1), abs(y2 - y1))

        if x2 < x1:
            x1 -= size
        if y2 < y1:
            y1 -= size

        rect = pygame.Rect(x1, y1, size, size)
        pygame.draw.rect(surface, self.get_color(), rect, 2)

    def draw_right_triangle(self, surface, start, end):
        """Рисует прямоугольный треугольник."""
        x1, y1 = start
        x2, y2 = end

        points = [
            (x1, y1),
            (x2, y2),
            (x1, y2)
        ]

        pygame.draw.polygon(surface, self.get_color(), points, 2)

    def draw_equilateral_triangle(self, surface, start, end):
        """Рисует равносторонний треугольник."""
        x1, y1 = start
        x2, y2 = end

        side = abs(x2 - x1)
        direction = 1 if x2 >= x1 else -1

        p1 = (x1, y1)
        p2 = (x1 + side * direction, y1)
        p3 = (x1 + (side // 2) * direction, y1 - int(side * 0.866))

        pygame.draw.polygon(surface, self.get_color(), [p1, p2, p3], 2)

    def draw_rhombus(self, surface, start, end):
        """Рисует ромб."""
        x1, y1 = start
        x2, y2 = end

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]

        pygame.draw.polygon(surface, self.get_color(), points, 2)

    def draw_selected_shape(self, surface, start, end):
        """Вызывает нужную функцию фигуры."""
        if self.drawing_mode == "rect":
            self.draw_rectangle(surface, start, end)
        elif self.drawing_mode == "circle":
            self.draw_circle(surface, start, end)
        elif self.drawing_mode == "square":
            self.draw_square(surface, start, end)
        elif self.drawing_mode == "rtriangle":
            self.draw_right_triangle(surface, start, end)
        elif self.drawing_mode == "etriangle":
            self.draw_equilateral_triangle(surface, start, end)
        elif self.drawing_mode == "rhombus":
            self.draw_rhombus(surface, start, end)

    def draw_ui(self, screen):
        """Рисует верхнюю панель инструментов."""
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, self.SCREEN_WIDTH, self.UI_HEIGHT))
        pygame.draw.line(screen, (0, 0, 0), (0, self.UI_HEIGHT), (self.SCREEN_WIDTH, self.UI_HEIGHT), 2)

        buttons = [
            ("Brush", "brush", 10),
            ("Rect", "rect", 75),
            ("Circle", "circle", 140),
            ("Eraser", "eraser", 205),
            ("Clear", "clear", 270),
            ("Square", "square", 335),
            ("R-Tri", "rtriangle", 400),
            ("E-Tri", "etriangle", 465),
            ("Rhomb", "rhombus", 530),
        ]

        for text, mode, x in buttons:
            rect = pygame.Rect(x, 10, 60, 35)

            if mode == "clear":
                color = (200, 100, 100)
            else:
                color = (100, 200, 100) if self.drawing_mode == mode else (150, 150, 150)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            label = self.small_font.render(text, True, (0, 0, 0))
            screen.blit(label, label.get_rect(center=rect.center))

        # Палитра цветов
        for i, (cname, cval) in enumerate(self.COLORS.items()):
            cr = pygame.Rect(10 + i * 35, 55, 30, 25)
            pygame.draw.rect(screen, cval, cr)
            pygame.draw.rect(screen, (0, 0, 0), cr, 2)

            if self.mode == cname:
                pygame.draw.rect(screen, (255, 255, 0), cr, 3)

        mode_text = self.font.render(
            f"Mode: {self.drawing_mode.upper()} | Color: {self.mode.upper()} | Size: {self.radius}",
            True,
            (0, 0, 0)
        )
        screen.blit(mode_text, (380, 58))

        help_text = self.small_font.render(
            "1 Brush | 2 Rect | 3 Circle | 4 Eraser | 5 Square | 6 Right Tri | 7 Equal Tri | 8 Rhombus | C Clear",
            True,
            (0, 0, 0)
        )
        screen.blit(help_text, (10, 85))

    def ProcessInput(self, events, pressed_keys):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.drawing_mode = "brush"
                elif event.key == pygame.K_2:
                    self.drawing_mode = "rect"
                elif event.key == pygame.K_3:
                    self.drawing_mode = "circle"
                elif event.key == pygame.K_4:
                    self.drawing_mode = "eraser"
                elif event.key == pygame.K_5:
                    self.drawing_mode = "square"
                elif event.key == pygame.K_6:
                    self.drawing_mode = "rtriangle"
                elif event.key == pygame.K_7:
                    self.drawing_mode = "etriangle"
                elif event.key == pygame.K_8:
                    self.drawing_mode = "rhombus"
                elif event.key == pygame.K_c:
                    self.canvas.fill((255, 255, 255))

                if event.key == pygame.K_r:
                    self.mode = "red"
                elif event.key == pygame.K_g:
                    self.mode = "green"
                elif event.key == pygame.K_b:
                    self.mode = "blue"
                elif event.key == pygame.K_y:
                    self.mode = "yellow"
                elif event.key == pygame.K_p:
                    self.mode = "purple"
                elif event.key == pygame.K_o:
                    self.mode = "orange"
                elif event.key == pygame.K_k:
                    self.mode = "pink"
                elif event.key == pygame.K_l:
                    self.mode = "black"

                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.radius = min(100, self.radius + 1)
                elif event.key == pygame.K_MINUS:
                    self.radius = max(1, self.radius - 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if my < self.UI_HEIGHT:
                    button_modes = [
                        ("brush", pygame.Rect(10, 10, 60, 35)),
                        ("rect", pygame.Rect(75, 10, 60, 35)),
                        ("circle", pygame.Rect(140, 10, 60, 35)),
                        ("eraser", pygame.Rect(205, 10, 60, 35)),
                        ("clear", pygame.Rect(270, 10, 60, 35)),
                        ("square", pygame.Rect(335, 10, 60, 35)),
                        ("rtriangle", pygame.Rect(400, 10, 60, 35)),
                        ("etriangle", pygame.Rect(465, 10, 60, 35)),
                        ("rhombus", pygame.Rect(530, 10, 60, 35)),
                    ]

                    for mode, rect in button_modes:
                        if rect.collidepoint(mx, my):
                            if mode == "clear":
                                self.canvas.fill((255, 255, 255))
                            else:
                                self.drawing_mode = mode

                    for i, (cname, _) in enumerate(self.COLORS.items()):
                        cr = pygame.Rect(10 + i * 35, 55, 30, 25)
                        if cr.collidepoint(mx, my):
                            self.mode = cname

                else:
                    if self.drawing_mode in ["rect", "circle", "square", "rtriangle", "etriangle", "rhombus"]:
                        self.start_pos = event.pos
                        self.drawing = True
                    elif self.drawing_mode == "brush":
                        self.draw_brush(event.pos)
                    elif self.drawing_mode == "eraser":
                        self.draw_brush(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing and self.start_pos:
                    end_pos = event.pos

                    # Финально рисуем фигуру на холсте
                    self.draw_selected_shape(self.canvas, self.start_pos, end_pos)

                    self.drawing = False
                    self.start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if mouse_buttons[0] and mouse_pos[1] > self.UI_HEIGHT:
                    if self.drawing_mode == "brush":
                        self.draw_brush(event.pos)
                    elif self.drawing_mode == "eraser":
                        self.draw_brush(event.pos)

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.canvas, (0, 0))

        # Preview фигуры до отпускания мыши
        if self.drawing and self.start_pos:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] > self.UI_HEIGHT:
                self.draw_selected_shape(screen, self.start_pos, mouse_pos)

        mouse_pos = pygame.mouse.get_pos()

        if not self.drawing and mouse_pos[1] > self.UI_HEIGHT:
            cursor_color = (0, 0, 0) if self.drawing_mode != "eraser" else (200, 200, 200)
            pygame.draw.circle(screen, cursor_color, mouse_pos, self.radius, 1)

            coord_text = self.small_font.render(
                f"X:{mouse_pos[0]} Y:{mouse_pos[1]}",
                True,
                (100, 100, 100)
            )
            screen.blit(coord_text, (self.SCREEN_WIDTH - 120, self.SCREEN_HEIGHT - 25))

        self.draw_ui(screen)


if __name__ == "__main__":
    run_game(800, 600, 60, PaintScene())