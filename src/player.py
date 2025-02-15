import pygame

class Player:
    def __init__(self, screen, min=1, max=5):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.x, self.y = self.width // 2, self.height // 2
        
        self.min = min
        self.max = max
        self.zoom = 1