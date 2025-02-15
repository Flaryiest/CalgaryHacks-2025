import pygame

class Map:
    def __init__(self, screen, player):
        self.x = player.x
        self.y = player.y

        self.width, self.height = pygame.display.get_surface().get_size()

        self.map = pygame.image.load("assets\\map.png")
        self.map = pygame.transform.scale(self.map, (self.width, self.height))
        
        self.rect = self.map.get_rect()
        self.screen = screen
        self.player = player

        self.cache = {}
    
    def render(self):
        width = int(self.rect.width * self.player.zoom)
        height = int(self.rect.height * self.player.zoom)
        
        try:
            scaled_map = self.cache[(width, height)]
        except KeyError:
            scaled_map = pygame.transform.scale(self.map, (width, height))
            self.cache[(width, height)] = scaled_map

        offset_x = (self.width // 2) - (self.player.x * self.player.zoom)
        offset_y = (self.height // 2) - (self.player.y * self.player.zoom)

        self.screen.blit(scaled_map, (offset_x, offset_y))
    