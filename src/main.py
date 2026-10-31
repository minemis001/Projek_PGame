import sys
import pygame

from settings import *
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.layar = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.font_judul = pygame.font.Font(None, 72)
        self.font_menu = pygame.font.Font(None, 48)

        self.state = STATE_MENU
        self.menu_items = ["New Game", "Load", "Exit"]
        self.menu_index = 0

        self.player = None

    # ---------- pindah state ----------
    def mulai_game_baru(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.state = STATE_PLAYING

    def pilih_menu(self):
        pilihan = self.menu_items[self.menu_index]
        if pilihan == "New Game":
            self.mulai_game_baru()
        elif pilihan == "Load":
            print("Load belum dibuat (Tahap 15)")
        elif pilihan == "Exit":
            self.running = False

    # ---------- event ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_index = (self.menu_index - 1) % len(self.menu_items)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_index = (self.menu_index + 1) % len(self.menu_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.pilih_menu()

                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

    # ---------- update ----------
    def update(self, dt):
        if self.state == STATE_PLAYING:
            self.player.update(dt, pygame.key.get_pressed())

    # ---------- gambar ----------
    def draw_menu(self):
        self.layar.fill(GRAY)
        judul = self.font_judul.render(TITLE, True, WHITE)
        self.layar.blit(judul, judul.get_rect(center=(WIDTH // 2, 140)))

        for i, teks in enumerate(self.menu_items):
            warna = YELLOW if i == self.menu_index else WHITE
            label = self.font_menu.render(teks, True, warna)
            self.layar.blit(label, label.get_rect(center=(WIDTH // 2, 280 + i * 60)))

    def draw_playing(self):
        self.layar.fill(BG_PLAY)
        self.player.draw(self.layar)

    def draw(self):
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        pygame.display.flip()

    # ---------- loop utama ----------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # detik sejak frame sebelumnya
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()