import pygame

class Plant:
    def __init__(self, player, screen, x, y, biome, dir="assets\\factory.png", scale=1):
        self.player = player
        self.screen = screen
        self.scale = scale
        self.biome = biome

        self.image = pygame.image.load(dir)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.width, self.height = pygame.display.get_surface().get_size()
        self.x, self.y = x, y
        self.multiplier = 1
    
    def render(self):
        offset_x = (self.width // 2) - (self.player.x * self.player.zoom)
        offset_y = (self.height // 2) - (self.player.y * self.player.zoom)

        zoomed_x = (self.x * self.player.zoom) + offset_x
        zoomed_y = (self.y * self.player.zoom) + offset_y

        scale = int(150 * self.player.zoom // 2) * self.multiplier * self.scale
        scaled_image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = pygame.Rect(zoomed_x, zoomed_y, scale, scale)

        self.screen.blit(scaled_image, (zoomed_x, zoomed_y))