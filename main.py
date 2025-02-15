from src import Screen, Settings
import pygame

screen = Screen()
setting = Settings()

run = True

while run: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False


