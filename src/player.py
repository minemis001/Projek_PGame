import pygame
from settings import TILE, RED


class Player:
    def __init__(self, tx, ty):
        self.size = 24  # hitbox sedikit lebih kecil dari tile agar mudah lewat celah
        self.speed = 200  # piksel per detik
        self.pos = pygame.Vector2(0, 0)
        self.set_tile(tx, ty)

    def set_tile(self, tx, ty):
        """Taruh pemain di tengah tile (tx, ty)."""
        offset = (TILE - self.size) / 2
        self.pos.update(tx * TILE + offset, ty * TILE + offset)

    @property
    def rect(self):
        return pygame.Rect(round(self.pos.x), round(self.pos.y), self.size, self.size)

    def update(self, dt, keys, tilemap):
        arah = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            arah.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            arah.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            arah.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            arah.y += 1
        if arah.length() > 0:
            arah = arah.normalize()

        # Gerak per sumbu: geser X, cek tabrakan, lalu geser Y, cek tabrakan
        self.pos.x += arah.x * self.speed * dt
        self._tabrakan(tilemap, "x", arah)
        self.pos.y += arah.y * self.speed * dt
        self._tabrakan(tilemap, "y", arah)

    def _tabrakan(self, tilemap, sumbu, arah):
        r = self.rect
        for tile in tilemap.solid_rects_near(r):
            if r.colliderect(tile):
                if sumbu == "x":
                    if arah.x > 0:
                        r.right = tile.left
                    elif arah.x < 0:
                        r.left = tile.right
                    self.pos.x = r.x
                else:
                    if arah.y > 0:
                        r.bottom = tile.top
                    elif arah.y < 0:
                        r.top = tile.bottom
                    self.pos.y = r.y

    def draw(self, layar, kamera):
        r = self.rect.move(-kamera.x, -kamera.y)
        pygame.draw.rect(layar, RED, r)