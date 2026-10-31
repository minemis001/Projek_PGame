import json
import os
import pygame

from settings import TILE

# Folder utama repo = satu tingkat di atas folder src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_DIR = os.path.join(BASE_DIR, "data", "maps")

# Karakter di grid -> warna (placeholder, nanti diganti gambar tile)
WARNA_TILE = {
    ".": (90, 150, 80),    # rumput
    "_": (150, 120, 80),   # lantai
    "#": (70, 70, 70),     # dinding / pohon / rumah (tidak bisa dilalui)
    "~": (50, 100, 200),   # air (tidak bisa dilalui)
    "D": (230, 190, 60),   # pintu / portal
}
TILE_SOLID = {"#", "~"}


class TileMap:
    def __init__(self, nama_file):
        path = os.path.join(MAP_DIR, nama_file + ".json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.nama = data["name"]
        self.grid = data["grid"]
        self.start = data["start"]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.width = self.cols * TILE
        self.height = self.rows * TILE
        # portal disimpan dengan kunci koordinat tile (x, y)
        self.portals = {(p["x"], p["y"]): p for p in data["portals"]}

    def tile_at(self, tx, ty):
        if 0 <= tx < self.cols and 0 <= ty < self.rows:
            return self.grid[ty][tx]
        return "#"  # di luar map dianggap dinding

    def solid_rects_near(self, rect):
        """Daftar rect tile padat yang berada di sekitar rect (untuk collision)."""
        hasil = []
        x0 = rect.left // TILE - 1
        x1 = rect.right // TILE + 1
        y0 = rect.top // TILE - 1
        y1 = rect.bottom // TILE + 1
        for ty in range(y0, y1 + 1):
            for tx in range(x0, x1 + 1):
                if self.tile_at(tx, ty) in TILE_SOLID:
                    hasil.append(pygame.Rect(tx * TILE, ty * TILE, TILE, TILE))
        return hasil

    def get_portal(self, rect):
        """Kembalikan portal jika titik tengah rect berada di tile portal."""
        tx = rect.centerx // TILE
        ty = rect.centery // TILE
        return self.portals.get((tx, ty))

    def draw(self, layar, kamera):
        lebar, tinggi = layar.get_size()
        tx0 = max(0, int(kamera.x) // TILE)
        ty0 = max(0, int(kamera.y) // TILE)
        tx1 = min(self.cols, (int(kamera.x) + lebar) // TILE + 2)
        ty1 = min(self.rows, (int(kamera.y) + tinggi) // TILE + 2)
        for ty in range(ty0, ty1):
            for tx in range(tx0, tx1):
                warna = WARNA_TILE.get(self.grid[ty][tx], (255, 0, 255))
                rect = pygame.Rect(tx * TILE - kamera.x, ty * TILE - kamera.y, TILE, TILE)
                pygame.draw.rect(layar, warna, rect)
                pygame.draw.rect(layar, (0, 0, 0), rect, 1)  # garis kisi tipis