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

plants = []
for biome in map.biomes:
    for i in range(0, 2):
        coordinates = random.choice(map.biomes[biome])
        plants.append(Plant(player, screen, coordinates[0] * 1.6, coordinates[1] * 1.6))

hover = {"status": False, "obj": None}
dialogue = pygame.image.load("assets\\dialogue.png")
dialogue = pygame.transform.scale(dialogue, (900, 300))
while run: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 2]:
                if event.button == 1:
                    for plant in plants:
                        if plant.rect.collidepoint(pygame.mouse.get_pos()):
                            background = screen.copy()
                            while True:
                                screen.blit(background, (0, 0))
                                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(map.width // 2 - 450, 300, 900, 300))
                                screen.blit(dialogue, (map.width // 2 - 450, 300))
                                pygame.display.flip()

                                
                scroll = True
            if event.button == 4:
                player.zoom += zoom
               
            elif event.button == 5:
                player.zoom -= zoom


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in [1, 2]:
                scroll = False

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
                    
    screen.fill((0, 91, 171))
    map.render()

    for plant in plants:
        if plant.rect.collidepoint(pygame.mouse.get_pos()):
            plant.multiplier = 1.1
        else:
            plant.multiplier = 1
        plant.render()

    pygame.display.flip()



