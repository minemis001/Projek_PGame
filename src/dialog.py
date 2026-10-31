import json
import os
import pygame

from settings import WIDTH, HEIGHT, WHITE, YELLOW

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIALOG_DIR = os.path.join(BASE_DIR, "data", "dialog")


def load_dialog(nama):
    """Baca data/dialog/<nama>.json dan kembalikan daftar baris dialog."""
    path = os.path.join(DIALOG_DIR, nama + ".json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["lines"]


def bungkus_teks(teks, font, lebar_maks):
    """Pecah teks menjadi beberapa baris agar muat dalam lebar_maks piksel."""
    baris = []
    sekarang = ""
    for kata in teks.split(" "):
        coba = kata if not sekarang else sekarang + " " + kata
        if font.size(coba)[0] <= lebar_maks:
            sekarang = coba
        else:
            baris.append(sekarang)
            sekarang = kata
    if sekarang:
        baris.append(sekarang)
    return baris


class DialogBox:
    CPS = 45  # karakter per detik (kecepatan teks berjalan)

    def __init__(self):
        self.font_nama = pygame.font.Font(None, 34)
        self.font_teks = pygame.font.Font(None, 30)

        margin = 30
        tinggi = 150
        self.rect = pygame.Rect(margin, HEIGHT - tinggi - margin, WIDTH - 2 * margin, tinggi)
        self.padding = 20

        self.lines = []
        self.index = 0
        self.shown = 0.0      # jumlah karakter yang sudah tampil
        self.aktif = False
        self.on_finish = None
        self.waktu = 0.0      # untuk animasi penanda "lanjut"

    # ---------- kontrol ----------
    def start(self, lines, on_finish=None):
        self.lines = lines
        self.index = 0
        self.shown = 0.0
        self.aktif = True
        self.on_finish = on_finish

    def _teks(self):
        return self.lines[self.index]["text"]

    def selesai_mengetik(self):
        return self.shown >= len(self._teks())

    def advance(self):
        """Dipanggil saat pemain menekan tombol lanjut."""
        if not self.aktif:
            return
        if not self.selesai_mengetik():
            self.shown = len(self._teks())  # tampilkan semua teks sekaligus
            return
        self.index += 1
        if self.index >= len(self.lines):
            self.aktif = False
            callback = self.on_finish
            self.on_finish = None
            if callback:
                callback()
        else:
            self.shown = 0.0

    # ---------- update & gambar ----------
    def update(self, dt):
        self.waktu += dt
        if self.aktif and not self.selesai_mengetik():
            self.shown = min(len(self._teks()), self.shown + self.CPS * dt)

    def draw(self, layar):
        if not self.aktif:
            return
        baris_data = self.lines[self.index]

        # Panel semi-transparan
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        panel.fill((15, 15, 35, 225))
        layar.blit(panel, self.rect.topleft)
        pygame.draw.rect(layar, WHITE, self.rect, 2)

        # Nama pembicara (kosong = narasi)
        nama = baris_data.get("speaker", "")
        if nama:
            label = self.font_nama.render(nama, True, YELLOW)
            tag = pygame.Rect(self.rect.x, self.rect.y - label.get_height() - 14,
                              label.get_width() + 24, label.get_height() + 12)
            pygame.draw.rect(layar, (15, 15, 35), tag)
            pygame.draw.rect(layar, WHITE, tag, 2)
            layar.blit(label, (tag.x + 12, tag.y + 6))

        # Teks berjalan: bungkus teks penuh dulu, lalu tampilkan sebagian
        lebar = self.rect.width - 2 * self.padding
        baris = bungkus_teks(baris_data["text"], self.font_teks, lebar)
        sisa = int(self.shown)
        y = self.rect.y + self.padding
        for b in baris:
            bagian = b[:max(0, sisa)]
            if bagian:
                layar.blit(self.font_teks.render(bagian, True, WHITE), (self.rect.x + self.padding, y))
            sisa -= len(b) + 1  # +1 untuk spasi antar-baris
            y += self.font_teks.get_linesize()

        # Penanda "tekan untuk lanjut" (segitiga berkedip)
        if self.selesai_mengetik() and int(self.waktu * 2) % 2 == 0:
            x = self.rect.right - 30
            y = self.rect.bottom - 26
            pygame.draw.polygon(layar, YELLOW, [(x, y), (x + 14, y), (x + 7, y + 10)])