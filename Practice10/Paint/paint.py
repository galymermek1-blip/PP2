import pygame
import sys
import os
from datetime import datetime
from tools import draw_shape, flood_fill

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 650
UI_HEIGHT = 120
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 200, 100)
RED = (220, 80, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 18)
text_font = pygame.font.SysFont("Arial", 28)

COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (180, 0, 255),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "white": (255, 255, 255)
}

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

current_tool = "pencil"
current_color_name = "black"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
typed_text = ""


def get_color():
    if current_tool == "eraser":
        return WHITE
    return COLORS[current_color_name]


def draw_text(surface, text, x, y, color=BLACK):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_button(text, x, y, w, h, active=False, color=GRAY):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GREEN if active else color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    label = small_font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

    return rect


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, f"paint_{timestamp}.png")

    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 2)

    tools = [
        ("Pencil", "pencil"),
        ("Line", "line"),
        ("Rect", "rect"),
        ("Circle", "circle"),
        ("Square", "square"),
        ("R-Tri", "rtriangle"),
        ("E-Tri", "etriangle"),
        ("Rhomb", "rhombus"),
        ("Fill", "fill"),
        ("Text", "text"),
        ("Eraser", "eraser"),
    ]

    x = 10
    for name, tool in tools:
        draw_button(name, x, 10, 65, 30, current_tool == tool)
        x += 70

    clear_btn = draw_button("Clear", 785, 10, 70, 30, False, RED)

    x = 10
    for cname, cval in COLORS.items():
        rect = pygame.Rect(x, 50, 28, 28)
        pygame.draw.rect(screen, cval, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        if current_color_name == cname:
            pygame.draw.rect(screen, RED, rect, 4)

        x += 33

    draw_button("Thin 2", 360, 50, 70, 28, brush_size == 2)
    draw_button("Med 5", 435, 50, 70, 28, brush_size == 5)
    draw_button("Thick 10", 510, 50, 80, 28, brush_size == 10)

    draw_text(
        screen,
        f"Tool: {current_tool.upper()} | Color: {current_color_name.upper()} | Size: {brush_size}",
        610,
        55
    )

    help_text = "Keys: 1 Thin, 2 Medium, 3 Thick | Ctrl+S Save | Enter text | Esc cancel"
    img = small_font.render(help_text, True, BLACK)
    screen.blit(img, (10, 92))

    return clear_btn


running = True

while running:
    screen.fill(WHITE)

    # First draw saved canvas
    screen.blit(canvas, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # Preview for line and shapes before mouse release
    if drawing and start_pos and current_tool in [
        "line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"
    ]:
        preview = canvas.copy()
        draw_shape(preview, current_tool, get_color(), start_pos, mouse_pos, brush_size)
        screen.blit(preview, (0, 0))

    # Preview for text before Enter
    if text_mode and text_pos:
        preview_text = text_font.render(typed_text + "|", True, get_color())
        screen.blit(preview_text, text_pos)

    # Draw UI last, but without covering preview on canvas area
    clear_button = draw_ui()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if text_mode:
                    text_mode = False
                    typed_text = ""
                    text_pos = None
                else:
                    running = False

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            elif event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(typed_text, True, get_color())
                    canvas.blit(final_text, text_pos)

                    text_mode = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < UI_HEIGHT:
                tool_buttons = [
                    ("pencil", pygame.Rect(10, 10, 65, 30)),
                    ("line", pygame.Rect(80, 10, 65, 30)),
                    ("rect", pygame.Rect(150, 10, 65, 30)),
                    ("circle", pygame.Rect(220, 10, 65, 30)),
                    ("square", pygame.Rect(290, 10, 65, 30)),
                    ("rtriangle", pygame.Rect(360, 10, 65, 30)),
                    ("etriangle", pygame.Rect(430, 10, 65, 30)),
                    ("rhombus", pygame.Rect(500, 10, 65, 30)),
                    ("fill", pygame.Rect(570, 10, 65, 30)),
                    ("text", pygame.Rect(640, 10, 65, 30)),
                    ("eraser", pygame.Rect(710, 10, 65, 30)),
                ]

                for tool, rect in tool_buttons:
                    if rect.collidepoint(mx, my):
                        current_tool = tool

                if clear_button.collidepoint(mx, my):
                    canvas.fill(WHITE)

                x = 10
                for cname in COLORS:
                    color_rect = pygame.Rect(x, 50, 28, 28)
                    if color_rect.collidepoint(mx, my):
                        current_color_name = cname
                    x += 33

                if pygame.Rect(360, 50, 70, 28).collidepoint(mx, my):
                    brush_size = 2
                elif pygame.Rect(435, 50, 70, 28).collidepoint(mx, my):
                    brush_size = 5
                elif pygame.Rect(510, 50, 80, 28).collidepoint(mx, my):
                    brush_size = 10

            else:
                if current_tool in ["pencil", "eraser"]:
                    drawing = True
                    last_pos = event.pos

                elif current_tool == "fill":
                    flood_fill(canvas, event.pos, get_color(), UI_HEIGHT)

                elif current_tool == "text":
                    text_mode = True
                    text_pos = event.pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and event.pos[1] > UI_HEIGHT:
                if current_tool == "pencil":
                    pygame.draw.line(canvas, get_color(), last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size)
                    last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if current_tool in [
                    "line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"
                ]:
                    draw_shape(canvas, current_tool, get_color(), start_pos, event.pos, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

pygame.quit()
sys.exit()