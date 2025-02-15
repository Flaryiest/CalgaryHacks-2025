import pygame

class Plant:
    def __init__(self, player, screen, x, y):
        self.player = player
        self.screen = screen

        self.image = pygame.image.load("assets\\factory.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.width, self.height = pygame.display.get_surface().get_size()
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
    
    def render(self):
        offset_x = (self.width // 2) - (self.player.x * self.player.zoom)
        offset_y = (self.height // 2) - (self.player.y * self.player.zoom)

        zoomed_x = (self.x * self.player.zoom) + offset_x
        zoomed_y = (self.y * self.player.zoom) + offset_y

        scaled_image = pygame.transform.scale(self.image, (int(100 * self.player.zoom // 2), int(100 * self.player.zoom // 2)))

        self.screen.blit(scaled_image, (zoomed_x, zoomed_y))