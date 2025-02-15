from src import *
import pygame, logging, random

logging.basicConfig(level=logging.DEBUG)

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

plants = [Plant(player, screen, random.randint(0, 1920), random.randint(0, 1080)) for i in range(0, 10)]

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
                zoomIncrement = 0.1

        elif event.type == pygame.MOUSEMOTION:
            if scroll:
                rel_x, rel_y = event.rel

                player.x -= rel_x
                player.y -= rel_y

    if player.x < 0:
        player.x = 0
    
    if player.x > player.width:
        player.x = player.width

    if player.y < 0:
        player.y = 0
    
    if player.y > player.height:
        player.y = player.height
                    
    screen.fill((0, 105, 170))
    map.render()

    for plant in plants:
        if plant.rect.collidepoint(pygame.mouse.get_pos()):
            print(random.randint(0, 100))
        plant.render()

    pygame.display.flip()



