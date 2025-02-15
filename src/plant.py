import pygame

class Plant:
    def __init__(self, player, screen, x, y):
        self.player = player
        self.screen = screen

        self.image = pygame.image.load()

        self.x, self.y = x, y
    
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