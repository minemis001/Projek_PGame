import pygame
from settings import TILE, RED, WIDTH, HEIGHT


class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)  # posisi (float agar gerak halus)
        self.size = TILE
        self.speed = 200  # piksel per detik

    def update(self, dt, keys):
        arah = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            arah.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            arah.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            arah.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            arah.y += 1

        # Normalisasi supaya gerak diagonal tidak lebih cepat
        if arah.length() > 0:
            arah = arah.normalize()
        self.pos += arah * self.speed * dt

        # Batasi agar tidak keluar layar (sementara, sebelum ada collision map)
        self.pos.x = max(0, min(self.pos.x, WIDTH - self.size))
        self.pos.y = max(0, min(self.pos.y, HEIGHT - self.size))

    def draw(self, layar):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        pygame.draw.rect(layar, RED, rect)