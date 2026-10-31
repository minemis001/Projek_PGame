import pygame

pygame.init()

isRun = True

window = pygame.display.set_mode((500,500))

x = 250
y = 250

panjang = 20
lebar = 20

speed = 10

while isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRun = False

    window.fill((255,255,255))
    pygame.draw.rect(window,(255,0,0),(x,y,lebar,panjang))

    pygame.display.update()

pygame.quit()