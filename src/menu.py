import pygame
import logging

logging.basicConfig(level=logging.DEBUG)
logging.disable()

class MenuSecondary:
    menu_open = True
    menu_x = -1 
    volume = 0.5
    music_playing = False  
    dragging = False 
    start_game = False  

    def loadMenuBackground(self, screen_width, screen_height):
        background = pygame.image.load("assets/menu assets/MenuSecondaryBackground.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
        return background

    def drawMenuIcon(self, screen, icon):
        screen.blit(icon, (20, 20))

    def drawMenuOptions(self, screen, menu_x, screen_width, screen_height):
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

    
        rect_x = menu_x + 15
        rect_y = 140  
        rect_width = 200
        rect_height = 35  
        border_thickness = 2 
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_thickness)


        slider_x = menu_x + 20
        slider_y = 450
        slider_width = 250
        slider_height = 10
        pygame.draw.rect(screen, (255, 255, 255), (slider_x, slider_y, slider_width, slider_height))
        
 
        knob_image = pygame.image.load("assets/Capybara slider.png")
        knob_width, knob_height = knob_image.get_size()
        knob_x = slider_x + self.volume * slider_width - knob_width // 2  
        knob_y = slider_y + (slider_height - knob_height) // 2 -10 
        screen.blit(knob_image, (knob_x, knob_y))  

    def drawMenu(self, screen, menu_x, background_image, screen_width, screen_height):
        logging.debug("MenuSecondary selected")
        screen.blit(background_image, (menu_x, 0))  
        self.drawMenuOptions(screen, menu_x, screen_width, screen_height)

    def menuToggle(self, screen_width):
        logging.debug(f"Menu open status: {self.menu_open}")
        if self.menu_open:
            self.menu_x += 30  
            if self.menu_x > 0:
                self.menu_x = 0  
        elif not self.menu_open:
            self.menu_x -= 30  
            if self.menu_x < -screen_width:
                self.menu_x = -screen_width 
        logging.debug(f"Menu x after toggle: {self.menu_x}")

    def handleMouseClick(self, pos, screen):
        button_x = self.menu_x + 20
        button_y = 150  
        button_width = 250
        button_height = 30

        if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
            logging.debug("Save Changes and Exit clicked")
            self.menu_open = False
            self.start_game = True  
            self.stopAudio() 
            screen_width, screen_height = screen.get_size()
            self.menu_x = -screen_width 


        restart_button_y = 300  
        if button_x <= pos[0] <= button_x + button_width and restart_button_y <= pos[1] <= restart_button_y + button_height + 20:
            logging.critical("Restart Game clicked")
            self.restartGame(screen)


        slider_x = button_x
        slider_y = 450
        slider_width = 250
        slider_height = 10
        if slider_x <= pos[0] <= slider_x + slider_width and slider_y <= pos[1] <= slider_y + slider_height:
            new_volume = (pos[0] - slider_x) / slider_width 
            self.setVolume(new_volume)
            self.dragging = True

    def handleMouseDrag(self, pos):
        if self.dragging:
            slider_x = self.menu_x + 20
            slider_y = 450
            slider_width = 250

            new_volume = (pos[0] - slider_x) / slider_width
            self.setVolume(new_volume)

    def setVolume(self, volume):
        self.volume = max(0, min(volume, 1))
        pygame.mixer.music.set_volume(self.volume)

    def restartGame(self, screen):
        logging.critical("Restart game")

        self.menu_open = False
        screen_width, screen_height = screen.get_size()
        self.menu_x = -screen_width  
        self.start_game = True  



    def loadAndPlayAudio(self):
        if not self.music_playing:  
            pygame.mixer.music.load("Audio/Undertale OST 054 Hotel.mp3")  
            pygame.mixer.music.set_volume(self.volume)  
            pygame.mixer.music.play(-1, 0.0) 
            self.music_playing = True
            logging.debug("Menu music started playing")

    def stopAudio(self):
        if self.music_playing:
            pygame.mixer.music.stop() 
            self.music_playing = False
            logging.debug("Menu music stopped")

    def gameLoop(self, screen, clock, menu_icon_pressed, menu_icon_notpressed):
        running = True
        screen_width, screen_height = screen.get_size()
        background_image = self.loadMenuBackground(screen_width, screen_height)

        pygame.mixer.music.set_volume(self.volume)
        
        while running:
            screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_icon_notpressed.get_rect(topleft=(20, 20)).collidepoint(event.pos) or menu_icon_pressed.get_rect(topleft=(20, 20)).collidepoint(event.pos):
                        self.menu_open = not self.menu_open
                    if self.menu_open:
                        self.handleMouseClick(event.pos, screen)
                elif event.type == pygame.MOUSEMOTION:
                    if self.menu_open and self.dragging:
                        self.handleMouseDrag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False  

            self.menuToggle(screen_width)

            if self.menu_open:
                self.loadAndPlayAudio()
            else:
                self.stopAudio()

            menu_icon = menu_icon_pressed if self.menu_open else menu_icon_notpressed
            self.drawMenuIcon(screen, menu_icon)

            if self.menu_open:
                self.drawMenu(screen, self.menu_x, background_image, screen_width, screen_height)
            else:
                self.drawMenu(screen, self.menu_x, background_image, screen_width, screen_height)  

            pygame.display.flip() 
            clock.tick(30)

            if self.start_game:
                running = False  

'''
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clock = pygame.time.Clock()

menu_icon_pressed = pygame.image.load("assets/menu assets/Button 1, Pressed.png")
menu_icon_pressed = pygame.transform.scale(menu_icon_pressed, (50, 50))
menu_icon_notpressed = pygame.image.load("assets/menu assets/Button 1, Unpressed.png")
menu_icon_notpressed = pygame.transform.scale(menu_icon_notpressed, (50, 50))

menu = MenuSecondary()
menu.gameLoop(screen, clock, menu_icon_pressed, menu_icon_notpressed)
'''