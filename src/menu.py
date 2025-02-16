import pygame
import logging

logging.basicConfig(level=logging.DEBUG)
logging.disable()

class MenuSecondary:
    menu_open = False
    menu_x = -1000
    volume = 0.5
    music_playing = False  # To track if music is already playing
    dragging = False  # Track if the user is dragging the volume slider

    def loadMenuBackground(self):
        background = pygame.image.load("assets/menu assets/MenuSecondaryBackground.jpg")
        background = pygame.transform.scale(background, (800, 600))
        return background

    def drawMenuIcon(self, screen, icon):
        screen.blit(icon, (730, 20))

    def drawMenuOptions(self, screen, menu_x):
        font = pygame.font.SysFont("assets/Fonts/TepidTerminal.ttf", 24)
        settings_text = font.render("Settings", True, (255, 255, 255))
        screen.blit(settings_text, (menu_x + 20, 100))

        restart_button = pygame.transform.scale(pygame.image.load("assets/menu assets/Green restart button, Unpressed.png"), (30, 30))
        restart_text = font.render("Restart Game", True, (255, 255, 255))
        screen.blit(restart_text, (menu_x + 20, 300))
        screen.blit(restart_button, (menu_x + 60, 320))

        volume_text = font.render(f"Volume: {int(self.volume * 100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (menu_x + 20, 400))

        save_text = font.render("Save Changes and Exit", True, (255, 255, 255))
        screen.blit(save_text, (menu_x + 20, 150))

        # Draw a rectangle under the "Save Changes and Exit" text with no fill (just a border)
        rect_x = menu_x + 15
        rect_y = 140  # Adjust the y-coordinate to place it right under the text
        rect_width = 200
        rect_height = 35  # Height of the rectangle
        border_thickness = 2  # Set the thickness of the border
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_thickness)

        # Draw the volume slider
        slider_x = menu_x + 20
        slider_y = 450
        slider_width = 250
        slider_height = 10
        pygame.draw.rect(screen, (255, 255, 255), (slider_x, slider_y, slider_width, slider_height))
        
        # Load the slider knob image
        knob_image = pygame.image.load("assets/Capybara slider.png")  # Path to your knob image
        knob_width, knob_height = knob_image.get_size()
        knob_x = slider_x + self.volume * slider_width - knob_width // 2  # Adjust to position the knob correctly
        knob_y = slider_y + (slider_height - knob_height) // 2 -10 # Vertically center the knob
        screen.blit(knob_image, (knob_x, knob_y))  # Draw the knob image

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
            self.stopAudio()  # Stop audio when menu is closed

        # "Restart Game" button bounds (adjusting the position)
        restart_button_y = 300  # Position for the "Restart Game" button
        if button_x <= pos[0] <= button_x + button_width and restart_button_y <= pos[1] <= restart_button_y + button_height + 20:
            logging.critical("Restart Game clicked")
            self.restartGame()

        # Check if the click is on the volume slider area
        slider_x = button_x
        slider_y = 450
        slider_width = 250
        slider_height = 10
        if slider_x <= pos[0] <= slider_x + slider_width and slider_y <= pos[1] <= slider_y + slider_height:
            new_volume = (pos[0] - slider_x) / slider_width  # Calculate new volume
            self.setVolume(new_volume)
            self.dragging = True

    def handleMouseDrag(self, pos):
        if self.dragging:
            slider_x = self.menu_x + 20
            slider_y = 450
            slider_width = 250
            # Update volume based on the new mouse position
            new_volume = (pos[0] - slider_x) / slider_width
            self.setVolume(new_volume)

    def setVolume(self, volume):
        self.volume = max(0, min(volume, 1))
        pygame.mixer.music.set_volume(self.volume)

    def restartGame(self):
        logging.critical("Restart game")

        self.menu_open = False
        self.menu_x = -1000

        # Additional restart logic can go here

    def loadAndPlayAudio(self):
        if not self.music_playing:  # Avoid loading the audio if it's already playing
            pygame.mixer.music.load("Audio/Undertale OST 054 Hotel.mp3")  # Path to your audio file
            pygame.mixer.music.set_volume(self.volume)  # Set the volume to current level
            pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely
            self.music_playing = True
            logging.debug("Menu music started playing")

    def stopAudio(self):
        if self.music_playing:
            pygame.mixer.music.stop()  # Stop the music
            self.music_playing = False
            logging.debug("Menu music stopped")

    def gameLoop(self, screen, clock, menu_icon_pressed, menu_icon_notpressed):
        running = True
        background_image = self.loadMenuBackground()

        pygame.mixer.music.set_volume(self.volume)
        
        while running:
            screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_icon_notpressed.get_rect(topleft=(730, 20)).collidepoint(event.pos) or menu_icon_pressed.get_rect(topleft=(730, 20)).collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                    if self.menu_open:
                        self.handleMouseClick(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.menu_open and self.dragging:
                        self.handleMouseDrag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False  # Stop dragging when mouse button is released

            self.menuToggle()

            # Play music only when the menu is open
            if self.menu_open:
                self.loadAndPlayAudio()
            else:
                self.stopAudio()

            # Choose the appropriate icon based on the menu state (open or closed)
            menu_icon = menu_icon_pressed if self.menu_open else menu_icon_notpressed
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

menu_icon_pressed = pygame.image.load("assets/menu assets/Button 1, Pressed.png")
menu_icon_pressed = pygame.transform.scale(menu_icon_pressed, (50, 50))
menu_icon_notpressed = pygame.image.load("assets/menu assets/Button 1, Unpressed.png")
menu_icon_notpressed = pygame.transform.scale(menu_icon_notpressed, (50, 50))

menu = MenuSecondary()
menu.gameLoop(screen, clock, menu_icon_pressed, menu_icon_notpressed)
