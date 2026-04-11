import pygame
import os


class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 28)

        current_dir = os.path.dirname(__file__)
        self.music_folder = os.path.join(current_dir, "music")

        self.playlist = [
            os.path.join(self.music_folder, f)
            for f in os.listdir(self.music_folder)
            if f.endswith(".mp3") or f.endswith(".wav")
        ]

        self.index = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def draw(self):
        self.screen.fill((255, 255, 255))

        text1 = self.font.render("P=Play S=Stop N=Next B=Back Q=Quit", True, (0, 0, 0))
        self.screen.blit(text1, (50, 50))

        if self.playlist:
            name = os.path.basename(self.playlist[self.index])
        else:
            name = "No music"

        text2 = self.font.render("Track: " + name, True, (0, 0, 255))
        self.screen.blit(text2, (50, 120))

        status = "Playing" if self.is_playing else "Stopped"
        text3 = self.font.render("Status: " + status, True, (0, 150, 0))
        self.screen.blit(text3, (50, 170))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.play()
                    elif event.key == pygame.K_s:
                        self.stop()
                    elif event.key == pygame.K_n:
                        self.next()
                    elif event.key == pygame.K_b:
                        self.prev()

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)