from screen import Screen

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = 0, 0
        self.zoom = 0