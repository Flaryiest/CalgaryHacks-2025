import json
import numpy as np
from PIL import Image
import pygame

class Map:
    def __init__(self, screen, player):
        self.x = player.x
        self.y = player.y

        self.width, self.height = pygame.display.get_surface().get_size()

        self.image = pygame.image.load("assets\\map.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.rect = self.image.get_rect()
        self.screen = screen
        self.player = player

        self.cache = {}

        image = Image.open("assets\\map.png").convert("RGB")
        self.matrix = np.array(image).tolist()
        
        with open("biomes.json", 'r') as f:
            self.biomes = json.load(f)

            
    def render(self):
        width = int(self.rect.width * self.player.zoom)
        height = int(self.rect.height * self.player.zoom)
        
        try:
            scaled_map = self.cache[(width, height)]
        except KeyError:
            scaled_map = pygame.transform.scale(self.image, (width, height))
            self.cache[(width, height)] = scaled_map

        offset_x = (self.width // 2) - (self.player.x * self.player.zoom)
        offset_y = (self.height // 2) - (self.player.y * self.player.zoom)

        self.screen.blit(scaled_map, (offset_x, offset_y))
    