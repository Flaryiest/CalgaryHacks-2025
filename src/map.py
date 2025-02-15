import pygame
from screen import Screen
class Map:
    def __init__(self, screen, player):
        self.x = player.x
        self.y = player.y
        self.map = pygame.image.load("assets\\map.png")
        self.screen = screen
    
    def render():
        pass
    