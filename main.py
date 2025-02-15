from src import *
import pygame

settings = Settings()

if settings.settings["fullscreen"] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.settings["width"], settings.settings["height"]))

pygame.display.set_caption("Save the Animals!!!") 

player = Player(screen)
map = Map(screen, player)
zoom = 0.1
run = True
scroll = False
while run: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                scroll = True
            if event.button == 4:
                player.zoom += zoom
            elif event.button == 5:
                player.zoom -= zoom

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                scroll = False

        elif event.type == pygame.MOUSEMOTION:
            if scroll:
                rel_x, rel_y = event.rel
                player.x -= rel_x
                player.y -= rel_y
    
    screen.fill((0, 0, 0))
    map.render()

    pygame.display.flip()



