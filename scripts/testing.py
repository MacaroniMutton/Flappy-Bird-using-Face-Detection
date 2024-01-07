import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()
running = True
img = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
mask = pygame.mask.from_surface(img)

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
    
    screen.fill((100, 100, 55))
    screen.blit(mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(60)
pygame.quit()