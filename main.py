from src import Settings
import pygame

settings = Settings()

if settings.settings["fullscreen"] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.settings["width"], settings.settings["height"]))

pygame.display.set_caption("Save the Animals!!!") 
run = True

while run: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False


