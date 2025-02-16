from src import *
import pygame, logging, random
from src.menu import MenuSecondary

logging.basicConfig(level=logging.DEBUG)

pygame.init()
pygame.font.init()

settings = Settings()

if settings.settings["fullscreen"] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.settings["width"], settings.settings["height"]))

pygame.display.set_caption("Save the Animals!!!")

menu = MenuSecondary()
menu_icon_pressed = pygame.image.load("assets/menu assets/Button 1, Pressed.png")
menu_icon_pressed = pygame.transform.scale(menu_icon_pressed, (50, 50))
menu_icon_notpressed = pygame.image.load("assets/menu assets/Button 1, Unpressed.png")
menu_icon_notpressed = pygame.transform.scale(menu_icon_notpressed, (50, 50))

clock = pygame.time.Clock()

# Main game loop
player = Player(screen)
map = Map(screen, player)
zoom = 0.1
run = True
scroll = False

plants = []
for biome in map.biomes:
    for i in range(0, 2):
        coordinates = random.choice(map.biomes[biome])
        if biome == "ocean":
            plants.append(Plant(player, screen, coordinates[0] * 1.6, coordinates[1] * 1.6, dir="assets\\pump.png", scale=4, biome=biome))
        else:
            print(biome)
            plants.append(Plant(player, screen, coordinates[0] * 1.6, coordinates[1] * 1.6, biome=biome))

hover = {"status": False, "obj": None}
dialogue = pygame.image.load("assets\\dialogue.png")
dialogue = pygame.transform.scale(dialogue, (900, 300))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_icon_notpressed.get_rect(topleft=(20, 20)).collidepoint(event.pos) or menu_icon_pressed.get_rect(topleft=(20, 20)).collidepoint(event.pos):
                menu.menu_open = not menu.menu_open
            if menu.menu_open:
                menu.handleMouseClick(event.pos, screen)
        elif event.type == pygame.MOUSEMOTION:
            if menu.menu_open and menu.dragging:
                menu.handleMouseDrag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            menu.dragging = False

        if not menu.menu_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1, 2]:
                    if event.button == 1:
                        for plant in plants:
                            if plant.rect.collidepoint(pygame.mouse.get_pos()):
                                background = screen.copy()
                                while True:
                                    screen.blit(background, (0, 0))
                                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(map.width // 2 - 450, 300, 900, 300))
                                    screen.blit(dialogue, (map.width // 2 - 450, 300))
                                    pygame.display.flip()
                    scroll = True
                if event.button == 4:
                    player.zoom += zoom
                elif event.button == 5:
                    player.zoom -= zoom
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in [1, 2]:
                    scroll = False
            elif event.type == pygame.MOUSEMOTION:
                if scroll:
                    rel_x, rel_y = event.rel
                    player.x -= rel_x
                    player.y -= rel_y

    if not menu.menu_open:
        if player.x < 0:
            player.x = 0
        if player.x > player.width:
            player.x = player.width
        if player.y < 0:
            player.y = 0
        if player.y > player.height:
            player.y = player.height

        screen.fill((0, 91, 171))
        map.render()

        for plant in plants:
            if plant.rect.collidepoint(pygame.mouse.get_pos()):
                plant.multiplier = 1.1
            else:
                plant.multiplier = 1
            plant.render()

    if menu.menu_open:
        menu.loadAndPlayAudio()
    else:
        menu.stopAudio()

    menu_icon = menu_icon_pressed if menu.menu_open else menu_icon_notpressed
    menu.drawMenuIcon(screen, menu_icon)

    if menu.menu_open:
        screen_width, screen_height = screen.get_size()
        menu.drawMenu(screen, menu.menu_x, menu.loadMenuBackground(screen_width, screen_height), screen_width, screen_height)

    pygame.display.flip()
    clock.tick(30)



