import pygame
import logging

logging.basicConfig(level=logging.CRITICAL)
#logging.disable()

class MenuSecondary:
    menu_open = False
    menu_x = -1000

    def loadMenuBackground(self):
        background = pygame.image.load("assets/menu assets/MenuSecondaryBackground.jpg")
        background = pygame.transform.scale(background, (800, 600))
        return background

    def drawMenuIcon(self, screen, icon):
        screen.blit(icon, (730, 20))

    def drawMenuOptions(self, screen, menu_x):
        font = pygame.font.SysFont('Arial', 24)
        settings_text = font.render("Settings", True, (255, 255, 255))
        screen.blit(settings_text, (menu_x + 20, 100))

        restart_text = font.render("Restart Game", True, (255, 255, 255))
        screen.blit(restart_text, (menu_x + 20, 300))

        save_text = font.render("Save Changes and Exit", True, (255, 255, 255))
        screen.blit(save_text, (menu_x + 20, 150))

    def drawMenu(self, screen, menu_x, background_image):
        logging.debug("MenuSecondary selected")
        screen.blit(background_image, (menu_x, 0))  # Draw the background at the updated menu_x position
        self.drawMenuOptions(screen, menu_x)

    def menuToggle(self):
        logging.debug(f"Menu open status: {self.menu_open}")
        if self.menu_open:
            self.menu_x += 30  # Move menu right when open
            if self.menu_x > 0:
                self.menu_x = 0  # Stop at 0, meaning the menu is fully open
        elif not self.menu_open:
            self.menu_x -= 30  # Move menu left when closing
            if self.menu_x < -1000:
                self.menu_x = -1000  # Stop at -1000, meaning the menu is fully closed
        logging.debug(f"Menu x after toggle: {self.menu_x}")

    def handleMouseClick(self, pos):
        button_x = self.menu_x + 20
        button_y = 150  # This is the position for the first button ("Save Changes and Exit")
        button_width = 250
        button_height = 30
        
        # "Save Changes and Exit" button bounds
        if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
            logging.debug("Save Changes and Exit clicked")
            self.menu_open = False

        # "Restart Game" button bounds (adjusting the position)
        restart_button_y = 300  # Position for the "Restart Game" button
        if button_x <= pos[0] <= button_x + button_width and restart_button_y <= pos[1] <= restart_button_y + button_height:
            logging.critical("Restart Game clicked")
            self.restartGame()

    def restartGame(self):
        logging.critical("Restart game")

        self.menu_open = False
        self.menu_x = -1000

        # Additional restart logic can go here


    def gameLoop(self, screen, clock, menu_icon):
        running = True
        background_image = self.loadMenuBackground()
        
        while running:
            screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_icon.get_rect(topleft=(730, 20)).collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                    if self.menu_open:
                        self.handleMouseClick(event.pos) 

            self.menuToggle()
            self.drawMenuIcon(screen, menu_icon)

            if self.menu_open:
                self.drawMenu(screen, self.menu_x, background_image)
            else:
                self.drawMenu(screen, self.menu_x, background_image)  # Draw background shifting when closing

            pygame.display.flip()  # Update the screen
            clock.tick(30)  # Limit the frame rate to 30 FPS

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

menu_icon = pygame.image.load("assets/menu assets/MenuSecondary.jpg")
menu_icon = pygame.transform.scale(menu_icon, (50, 50))

menu = MenuSecondary()
menu.gameLoop(screen, clock, menu_icon)
