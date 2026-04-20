import pygame
import math
import sys

# ========== ОСНОВНАЯ АРХИТЕКТУРА СЦЕН ==========
class SceneBase:
    def __init__(self):
        self.next = self
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")
    def Update(self):
        print("uh-oh, you didn't override this in the child class")
    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Paint App - Graphic Editor")
    clock = pygame.time.Clock()
    active_scene = starting_scene
    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
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

class PaintScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.radius = 15
        self.mode = 'blue'
        self.drawing_mode = 'brush'
        self.start_pos = None
        self.drawing = False
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.COLORS = {
            'red': (255,0,0), 'green': (0,255,0), 'blue': (0,0,255),
            'yellow': (255,255,0), 'purple': (255,0,255), 'cyan': (0,255,255),
            'black': (0,0,0), 'white': (255,255,255), 'orange': (255,165,0),
            'pink': (255,192,203)
        }
        self.canvas = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.canvas.fill((255,255,255))
        try:
            self.font = pygame.font.Font(None,24)
            self.small_font = pygame.font.Font(None,18)
        except:
            pygame.font.init()
            self.font = pygame.font.Font(None,24)
            self.small_font = pygame.font.Font(None,18)
    def get_color(self):
        if self.drawing_mode == 'eraser':
            return (255,255,255)
        return self.COLORS.get(self.mode,(0,0,0))
    def draw_brush(self, pos):
        pygame.draw.circle(self.canvas, self.get_color(), pos, self.radius)
    def draw_rectangle(self, start, end):
        x1,y1 = start; x2,y2 = end
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))
        pygame.draw.rect(self.canvas, self.get_color(), rect, 2)
    def draw_circle(self, start, end):
        x1,y1 = start; x2,y2 = end
        r = int(math.hypot(x2-x1, y2-y1))
        pygame.draw.circle(self.canvas, self.get_color(), start, r, 2)
    def draw_ui(self, screen):
        pygame.draw.rect(screen, (200,200,200), (0,0,self.SCREEN_WIDTH,80))
        pygame.draw.line(screen, (0,0,0), (0,80), (self.SCREEN_WIDTH,80),2)
        # кнопки
        brush_rect = pygame.Rect(10,10,60,60)
        col = (100,200,100) if self.drawing_mode=='brush' else (150,150,150)
        pygame.draw.rect(screen, col, brush_rect); pygame.draw.rect(screen,(0,0,0),brush_rect,2)
        screen.blit(self.font.render("Brush",True,(0,0,0)),(20,35))
        rect_rect = pygame.Rect(80,10,60,60)
        col = (100,200,100) if self.drawing_mode=='rect' else (150,150,150)
        pygame.draw.rect(screen, col, rect_rect); pygame.draw.rect(screen,(0,0,0),rect_rect,2)
        screen.blit(self.font.render("Rect",True,(0,0,0)),(88,35))
        circle_rect = pygame.Rect(150,10,60,60)
        col = (100,200,100) if self.drawing_mode=='circle' else (150,150,150)
        pygame.draw.rect(screen, col, circle_rect); pygame.draw.rect(screen,(0,0,0),circle_rect,2)
        screen.blit(self.font.render("Circle",True,(0,0,0)),(155,35))
        eraser_rect = pygame.Rect(220,10,60,60)
        col = (100,200,100) if self.drawing_mode=='eraser' else (150,150,150)
        pygame.draw.rect(screen, col, eraser_rect); pygame.draw.rect(screen,(0,0,0),eraser_rect,2)
        screen.blit(self.font.render("Eraser",True,(0,0,0)),(223,35))
        clear_rect = pygame.Rect(290,10,60,60)
        pygame.draw.rect(screen, (200,100,100), clear_rect); pygame.draw.rect(screen,(0,0,0),clear_rect,2)
        screen.blit(self.font.render("Clear",True,(0,0,0)),(298,35))
        # палитра
        for i,(cname,cval) in enumerate(self.COLORS.items()):
            cr = pygame.Rect(370+i*35,10,30,30)
            pygame.draw.rect(screen, cval, cr); pygame.draw.rect(screen,(0,0,0),cr,2)
            if self.mode == cname:
                pygame.draw.rect(screen,(255,255,0),cr,3)
        # тексты
        # 1. Size - ТОЛЬКО ЭТО МЕНЯЮ: y было 25, стало 55 (ниже на 30)
        size_text = self.font.render(f"Size: {self.radius}", True, (0,0,0))
        screen.blit(size_text, (self.SCREEN_WIDTH - 130, 55))
        # 2. Mode
        mode_display = {'brush':'BRUSH','rect':'RECTANGLE','circle':'CIRCLE','eraser':'ERASER'}.get(self.drawing_mode, self.drawing_mode.upper())
        info_text = self.font.render(f"Mode: {mode_display} | Color: {self.mode.upper()}", True, (0,0,0))
        screen.blit(info_text, (370, 55))
        # 3. Инструкция
        help_text = self.small_font.render("1: Brush 2: Rect 3: Circle 4: Eraser | +/-: Size | C: Clear | ESC: Exit", True, (0,0,0))
        screen.blit(help_text, (10,85))
    def ProcessInput(self, events, pressed_keys):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.drawing_mode = 'brush'
                elif event.key == pygame.K_2:
                    self.drawing_mode = 'rect'
                elif event.key == pygame.K_3:
                    self.drawing_mode = 'circle'
                elif event.key == pygame.K_4:
                    self.drawing_mode = 'eraser'
                elif event.key == pygame.K_c:
                    self.canvas.fill((255,255,255))
                if event.key == pygame.K_r:
                    self.mode = 'red'
                elif event.key == pygame.K_g:
                    self.mode = 'green'
                elif event.key == pygame.K_b:
                    self.mode = 'blue'
                elif event.key == pygame.K_y:
                    self.mode = 'yellow'
                elif event.key == pygame.K_p:
                    self.mode = 'purple'
                elif event.key == pygame.K_c and not pressed_keys[pygame.K_LCTRL]:
                    self.mode = 'cyan'
                elif event.key == pygame.K_o:
                    self.mode = 'orange'
                elif event.key == pygame.K_k:
                    self.mode = 'pink'
                elif event.key == pygame.K_l:
                    self.mode = 'black'
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.radius = min(100, self.radius+1)
                elif event.key == pygame.K_MINUS:
                    self.radius = max(1, self.radius-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                if my < 80:
                    if 10 <= mx <= 70:
                        self.drawing_mode = 'brush'
                    elif 80 <= mx <= 140:
                        self.drawing_mode = 'rect'
                    elif 150 <= mx <= 210:
                        self.drawing_mode = 'circle'
                    elif 220 <= mx <= 280:
                        self.drawing_mode = 'eraser'
                    elif 290 <= mx <= 350:
                        self.canvas.fill((255,255,255))
                    for i,(cname,_) in enumerate(self.COLORS.items()):
                        cr = pygame.Rect(370+i*35,10,30,30)
                        if cr.collidepoint(mx,my):
                            self.mode = cname
                else:
                    if self.drawing_mode in ['rect','circle']:
                        self.start_pos = event.pos
                        self.drawing = True
                    elif self.drawing_mode == 'brush':
                        self.draw_brush(event.pos)
                    elif self.drawing_mode == 'eraser':
                        self.draw_brush(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing and self.start_pos:
                    end_pos = event.pos
                    if self.drawing_mode == 'rect':
                        self.draw_rectangle(self.start_pos, end_pos)
                    elif self.drawing_mode == 'circle':
                        self.draw_circle(self.start_pos, end_pos)
                    self.drawing = False
                    self.start_pos = None
            if event.type == pygame.MOUSEMOTION:
                if mouse_buttons[0]:
                    if mouse_pos[1] > 80:
                        if self.drawing_mode == 'brush':
                            self.draw_brush(event.pos)
                        elif self.drawing_mode == 'eraser':
                            self.draw_brush(event.pos)
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.canvas, (0,0))
        if self.drawing and self.start_pos and self.drawing_mode in ['rect','circle']:
            mp = pygame.mouse.get_pos()
            if mp[1] > 80:
                if self.drawing_mode == 'rect':
                    x1,y1 = self.start_pos
                    x2,y2 = mp
                    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))
                    pygame.draw.rect(screen, self.get_color(), rect, 2)
                else:
                    r = int(math.hypot(mp[0]-self.start_pos[0], mp[1]-self.start_pos[1]))
                    pygame.draw.circle(screen, self.get_color(), self.start_pos, r, 2)
        mp = pygame.mouse.get_pos()
        if not self.drawing and mp[1] > 80:
            cursor_color = (0,0,0) if self.drawing_mode != 'eraser' else (200,200,200)
            pygame.draw.circle(screen, cursor_color, mp, self.radius, 1)
            coord_text = self.small_font.render(f"X:{mp[0]} Y:{mp[1]}", True, (100,100,100))
            screen.blit(coord_text, (self.SCREEN_WIDTH-120, self.SCREEN_HEIGHT-25))
        self.draw_ui(screen)

if __name__ == "__main__":
    run_game(800,600,60,PaintScene())
