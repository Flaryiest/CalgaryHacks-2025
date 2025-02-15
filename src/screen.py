import pygame

class Screen:
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((500, 500))

        pygame.display.set_caption("Save the Animals!!!") 

    def update():
        pygame.display.update()